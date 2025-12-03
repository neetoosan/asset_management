import sys
from pathlib import Path
# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
import traceback

try:
    from PySide6.QtWidgets import QApplication, QMessageBox
    from PySide6.QtCore import QFile, QTextStream
    from app.gui.main_window import MainWindow
    from app.gui.views.login_screen import LoginScreen
    from app.gui.views.welcome_screen import WelcomeScreen
    from app.core.config import Config
    from app.services.session_service import SessionService
    from app.services.config_service import ConfigService
    from app.core.database import init_db
    from app.utils.theme_manager import ThemeManager, Theme
    from PySide6.QtCore import QThread, Signal, QObject, QTimer
except Exception:
    print("Import error in app/main.py:")
    traceback.print_exc()
    # Also print module search path for debugging
    print('\nPython sys.path:')
    for p in sys.path:
        print(' -', p)
    raise

def main():
    # Initialize configuration
    config = Config()    
    # Initialize database and create default data
    try:
        # Initialize database
        init_db(config.DATABASE_URL)
        
        # Import here to avoid circular imports
        from app.services.user_service import UserService
        from app.services.role_service import RoleService
        from app.core.database import get_db
        from app.core.models import Role, Permission, RolePermission, UserRole, PermissionType
        
        # Initialize services
        user_service = UserService()
        role_service = RoleService()
        
        with get_db() as session:
            # Ensure admin role exists
            admin_role = session.query(Role).filter_by(name=UserRole.ADMIN).first()
            if not admin_role:
                admin_role = Role(name=UserRole.ADMIN, description="Administrator with full access")
                session.add(admin_role)
                session.flush()
            
            # Ensure all permissions exist and are granted to admin
            for perm_type in PermissionType:
                perm = session.query(Permission).filter_by(name=perm_type).first()
                if not perm:
                    perm = Permission(name=perm_type)
                    session.add(perm)
                    session.flush()
                    # Grant to admin role
                    role_perm = RolePermission(
                        role_id=admin_role.id,
                        permission_id=perm.id,
                        granted="true"
                    )
                    session.add(role_perm)
                else:
                    # Ensure admin role has an explicit grant for this permission
                    rp = session.query(RolePermission).filter_by(role_id=admin_role.id, permission_id=perm.id).first()
                    if not rp:
                        rp = RolePermission(role_id=admin_role.id, permission_id=perm.id, granted="true")
                        session.add(rp)
                    else:
                        # If a RolePermission exists but is not granted, set it to granted for admin
                        if getattr(rp, 'granted', None) != "true":
                            rp.granted = "true"
                            session.add(rp)
            
            session.commit()
            print("Database initialized successfully")
            
    except Exception as e:
        print(f"Database initialization error: {e}")
        sys.exit(1)
    
    # Create application
    app = QApplication(sys.argv)
    # Use default behavior: quit when the last window is closed so the process exits
    app.setQuitOnLastWindowClosed(True)

    # Ensure any leftover threads/cleanup run when last window is closed
    def _on_last_window_closed():
        try:
            print("Application: last window closed, quitting application")
        except Exception:
            pass
    app.lastWindowClosed.connect(_on_last_window_closed)
    
    # Initialize theme manager and apply theme
    theme_manager = ThemeManager()
    theme_manager.apply_theme()
    
    # Create welcome and login screens
    welcome_screen = WelcomeScreen()
    login_screen = LoginScreen()
    
    # When user clicks Login on the welcome screen, show the login form
    def on_welcome_login():
        try:
            welcome_screen.hide()
            # show login screen and give focus to username
            login_screen.show()
            try:
                login_screen.ui.usernameInput.setFocus()
            except Exception:
                pass
        except Exception:
            pass
    welcome_screen.loginRequested.connect(on_welcome_login)
    # Create main window but don't show it yet - will be created after successful login
    main_window = None
    
    # Prepare loading screen (but don't show yet)
    from app.gui.views.loading_screen import LoadingScreen
    loader = LoadingScreen()

    # Connect login success to show main window
    def on_login_successful(session_token):
        nonlocal main_window
        print(f"Login successful, initializing with token: {session_token}")  # Debug logging
        login_screen.hide()

        # Start non-blocking loader (each image shown for 1.5s by default)
        try:
            loader.start(1500)
        except Exception:
            # Fallback to modal play if start fails
            try:
                loader.play(1500)
            except Exception:
                pass
        # Run session verification and main window initialization in a background thread
        class InitWorker(QObject):
            finished = Signal(bool, object)

            def __init__(self, token, config):
                super().__init__()
                self.token = token
                self.config = config

            def run(self):
                try:
                    print("InitWorker: starting backend session validation")
                    # Perform backend-only session validation to avoid GUI creation in worker
                    from app.services.session_service import SessionService as _SessionService
                    ss = _SessionService()
                    valid = ss.validate_session(self.token)
                    print(f"InitWorker: validation result = {valid}")
                    if valid:
                        # return True and no payload data - main thread will construct GUI
                        self.finished.emit(True, None)
                    else:
                        self.finished.emit(False, 'Invalid session token')
                except Exception as ex:
                    print(f"InitWorker: exception: {ex}")
                    self.finished.emit(False, str(ex))

        # QObject-based finish handler created on the main thread. This ensures
        # the handler has a GUI-thread affinity so GUI objects are created safely.
        class FinishHandler(QObject):
            def __init__(self):
                super().__init__()

            def handle(self, success, payload):
                nonlocal main_window
                print(f"on_init_finished: called (success={success}, payload={payload})")
                try:
                    # Clean up worker/thread references after worker finished
                    if hasattr(loader, '_init_worker_thread'):
                        wt = loader._init_worker_thread
                        try:
                            # Only quit/wait if we're not running on the worker thread
                            if QThread.currentThread() is not wt:
                                wt.quit()
                                ok = wt.wait(5000)
                                print(f"on_init_finished: worker_thread.wait returned {ok}; isRunning={wt.isRunning()}")
                                if ok:
                                    try:
                                        wt.deleteLater()
                                    except Exception:
                                        pass
                                    try:
                                        del loader._init_worker_thread
                                    except Exception:
                                        pass
                                else:
                                    print("on_init_finished: worker did not stop within timeout; leaving thread object for later cleanup")
                        except Exception as e:
                            print(f"on_init_finished: exception while stopping thread: {e}")
                    if hasattr(loader, '_init_worker'):
                        try:
                            loader._init_worker.deleteLater()
                        except Exception:
                            pass
                        try:
                            del loader._init_worker
                        except Exception:
                            pass

                    # Ensure loader.stop() runs on the GUI thread's event loop to avoid
                    # stopping timers from another thread. Schedule via singleShot(0,...)
                    try:
                        QTimer.singleShot(0, loader.stop)
                    except Exception:
                        try:
                            loader.stop()
                        except Exception:
                            pass

                    if not success:
                        print(f"on_init_finished: initialization failed: {payload}")
                        QMessageBox.critical(None, 'Initialization Error', f'Failed to initialize application: {payload}')
                        return

                    # Construct GUI objects on the main (GUI) thread only
                    print("on_init_finished: constructing MainWindow")
                    main_window = MainWindow(config)
                    # initialize_session may perform DB operations but creates GUI elements only on main thread
                    main_window.initialize_session(session_token)
                    # Connect main window logout signal to the top-level handler so
                    # the login screen is shown when the user logs out.
                    try:
                        main_window.logoutRequested.connect(on_logout_requested)
                    except Exception as e:
                        print(f"Failed to connect logoutRequested signal: {e}")
                    main_window.show()
                    print("on_init_finished: MainWindow shown")
                except Exception as ex:
                    print(f"on_init_finished: exception: {ex}")
                    QMessageBox.critical(None, 'Initialization Exception', str(ex))

        # Instantiate the finish handler on the main thread and keep a reference
        finish_handler = FinishHandler()
        loader._finish_handler = finish_handler

        # Start worker thread
        worker_thread = QThread()
        worker = InitWorker(session_token, config)
        worker.moveToThread(worker_thread)
        # Keep references on loader so they are not garbage collected
        loader._init_worker_thread = worker_thread
        loader._init_worker = worker

        # Ensure the finished signal is delivered to the main thread's event loop
        # so our FinishHandler.handle runs on the GUI thread. Use a queued connection.
        from PySide6.QtCore import Qt
        worker.finished.connect(finish_handler.handle, type=Qt.QueuedConnection)
        worker_thread.started.connect(worker.run)
        worker_thread.start()
    # Connect logout to show login screen
    def on_logout_requested():
        # Ensure desktop/session state is cleaned up
        try:
            if main_window and hasattr(main_window, 'session_service'):
                try:
                    logout_result = main_window.session_service.logout()
                    print(f"Logout result: {logout_result}")
                except Exception as e:
                    print(f"Error during session_service.logout(): {e}")
                # Clear any stored session token on the main window as a safety
                try:
                    if hasattr(main_window, '_session_token'):
                        main_window._session_token = None
                except Exception:
                    pass
        except Exception:
            pass

        # Hide main window and present login screen with cleared inputs
        try:
            main_window.hide()
        except Exception:
            pass

        # Clear login form
        try:
            login_screen.ui.usernameInput.clear()
            login_screen.ui.passwordInput.clear()
            login_screen.ui.errorLabel.clear()
            login_screen.ui.errorLabel.setText("You have been logged out.")
        except Exception:
            pass

        try:
            login_screen.show()
        except Exception:
            pass
    
    # Connect login handler
    login_screen.loginSuccessful.connect(on_login_successful)
    
    # Show welcome screen first
    welcome_screen.show()
    
    # Run application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()