# TeamF-TrackingProject
This project is a KivyMD-based task tracking app for Team F.

## Prerequisites:
- Python 3.10 or higher installed on your system (preferably 3.12) 
- Internet connection for installing packages

- Optional: Visual Studio Code, it will make running the scripts easier
- Optional: Git or GitHub Desktop (If cloning the repo)

## Setup Instructions:

### 1. Get Project Files

#### ZIP FILE METHOD:
- 1. Press the green "**<> Code**" button on this repository
- 2. Click Download as a ZIP File
- 3. Extract the ZIP file into a new folder (preferably empty)

##### OR

#### CLONING REPO METHOD:
- 1. Open your terminal or command prompt
- 2. Cd/Navigate to your preferred folder (preferably empyty)
- 3. Copy and run this command:

    ```bash
    git clone https://github.com/nmartinez71/TeamF-TrackingProject.git
    cd TeamF-TrackingProject

#### 1.5 (Optional): Open the Project in VS Code
If you're using Visual Studio Code:
- 1. Open VS Code.
- 2. Click File > Open Folder...
- 3. Select the folder where you extracted or cloned the project.
    (Optional) When prompted, click "Yes" to install any recommended extensions or trust the folder.

This makes it easier to view and run the commands from inside VS Code.

### 2. Run Setup Script
- Run this command in the project folder:

    python setup_dev_env.py

This Setup Script will create a virtual environment and install all dependencies used in the project

### 3. Activate Environment

- Run this command once the Setup Script ends (it will also suggest it at the end):
    
    kivy_venv\Scripts\activate 

By Activating the environment, Python will be able to access the dependencies and run the Kivy files required for the app.

### 3. Activate Environment

- With the environment activated, start the app:
    
    kivy_venv\Scripts\activate 

- If in VS Code, you should see green "(kivy_venv)" text in the terminal, which indicates the virtual environment is active.


