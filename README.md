# Film Technology 2 — Installation on Macs (MacOS) or PCs (Windows/Linux) outside Room 043

You need three things: **Visual Studio Code**, **Python 3.13** and a **virtual environment** that holds the Python packages for this course.

A virtual environment is simply a folder called `.venv` inside the course folder. Everything we install ends up in that folder and nothing else on your computer is changed. If something goes wrong, delete the folder and start again.

The setup has to be done once and takes about 10 minutes.

## 1. Install Visual Studio Code

Download and install it from https://code.visualstudio.com

## 2. Get the course files and open them in VS Code

1. On https://github.com/janfroehlich/hdm-filmtech-2 click the green **Code** button, choose **Download ZIP** and unzip the file.
2. In VS Code choose **File → Open Folder…** and select the unzipped folder. Open the folder, not a single file. If VS Code asks whether you trust the authors, answer **Yes**.
3. VS Code offers to install the recommended extensions: click **Install**. If it does not ask, open the Extensions view (the icon with the four squares on the left) and install **Python** and **Jupyter**, both from Microsoft.

## 3. Install Python 3.13

**Install Python 3.13, not the newest version.** The package we use to read camera RAW files (`rawpy`) is not available for Python 3.15 or later yet.

- **Windows:** in VS Code open **Terminal → New Terminal**, type the following line and press Enter:

      winget install -e --id Python.Python.3.13

  Alternatively go to https://www.python.org/downloads/windows/, look for the newest **Python 3.13.x** entry that offers a *Windows installer (64-bit)* and run it.

- **macOS:** go to https://www.python.org/downloads/macos/, look for the newest **Python 3.13.x** entry that offers a *macOS 64-bit universal2 installer* and run it. If you use Homebrew, `brew install python@3.13` does the same.

- **Linux:** install `python3.13` and `python3.13-venv` with your package manager, or use the uv alternative below.

Afterwards **quit and restart VS Code** so that it finds the new Python.

## 4. Create the virtual environment

1. Open the Command Palette with **Ctrl+Shift+P** (macOS: **Cmd+Shift+P**).
2. Type **Python: Create Environment** and press Enter.
3. Choose **Venv**.
4. Choose **Python 3.13** from the list.
5. If asked for a name, keep `.venv`.
6. When asked which dependencies to install, tick **requirements.txt** and confirm with **OK**.

VS Code now creates the folder `.venv` and downloads the packages into it. This takes a few minutes and needs about 1 GB of disk space.

## 5. Select the environment in the notebook

Open `B_FT2_00_Introduction_to_Python_student.ipynb`, click **Select Kernel** at the top right of the notebook, choose **Python Environments…** and then **.venv (Python 3.13.x)**.

You have to do this once for every notebook of the course. VS Code remembers your choice.

## 6. Check the installation

Run the first code cell of the notebook: click into it and press **Shift+Enter**. It should end with *Everything is ready*.

<details>
<summary><b>Alternative to steps 3 and 4: everything in the VS Code terminal with uv</b></summary>

[uv](https://docs.astral.sh/uv/) is a small tool that downloads Python 3.13 by itself and creates the environment. You do not need to install Python separately and you do not need administrator rights.

1. In VS Code open **Terminal → New Terminal** and install uv:

   - Windows: `winget install -e --id astral-sh.uv`
   - macOS and Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`

2. Close the terminal, open a new one and run these two lines:

       uv venv --python 3.13 --seed
       uv pip install -r requirements.txt

3. Continue with step 5.

</details>

<details>
<summary><b>If something does not work</b></summary>

- **Python 3.13 does not show up in the list in step 4:** quit and restart VS Code. If it is still missing, Python 3.13 is not installed, so repeat step 3.

- **`No matching distribution found for rawpy`** or **`Could not find a version that satisfies the requirement ...`:** the environment was created with the wrong Python version. Delete the folder `.venv` and repeat step 4 with Python 3.13.

- **`ModuleNotFoundError: No module named ...` when you run a cell:** the notebook is not using `.venv`. Repeat step 5, then run the check cell at the top of the notebook.

- **VS Code asks to install `ipykernel`:** answer **Install**, then run the check cell at the top of the notebook. It tells you what else is missing.

- **Saving a plot as PDF fails with "Kaleido requires Google Chrome":** install Google Chrome, or run `plotly_get_chrome` once in the VS Code terminal. Only `fig.write_image(...)` needs this, everything else works without it.

- **Start again from scratch:** delete the folder `.venv` and repeat step 4.

- **Create the environment by hand** in the VS Code terminal. This does the same as step 4.

  Windows:

      py -3.13 -m venv .venv
      .venv\Scripts\python -m pip install -r requirements.txt

  macOS and Linux:

      python3.13 -m venv .venv
      .venv/bin/python -m pip install -r requirements.txt

</details>
