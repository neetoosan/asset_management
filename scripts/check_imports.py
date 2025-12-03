import importlib, traceback, sys, os
# Ensure project root is on sys.path so imports like 'app.*' resolve when this
# script is run from other working directories.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

mods=['app.gui.views.recently_deleted','app.gui.main_window','app.services.asset_service','app.services.user_service']
for m in mods:
    try:
        importlib.import_module(m)
        print(m, 'OK')
    except Exception:
        traceback.print_exc()
        print(m, 'FAILED')
