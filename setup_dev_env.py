import os
import subprocess
import sys
import platform

VENV_NAME = "kivy_venv"
REQUIREMENTS = [
    "kivy==2.3.0",
    "kivymd==1.1.1",
    "cryptography",
    "plyer",
    "firebase-admin",
    "requests",
    "python-dotenv"
]

def run_command(cmd, env=None):
    try:
        subprocess.run(cmd, check=True, shell=True, env=env)
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        sys.exit(1)

def create_virtual_env():
    if not os.path.isdir(VENV_NAME):
        print("Creating virtual environment...")
        run_command(f"{sys.executable} -m venv {VENV_NAME}")
    else:
        print("Virtual environment already exists.")

def install_dependencies():
    print("installing dependencies into virtual environment...")
    
    pip_path = os.path.join(
        VENV_NAME, "Scripts" if platform.system() == "Windows" else "bin", "pip"
    )

    for package in REQUIREMENTS:
        print(f"→ Installing: {package}")
        run_command(f'"{pip_path}" install {package}')

def post_install_notice():
    activation_cmd = (
        f"{VENV_NAME}\\Scripts\\activate"
        if platform.system() == "Windows"
        else f"source {VENV_NAME}/bin/activate"
    )
    print("\nSetup complete!")
    print(f"To activate the environment, run:\n\n    {activation_cmd}\n")
    print("You can now run your Kivy app in the development environment.")

if __name__ == "__main__":
    print("Starting KivyMD Dev Environment Setup...")
    create_virtual_env()
    install_dependencies()
    post_install_notice()
