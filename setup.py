import os
import subprocess
import sys

def create_virtual_env():
    print("Creating virtual environment...")
    subprocess.check_call([sys.executable, '-m', 'venv', 'venv'])
    print("Virtual environment created.")

def install_dependencies():
    print("Installing dependencies from requirements.txt...")
    # Determine the correct command based on the operating system
    pip_executable = os.path.join('venv', 'Scripts' if os.name == 'nt' else 'bin', 'pip')
    subprocess.check_call([pip_executable, 'install', '-r', 'requirements.txt'])
    print("Dependencies installed.")

def verify_sgpt():
    print("Verifying sgpt installation...")
    # Adjust the sgpt path for Windows if necessary
    sgpt_path = os.path.join(os.environ.get("HOME", ""), ".local", "bin", "sgpt") if os.name != 'nt' else "sgpt"
    try:
        subprocess.check_call([sgpt_path, '--version'])
        print("sgpt is correctly installed.")
    except subprocess.CalledProcessError:
        print("sgpt is not installed or not found at", sgpt_path)

def main():
    create_virtual_env()
    install_dependencies()
    verify_sgpt()
    # Provide OS-specific instructions for activating the virtual environment
    activate_command = "source venv/bin/activate" if os.name != 'nt' else r".\venv\Scripts\activate"
    print(f"Setup completed. Please activate the virtual environment with `{activate_command}`.")

if __name__ == "__main__":
    main()