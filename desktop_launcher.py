import subprocess
import time
import webview
import sys

def launch_desktop_app():
    # 1. Start the Streamlit dashboard silently in the background
    # This prevents the server from attempting to open a traditional browser tab automatically
    streamlit_process = subprocess.Popen(
        [
            sys.executable, 
            "-m", 
            "streamlit", 
            "run", 
            "master_dashboard.py", 
            "--server.headless=true", 
            "--server.port=8501"
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # 2. Wait 2 seconds for the background telemetry server to completely initialize
    time.sleep(2)

    try:
        # 3. Create and mount the native desktop GUI window
        webview.create_window(
            title="ATOC Autonomous AI Matrix Dashboard", 
            url="http://localhost:8501",
            width=1400,
            height=850,
            resizable=True
        )
        # Start the desktop frame engine
        webview.start()
        
    finally:
        # 4. Clean up background subprocess tracking instances when the window closes
        streamlit_process.terminate()

if __name__ == "__main__":
    launch_desktop_app()