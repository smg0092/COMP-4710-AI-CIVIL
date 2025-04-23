# Civil AI Prediction App (Windows)

This is a standalone desktop application for running rooftop damage predictions using a pre-trained AI model, provided through a graphical user interface (GUI).

---

## Requirements

Before running the application, please ensure the following are installed:

### System Requirements
- Windows 10 or newer
- Internet connection (to install Python dependencies)

### Software Requirements
- **Python 3.10+**  
  Download: https://www.python.org/downloads/  
  Make sure to check "Add Python to PATH" during installation.

- **MATLAB Runtime**  
  Required to run the compiled `.exe` file.  
  Download: https://www.mathworks.com/products/compiler/matlab-runtime.html  
  Use the version that matches the one used to compile `RC_predictionFunction.exe`.

---

## Installation and Usage

1. Unzip the project folder anywhere on your computer (e.g., Desktop or Documents).
2. Double-click `run_app.bat`.
   - This script will:
     - Check that Python is available
     - Ensure pip is installed
     - Install required dependencies (`Pillow`)
     - Launch the GUI
3. Inside the application:
   - Select a folder of input images
   - Choose an output folder
   - Run the prediction, which uses a compiled MATLAB model

---

## Project Files

| File/Folder                        | Description                                      |
|------------------------------------|--------------------------------------------------|
| `ViewForCivilAI_GUI_Controller.py` | Main script that runs the application            |
| `ViewForCivilAI_GUI.py`            | GUI layout (generated using PAGE)                |
| `ViewForCivilAI_GUI_support.py`    | PAGE GUI launcher support                        |
| `RC_predictionFunction.exe`        | Compiled MATLAB prediction function              |
| `RCDetection_v1.mat`               | Pre-trained model data file                      |
| `requirements.txt`                 | Python package list (`Pillow`)                   |
| `run_app.bat`                      | Launcher script that handles setup and execution |
| `themes/default.tcl`               | GUI theme styling file                           |

---

## Troubleshooting

- If you see "`python` is not recognized as an internal or external command", Python is either not installed or not added to your system PATH.
- If the prediction fails to run, ensure the correct version of MATLAB Runtime is installed.
- If nothing happens when double-clicking `run_app.bat`, try running it from Command Prompt to see the output.

---

## Support

If you experience any issues or have questions, please reach out to the development team for assistance.
