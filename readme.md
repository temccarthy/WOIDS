# WSP Optimized Inspection Data System (WOIDS)
A PDF report generator made for the use of WSP.

## Compliation
WOIDS must be compiled into an executable (exe) in order to be used on WSP's work computers. To make changes to the PDF, 
you must update the Python code. Follow these steps to download the code and compile it yourself. Otherwise, skip to the 
Program Use section

### Code
Download WOIDS by either using Git clone (advanced), or download a zip of all the files. Unzip the folder to get started.

### Python
WOIDS is built in Python 3.9, which you can download [here](https://www.python.org/downloads/). Beginners should skip 
down the Modules section.

### Virtual Environments
For advanced users, you can (should) set up a virtual environment to isolate your python versions and modules from each 
other. Instantiate the environment with `python -m venv {nameOfEnv}` and run the `activate` script associated with your 
terminal (eg. Linux terminal - `activate.sh`; Powershell - `activate.ps1` etc)

### Modules
Once Python is installed and your environment is set up, you have to install WOIDS's modules. Open a terminal in the 
WOIDS folder (eg. Powershell, Command Prompt, etc) and run `pip install -r requirements.txt`. Once that is done, you are 
all set to edit and compile the program as you see fit.

### Building
Once you're ready to build, run `pyinstaller --onefile gui.spec`. This will drop an exe called `WOIDS.exe` in the `dist` 
folder.

## Program Use
### Formatting
WOIDS uses a very specific format for linking spreadsheet entries to pictures. A template spreadsheet can be generated 
by running the program and clicking the `Generate Template` button. You can also find it in the `resources` folder if 
you have downloaded the code. 

#### Spreadsheet
In the spreadsheet, you'll find 1 sheet about general report information and 5 sheets for deficiencies. Fill out these 
sheets. For WOIDS to match pictures to entries, the Discipline, Number, and ID columns must be filled in properly.

![Example sheet](https://github.com/temccarthy/WOIDS/blob/dev/docs/id%20picture.png?raw=true)

Match the Discipline letter to the sheet that it's in (Architectural - A, Electrical - E, etc), and increment the Number 
value as more entries are added. 

#### Image Names
Images should be renamed according to which discipline they belong. In the case of WOIDS, you should use the mass rename
feature in Windows to speed up the renaming process. Select all your photos, right click and click rename. 

![Image renaming](https://github.com/temccarthy/WOIDS/blob/dev/docs/Images.png?raw=true)

You only need to rename them to one letter (A, C, E, S, or M) - the numbers in parentheses will automatically fill in. 
In the end, your folder should look like this:

![Folder structure](https://github.com/temccarthy/WOIDS/blob/dev/docs/final%20folder.png?raw=true)

Make sure your photos and the spreadsheet are all in the **same folder**.

### Execution
To run the program, simply select your spreadsheet and click Generate Report. The program will automatically run the 
Check Files function so you don't have to. If successful, the program will generate the PDF and place it in the same 
folder as the images. 

#### Crashes
If WOIDS crashes, the likely cause is that the spreadsheet has not been filled out properly. Please make sure the 
spreadsheet is filled out correctly and try running the program again. If the problem still persists, please reach out.