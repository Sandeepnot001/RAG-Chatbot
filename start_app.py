import subprocess
import os
import sys
import time
import signal

def start_backend():
    print("Starting Backend...")
    return subprocess.Popen(
        [sys.executable, "-m", "backend.main"],
        cwd=os.getcwd()
    )

def start_frontend():
    print("Starting Frontend...")
    # Using shell=True for npm on Windows
    return subprocess.Popen(
        "npm run dev",
        cwd=os.path.join(os.getcwd(), "frontend"),
        shell=True
    )

def main():
    backend_proc = None
    frontend_proc = None
    
    try:
        backend_proc = start_backend()
        frontend_proc = start_frontend()
        
        print("\n" + "="*50)
        print("Application Started Successfully!")
        print(f"Backend: http://127.0.0.1:8000")
        print(f"Frontend: http://localhost:5173")
        print("Press Ctrl+C to stop both services.")
        print("="*50 + "\n")
        
        while True:
            time.sleep(1)
            if backend_proc.poll() is not None:
                print("Backend process exited!")
                break
            if frontend_proc.poll() is not None:
                print("Frontend process exited!")
                break
                
    except KeyboardInterrupt:
        print("\nStopping services...")
    finally:
        if backend_proc:
            backend_proc.terminate()
        if frontend_proc:
            # On Windows, taskkill might be needed for npm/vite child processes
            if os.name == 'nt':
                subprocess.run(['taskkill', '/F', '/T', '/PID', str(frontend_proc.pid)], capture_output=True)
            else:
                frontend_proc.terminate()
        print("Cleanup done.")

if __name__ == "__main__":
    main()
