import sys
import uvicorn
from multiprocessing import Process
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def run_api():
    """Run the FastAPI server"""
    uvicorn.run(
        "app.api.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )

def run_gui():
    """Run the Qt GUI application"""
    from app.main import main
    main()

def run_both():
    """Run both API and GUI"""
    # Start API in a separate process
    api_process = Process(target=run_api)
    api_process.start()
    
    # Run GUI in main process
    try:
        run_gui()
    finally:
        # Ensure API process is terminated when GUI exits
        api_process.terminate()
        api_process.join()

if __name__ == "__main__":
    run_both()