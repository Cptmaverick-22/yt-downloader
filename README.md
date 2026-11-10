# YT Downloader

A cross-platform command-line YouTube downloader built with Python and [yt-dlp](https://github.com/yt-dlp/yt-dlp). Download videos as MP4 or extract audio as MP3.

## Features

- Download YouTube videos in available resolutions, up to 2160p (4K).
- Download audio as MP3 at 128, 192, 256, or 320 kbps.
- Display download progress, speed, and estimated time remaining.
- Merge video and audio streams using FFmpeg.
- Convert audio to MP3 using FFmpeg.
- Choose a custom download directory.
- Remember the selected download directory between runs.
- Detect duplicate downloads using the YouTube video ID, resolution, and audio bitrate.
- Handle download cancellation with Ctrl+C.
- Clean up incomplete files after cancellation.
- Validate supported YouTube URLs.
- Support Windows and Linux.

## Requirements

Install the following software before running the application:

| Requirement | Minimum / recommendation |
|---|---|
| Python | 3.11 or newer |
| FFmpeg | A working installation available on PATH |
| FFprobe | Included with FFmpeg |
| Deno | 2.3.0 or newer |
| Internet connection | Required |

**Note:** FFmpeg and Deno must be accessible from your system's PATH. The Python dependencies are installed separately inside the virtual environment.

## Installation

### 1. Clone or download the project

Download this repository and open a terminal in the project directory.

### 2. Install prerequisites

#### Fedora Linux

Install Python and FFmpeg:

```bash
sudo dnf install python3 python3-pip ffmpeg
```

If FFmpeg is unavailable in your enabled repositories, follow the [RPM Fusion installation instructions](https://rpmfusion.org/Configuration).

Install Deno:

```bash
curl -fsSL https://deno.land/install.sh | sh
```

Add Deno to PATH if it is not already available:

```bash
echo 'export PATH="$HOME/.deno/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

#### Windows

Install Python 3.11 or newer. During installation, enable the option to add Python to PATH.

Install Deno from CMD using WinGet:

```cmd
winget install DenoLand.Deno
```

Install FFmpeg using a Windows build from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) or another trusted source. Extract it and add the folder containing `ffmpeg.exe` and `ffprobe.exe` to your system PATH.

Close and reopen CMD after installing software or changing PATH.

### 3. Verify prerequisites

Run these commands to confirm the installations:

**Fedora:**

```bash
python3 --version
ffmpeg -version
ffprobe -version
deno --version
```

**Windows CMD:**

```cmd
python --version
ffmpeg -version
ffprobe -version
deno --version
```

Make sure each command runs successfully before continuing.

### 4. Create a virtual environment

**Fedora:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows CMD:**

```cmd
py -3 -m venv .venv
.venv\Scripts\activate
```

The terminal should now show `(.venv)` at the beginning of the prompt.

> Create a separate virtual environment on each operating system. Do not copy the `.venv` directory between Windows and Linux.

### 5. Install Python dependencies

With the virtual environment activated, run:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Usage

Make sure the virtual environment is activated, then run:

```bash
python main.py
```

The application displays the following menu:

```text
YT Downloader v1.0

1. Download Video
2. Download Audio (MP3)
3. Change Download Location
4. Exit
```

Follow the on-screen instructions to download a video or audio file.

### Video download

1. Select **Download Video**.
2. Paste a supported YouTube URL.
3. Select an available video resolution.
4. Wait for the download and merging process to finish.

Example filename:

```text
Video Name [1080p] [VIDEO_ID].mp4
```

### Audio download

1. Select **Download Audio (MP3)**.
2. Paste a supported YouTube URL.
3. Select an audio bitrate: 128, 192, 256, or 320 kbps.
4. Wait for the download and conversion process to finish.

Example filename:

```text
Audio Name [320kbps] [VIDEO_ID].mp3
```

### Change download location

Select **Change Download Location** from the main menu and enter the desired directory.

The application creates the directory if necessary and saves the selected location for future runs.

## Project Structure

```text
yt-downloader/
│
├── main.py
├── downloader.py
├── config.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── downloads/       # Created automatically
├── settings.json    # Created automatically
└── .venv/           # Python virtual environment
```

The `downloads/`, `settings.json`, and `.venv/` entries are generated locally and should not be committed to Git.

## Troubleshooting

### FFmpeg not found

Make sure FFmpeg and FFprobe are installed and their executable directory is included in PATH.

Verify with:

```bash
ffmpeg -version
ffprobe -version
```

### Deno not found

Make sure Deno is installed and available in PATH.

Verify with:

```bash
deno --version
```

Restart the terminal after changing PATH.

### Python dependency errors

Activate the virtual environment and reinstall the dependencies:

```bash
python -m pip install -r requirements.txt
```

### YouTube download errors

Make sure:

- The URL is valid and supported.
- Your internet connection is working.
- yt-dlp and its dependencies are up to date.
- Deno is installed and accessible.

To update yt-dlp inside the virtual environment:

```bash
python -m pip install --upgrade "yt-dlp[default]"
```

## Legal Notice

Use this application only to download content that you own, have permission to download, or are otherwise legally authorized to download.

Respect copyright laws and YouTube's Terms of Service.

## Technology Stack

- **Python** — Application logic and command-line interface.
- **yt-dlp** — Video and audio extraction and downloading.
- **FFmpeg** — Video/audio merging and audio conversion.
- **Deno** — JavaScript runtime used by yt-dlp for YouTube support.

## Version

**YT Downloader v1.0**

## License

No license has been specified yet. All rights are reserved by default unless a license is added to this project.