import os
import subprocess
import sys

def create_virtual_env():
    print("Creating virtual environment...")
    command = [sys.executable, '-m', 'venv', 'venv']
    # Ensure command is executable on both Windows and Unix-type OS
    if os.name == 'nt':
        command.insert(0, 'cmd.exe')
        command.insert(1, '/c')
    try:
        subprocess.check_call(command)
        print("Virtual environment created.")
    except subprocess.CalledProcessError:
        print("Error creating virtual environment.")

def install_dependencies():
    print("Installing dependencies from requirements.txt...")
    # Determine the correct command based on the operating system
    pip_executable = os.path.join('venv', 'Scripts' if os.name == 'nt' else 'bin', 'pip')
    # Ensure command is executable on both Windows and Unix-type OS
    if os.name == 'nt':
        pip_executable = pip_executable.replace('\\', '/')
    try:
        subprocess.check_call([pip_executable, 'install', '-r', 'requirements.txt'])
        print("Dependencies installed.")
    except subprocess.CalledProcessError:
        print("Error installing dependencies.")

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
    try:
        create_virtual_env()
        install_dependencies()
        verify_sgpt()
    except Exception as e:
        print(e)
        print("An error occurred while setting up the environment. Please try again or contact the support team.")
    else:
        # Provide OS-specific instructions for activating the virtual environment
        activate_command = "source venv/bin/activate" if os.name != 'nt' else r".\venv\Scripts\activate"
        print(f"Setup completed. Please activate the virtual environment with `{activate_command}`.")

if __name__ == "__main__":
    main()