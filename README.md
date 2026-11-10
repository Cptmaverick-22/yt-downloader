# YT Downloader

A beginner-friendly, cross-platform command-line YouTube downloader built with Python and [yt-dlp](https://github.com/yt-dlp/yt-dlp).

Download videos as MP4 or extract audio as MP3 with selectable quality and bitrate.

**Current version:** 1.0

**Supported operating systems:** Windows 10/11 and Fedora Linux

---

## Table of Contents

1. [Features](#features)
2. [How It Works](#how-it-works)
3. [Requirements](#requirements)
4. [Installation on Windows](#installation-on-windows)
5. [Installation on Fedora Linux](#installation-on-fedora-linux)
6. [Download the Project](#download-the-project)
7. [Set Up the Application](#set-up-the-application)
8. [How to Use](#how-to-use)
9. [Download Location](#download-location)
10. [File Naming](#file-naming)
11. [Project Structure](#project-structure)
12. [Troubleshooting](#troubleshooting)
13. [Updating the Application](#updating-the-application)
14. [Uninstalling](#uninstalling)
15. [Legal Notice](#legal-notice)
16. [License](#license)

---

## Features

- Download videos in available resolutions, up to 2160p (4K) when supported by the source.
- Download audio as MP3 at 128, 192, 256, or 320 kbps.
- Display download progress, speed, and estimated remaining time.
- Merge separate video and audio streams using FFmpeg.
- Convert downloaded audio to MP3.
- Choose a custom download directory.
- Remember your preferred download directory.
- Detect duplicate downloads using the video ID, resolution, and bitrate.
- Cancel downloads using Ctrl+C.
- Clean up incomplete files after cancellation.
- Validate supported YouTube URLs.
- Support Windows and Fedora Linux.

## How It Works

YT Downloader uses four main technologies:

| Software | Purpose |
|---|---|
| Python | Runs the application |
| yt-dlp | Handles video and audio extraction |
| FFmpeg | Merges video/audio streams and converts audio |
| Deno | Provides a JavaScript runtime used by yt-dlp |

**Note:** Python, FFmpeg, and Deno are installed separately. The Python dependencies are installed through `requirements.txt`.

## Requirements

Make sure your computer has the following:

| Requirement | Minimum version |
|---|---|
| Python | 3.11 or newer |
| FFmpeg | Installed and available in PATH |
| FFprobe | Installed and available in PATH |
| Deno | 2.3.0 or newer |
| Internet connection | Required |

You do not need to install yt-dlp manually. It is installed through `requirements.txt`.

### What is requirements.txt?

This file contains the Python packages required by the application.

Its current content is:

```text
yt-dlp[default]
```

This installs yt-dlp and its default optional dependencies. It does not install Python, FFmpeg, or Deno.

---

# Installation on Windows

Follow these instructions on Windows 10 or Windows 11.

## Step 1: Install Python

1. Visit the [official Python website](https://www.python.org/downloads/windows/).
2. Download Python 3.11 or newer.
3. Run the installer.
4. Enable **Add python.exe to PATH** if the option is displayed.
5. Click **Install Now**.
6. Close and reopen Command Prompt (CMD).

### Verify Python

```cmd
python --version
py --version
```

Both commands should display an installed Python version.

If Windows opens the Microsoft Store instead of Python, check your Python installation and Windows App Execution Aliases settings.

## Step 2: Install Deno

Deno is a JavaScript runtime used by yt-dlp for certain YouTube extraction operations.

Open CMD and execute:

```cmd
winget install DenoLand.Deno
```

After installation, close and reopen CMD.

### Verify Deno

```cmd
deno --version
```

The command should display the installed version.

If Windows cannot find `deno`, check that its installation directory is available through PATH.

## Step 3: Install FFmpeg and FFprobe

FFmpeg is required for merging video and audio streams and converting audio into MP3. FFprobe is included in standard FFmpeg builds.

### Method 1: Install using WinGet (Recommended)

WinGet is the Windows Package Manager available on supported Windows 10 and Windows 11 installations.

1. Open CMD.
2. Check whether WinGet is available:

```cmd
winget --version
```

3. Install FFmpeg:

```cmd
winget install -e --id Gyan.FFmpeg
```

4. Wait for installation to finish.
5. Close and reopen CMD.

WinGet installs the FFmpeg build and handles its installation configuration.

### Verify FFmpeg and FFprobe

Execute:

```cmd
where ffmpeg
where ffprobe
```

Then check their versions:

```cmd
ffmpeg -version
ffprobe -version
```

Both executables should be found and display version information.

### Method 2: Manual Installation (Alternative)

If WinGet is unavailable or you prefer manual installation:

1. Visit [Gyan.dev FFmpeg Builds](https://www.gyan.dev/ffmpeg/builds/).
2. Download the **Release Essentials** build.
3. Extract the archive using a suitable archive utility.
4. Locate the extracted `bin` directory.
5. Confirm that it contains:

```text
ffmpeg.exe
ffprobe.exe
```

6. Copy the full path of the `bin` directory.
7. Add that directory to Windows PATH:

   - Open Windows Search.
   - Search for **Environment Variables**.
   - Select **Edit the system environment variables**.
   - Click **Environment Variables**.
   - Under your user variables, select `Path`.
   - Click **Edit**, then **New**.
   - Paste the FFmpeg `bin` directory path.
   - Save all changes.

8. Close and reopen CMD.

Verify the installation:

```cmd
ffmpeg -version
ffprobe -version
```

**Important:** Use either WinGet or the manual method. You do not need to install FFmpeg again if it is already installed and both commands work.

Gyan.dev is a third-party provider of Windows FFmpeg builds, not the official FFmpeg project itself.

---

# Installation on Fedora Linux

Follow these instructions on Fedora Linux.

## Step 1: Install Python and pip

Open Terminal and execute:

```bash
sudo dnf install python3 python3-pip
```

### Verify Python

```bash
python3 --version
```

## Step 2: Enable RPM Fusion and install FFmpeg

Fedora's default repositories may not provide the FFmpeg packages required by this application.

Enable the RPM Fusion Free repository:

```bash
sudo dnf install https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm
```

Then install FFmpeg:

```bash
sudo dnf install ffmpeg
```

### Verify FFmpeg installation

```bash
ffmpeg -version
ffprobe -version
```

Both commands should display version information.

For more information about RPM Fusion:

https://rpmfusion.org/Configuration

## Step 3: Install Deno

Deno is a JavaScript runtime used by yt-dlp for certain YouTube extraction operations.

Open Terminal and execute:

```bash
curl -fsSL https://deno.land/install.sh | sh
```

Follow any instructions displayed by the installer.

Close and reopen Terminal, then verify:

```bash
deno --version
```

### If Deno is not found

The Deno executable is commonly installed in:

```text
~/.deno/bin/
```

For Bash, add that directory to PATH:

```bash
echo 'export PATH="$HOME/.deno/bin:$PATH"' >> ~/.bashrc
```

Reload your shell configuration:

```bash
source ~/.bashrc
```

Verify again:

```bash
deno --version
```

---

# Download the Project

You can obtain YT Downloader in two ways.

## Method 1: Download ZIP (Recommended for beginners)

1. Visit the [GitHub repository](https://github.com/Cptmaverick-22/yt-downloader).
2. Click the green **Code** button.
3. Select **Download ZIP**.
4. Extract the downloaded archive.
5. Open the extracted `yt-downloader` folder.

## Method 2: Clone using Git

If Git is installed, open a terminal and execute:

```bash
git clone https://github.com/Cptmaverick-22/yt-downloader.git
```

Then open the project directory:

```bash
cd yt-downloader
```

---

# Set Up the Application

After downloading or cloning the project, follow the instructions for your operating system.

## Windows (Command Prompt)

Open CMD inside the `yt-downloader` directory.

### Step 1: Create a virtual environment

```cmd
py -3 -m venv .venv
```

A virtual environment keeps this application's Python dependencies separate from other projects.

### Step 2: Activate the virtual environment

```cmd
.venv\Scripts\activate
```

Your CMD prompt should now begin with:

```text
(.venv)
```

### Step 3: Upgrade pip

```cmd
python -m pip install --upgrade pip
```

### Step 4: Install dependencies

```cmd
python -m pip install -r requirements.txt
```

Wait until the installation finishes.

## Fedora Linux (Terminal)

Open Terminal inside the `yt-downloader` directory.

### Step 1: Create a virtual environment

```bash
python3 -m venv .venv
```

### Step 2: Activate it

```bash
source .venv/bin/activate
```

Your terminal prompt should now display:

```text
(.venv)
```

### Step 3: Upgrade pip

```bash
python -m pip install --upgrade pip
```

### Step 4: Install dependencies

```bash
python -m pip install -r requirements.txt
```

**Important:** Create a separate virtual environment on each operating system. Never copy a Windows `.venv` folder to Linux or vice versa.

---

# How to Use

Once installation is complete and the virtual environment is activated, execute:

```bash
python main.py
```

The application displays its main menu:

```text
YT Downloader v1.0

1. Download Video
2. Download Audio (MP3)
3. Change Download Location
4. Exit
```

Choose an option by entering its corresponding number.

## Download a Video

1. Select `1` from the main menu.
2. Paste a supported YouTube video URL.
3. Select an available video resolution.
4. Wait for downloading and merging to finish.

Example:

```text
YouTube URL: https://www.youtube.com/watch?v=VIDEO_ID
```

The application displays download progress, speed, and estimated remaining time.

Available resolutions depend on the source video.

## Download Audio (MP3)

1. Select `2` from the main menu.
2. Paste a supported YouTube URL.
3. Choose the desired audio bitrate.

Available bitrates:

- 128 kbps
- 192 kbps
- 256 kbps
- 320 kbps

The application downloads and converts the audio into MP3 format.

## Change Download Location

1. Select `3` from the main menu.
2. Enter your preferred download directory.
3. The application creates the directory if necessary.
4. Your selected location is saved for future runs.

## Exit the Application

Select `4` from the main menu.

---

# Download Location

By default, downloaded files are saved inside:

```text
yt-downloader/downloads/
```

You can change this directory through the application menu.

Your preferred location is stored in:

```text
settings.json
```

This file is generated automatically and is specific to your computer.

---

# File Naming

YT Downloader includes the video ID in downloaded filenames to help identify videos and detect duplicates.

### Video filename example

```text
Video Name [1080p] [VIDEO_ID].mp4
```

### Audio filename example

```text
Audio Name [320kbps] [VIDEO_ID].mp3
```

This makes it easier to identify downloaded quality and distinguish different versions of the same video.

---

# Project Structure

After installation and first use, the project directory may look like this:

```text
yt-downloader/
│
├── main.py
├── downloader.py
├── config.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
│
├── .venv/              # Created during installation
├── downloads/          # Created for downloaded media
├── settings.json       # Created for application settings
└── __pycache__/        # Generated by Python
```

### Main Python files

| File | Purpose |
|---|---|
| `main.py` | Application menu and user interaction |
| `downloader.py` | Downloading, conversion, and progress handling |
| `config.py` | Download directory and settings management |
| `requirements.txt` | Python package dependencies |
| `README.md` | Installation and usage documentation |
| `LICENSE` | MIT License |

---

# Troubleshooting

## 1. Python is not recognized

Possible Windows message:

```text
'python' is not recognized as an internal or external command
```

**Solution:**

- Install Python from https://www.python.org/downloads/.
- Enable **Add python.exe to PATH** during installation.
- Restart CMD.
- Try `py --version` if `python` is unavailable.

## 2. FFmpeg was not found

**Possible cause:** FFmpeg is not installed or its executable directory is missing from PATH.

**Solution:**

- Install FFmpeg using WinGet or the manual method on Windows.
- Install FFmpeg through RPM Fusion on Fedora.
- Make sure the directory containing `ffmpeg` and `ffprobe` is available through PATH.
- Restart the terminal.

Verify:

```bash
ffmpeg -version
ffprobe -version
```

On Windows, you can also check the executable locations:

```cmd
where ffmpeg
where ffprobe
```

## 3. Deno was not found

**Possible cause:** Deno is not installed or is unavailable through PATH.

**Solution:**

- Install Deno.
- Verify its PATH configuration.
- Restart the terminal.

Verify:

```bash
deno --version
```

## 4. No module named yt_dlp

**Possible cause:** Project dependencies have not been installed or the virtual environment is not activated.

**Solution:**

Activate the virtual environment and execute:

```bash
python -m pip install -r requirements.txt
```

## 5. Virtual environment activation fails on Windows

Make sure you are using Command Prompt (CMD).

Execute:

```cmd
.venv\Scripts\activate
```

If you are using PowerShell, its activation command is different and may be restricted by your execution policy.

## 6. YouTube download fails

Check the following:

- Your internet connection is working.
- The YouTube URL is supported.
- The video is available and accessible.
- FFmpeg and Deno are installed.
- yt-dlp is up to date.

Update yt-dlp inside the activated virtual environment:

```bash
python -m pip install --upgrade "yt-dlp[default]"
```

Some videos may have restrictions that prevent downloading. The application cannot bypass every restriction.

## 7. Download was interrupted

Pressing Ctrl+C cancels the current download.

The application attempts to clean up incomplete download files. If a download is interrupted by a system crash or power failure, check the download directory for leftover temporary files.

---

# Updating the Application

## If you cloned the repository using Git

Open the project directory and execute:

```bash
git pull
```

Activate the virtual environment and update dependencies:

```bash
python -m pip install --upgrade -r requirements.txt
```

Then start the application:

```bash
python main.py
```

## If you downloaded a ZIP

Download the latest ZIP from:

https://github.com/Cptmaverick-22/yt-downloader

Extract the new version and follow the setup instructions if required.

Back up your `settings.json` and downloaded files before replacing your existing folder.

---

# Uninstalling

To remove YT Downloader:

1. Close the application.
2. Delete the extracted `yt-downloader` project folder.
3. If you installed Python, FFmpeg, or Deno only for this application, you may uninstall them separately.

**Warning:** Deleting the project folder also deletes its local downloads and settings if they are stored inside that folder. Back up anything you want to keep first.

---

# Legal Notice

Use this application only to download content that you own, have permission to download, or are otherwise legally authorized to download.

Respect copyright laws and YouTube's Terms of Service.

This project does not provide permission to download copyrighted material without authorization.

YT Downloader is an independent project and is not affiliated with, endorsed by, or officially associated with YouTube.

---

# License

This project is licensed under the MIT License.

See the [LICENSE](LICENSE) file for details.

---

# Author

**Cptmaverick-22**

GitHub Repository:

https://github.com/Cptmaverick-22/yt-downloader

**YT Downloader v1.0**