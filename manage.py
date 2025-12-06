#!/usr/bin/env python3
"""
Traffic Management System CLI
Unified management script for the intelligent traffic management project.
"""
import os
import sys
import argparse
import subprocess
from pathlib import Path

# Constants
PROJECT_ROOT = Path(__file__).parent.absolute()
VENV_PYTHON = PROJECT_ROOT / "venv" / "bin" / "python3"
STREAMLIT_CMD = ["streamlit", "run"]

def get_python_cmd():
    """Get the python command to use."""
    if VENV_PYTHON.exists():
        return str(VENV_PYTHON)
    return sys.executable

def run_streamlit(script_path, port=8501):
    """Run a streamlit application."""
    full_path = PROJECT_ROOT / script_path
    if not full_path.exists():
        print(f"❌ Error: Script not found at {full_path}")
        return False
    
    print(f"🚀 Starting {script_path} on port {port}...")
    cmd = [get_python_cmd(), "-m", "streamlit", "run", str(full_path), "--server.port", str(port)]
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n👋 Stopped.")
    return True

def run_script(script_path, args=None):
    """Run a python script."""
    full_path = PROJECT_ROOT / script_path
    if not full_path.exists():
        print(f"❌ Error: Script not found at {full_path}")
        return False
        
    print(f"🚀 Running {script_path}...")
    cmd = [get_python_cmd(), str(full_path)]
    if args:
        cmd.extend(args)
        
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n👋 Stopped.")
    return True

def main():
    parser = argparse.ArgumentParser(description="Traffic Management System CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Dashboard Commands
    subparsers.add_parser("start-admin", help="Start the Admin Dashboard")
    subparsers.add_parser("start-driver", help="Start the Driver Mobile App")
    subparsers.add_parser("start-all", help="Start Admin and Driver apps")

    subparsers.add_parser("setup", help="Setup test data")
    subparsers.add_parser("clean", help="Clean temporary files")

    args = parser.parse_args()

    if args.command == "start-admin":
        run_streamlit("src/dashboard/admin_panel.py", 8501)
    elif args.command == "start-driver":
        run_streamlit("src/dashboard/driver_app.py", 8502)
    elif args.command == "setup":
        run_script("scripts/setup_test_data.py")
    elif args.command == "clean":
        print("🧹 Cleaning up...")
        subprocess.run(["find", ".", "-type", "d", "-name", "__pycache__", "-exec", "rm", "-rf", "{}", "+"])
        subprocess.run(["find", ".", "-type", "d", "-name", ".pytest_cache", "-exec", "rm", "-rf", "{}", "+"])
        print("✅ Clean complete.")
    elif args.command == "start-all":
        print("🚀 Starting System...")
        procs = []
        try:
            # Start Admin Panel
            print("   - Launching Admin Panel (Port 8501)...")
            p1 = subprocess.Popen([get_python_cmd(), "-m", "streamlit", "run", str(PROJECT_ROOT / "src/dashboard/admin_panel.py"), "--server.port", "8501"])
            procs.append(p1)

            # Start Driver App
            print("   - Launching Driver App (Port 8502)...")
            p2 = subprocess.Popen([get_python_cmd(), "-m", "streamlit", "run", str(PROJECT_ROOT / "src/dashboard/driver_app.py"), "--server.port", "8502"])
            procs.append(p2)
            
            print("\n✅ System running! Press Ctrl+C to stop.")
            for p in procs:
                p.wait()
        except KeyboardInterrupt:
            print("\n👋 Stopping all services...")
            for p in procs:
                p.terminate()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
