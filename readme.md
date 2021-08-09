# WSP Optimized Inspection Data System (WOIDS)
A PDF report generator made for the use of WSP.

## Compliation
This program must be compiled into an executable (exe) in order to be used on WSP's work computers. To make changes to the PDF, you must update the Python code. Follow these steps to download the code and compile it yourself. Otherwise, skip to the Program Use section

### Code
Download the program by either using Git clone (advanced), or download a zip of all the files. Unzip the folder to get started.

### Python
The program is built in Python 3.9, which you can download [here](https://www.python.org/downloads/). Beginners should skip down the Modules section.

### Virtual Environments
For advanced users, you can (should) set up a virtual environment to isolate your python versions and modules from each other. Instantiate the environment with `python -m venv {nameOfEnv}` and run the `activate` script associated with your terminal (eg. Linux terminal - `activate.sh`; Powershell - `activate.ps1` etc)

### Modules
Once Python is installed and your environment is set up, you have to install the program's modules. Open a terminal in the WOIDS folder (eg. Powershell, Command Prompt, etc) and run `pip install -r requirements.txt`. Once that is done, you are all set to edit and compile the program as you see fit.

### Building
Once you're ready to build, run `pyinstaller --onefile gui.spec`. This will drop an exe called `WOIDS.exe` in the `dist` folder.


## Program Use
