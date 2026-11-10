# YT Downloader

A lightweight Windows command-line application for downloading YouTube videos and audio. Download videos as MP4 or extract audio as MP3 using a simple menu-driven interface.

**Current Version:** 1.0  
**Platform:** Windows 64-bit

---

## Download

### [Download YT Downloader v1.0](https://github.com/Cptmaverick-22/yt-downloader/releases/latest)

Download the Windows installer from the official GitHub Releases page.

**Installer:** `YT-Downloader-Setup.exe`

### Installation

1. Visit the [YT Downloader Releases page](https://github.com/Cptmaverick-22/yt-downloader/releases).
2. Download `YT-Downloader-Setup.exe`.
3. Run the installer.
4. Follow the installation instructions.
5. Launch **YT Downloader** from the Start Menu.

That's it! No separate Python, FFmpeg, Deno, or other dependency installation is required.

---

## Features

- Download YouTube videos in available resolutions, up to 2160p (4K).
- Download audio in MP3 format.
- Select audio bitrates: 128, 192, 256, or 320 kbps.
- Display download progress, speed, and estimated time remaining.
- Automatically merge video and audio streams.
- Choose a custom download directory.
- Remember the selected download location between sessions.
- Detect duplicate downloads.
- Cancel downloads using Ctrl+C.
- Automatically clean up incomplete files after cancellation.
- Bundled FFmpeg and Deno runtimes.
- Simple menu-driven command-line interface.

---

## Application Menu

When you launch YT Downloader, you will see the following menu:

```text
Welcome to YT Downloader!

YT Downloader v1.0
----------------------------
1. Download Video
2. Download Audio (MP3)
3. Change Download Location
4. Exit
```

Follow the on-screen instructions to download videos or audio.

---

## How to Use

### Download Video

1. Launch YT Downloader.
2. Select **Download Video**.
3. Paste the YouTube video URL.
4. Select your preferred available resolution.
5. Wait for the download to finish.

Videos are saved in MP4 format.

Example filename:

```text
Video Name [1080p] [VIDEO_ID].mp4
```

### Download Audio (MP3)

1. Launch YT Downloader.
2. Select **Download Audio (MP3)**.
3. Paste the YouTube video URL.
4. Select your preferred audio bitrate.
5. Wait for the download and conversion to finish.

Audio is saved in MP3 format.

Example filename:

```text
Audio Name [320kbps] [VIDEO_ID].mp3
```

### Change Download Location

1. Select **Change Download Location** from the main menu.
2. Enter your preferred download directory.
3. Confirm the new location.

The application creates the directory if necessary and remembers your selected location for future sessions.

---

## System Requirements

| Requirement | Details |
|---|---|
| Operating System | Windows |
| Architecture | 64-bit |
| Internet Connection | Required |
| Python | Not required for installed application |
| FFmpeg | Bundled |
| Deno | Bundled |

---

## Project Structure

The repository contains the application source code and Windows packaging files.

```text
yt-downloader/
│
├── main.py
├── downloader.py
├── config.py
├── requirements.txt
│
├── build_windows.bat
├── installer.iss
│
├── LICENSE
├── THIRD_PARTY_NOTICES.md
├── README.md
├── .gitignore
│
└── licenses/
    ├── BROTLI-LICENSE.txt
    ├── CERTIFI-LICENSE.txt
    ├── CHARSET-NORMALIZER-LICENSE.txt
    ├── PYCRYPTODOMEX-LICENSE.txt
    ├── PYTHON-LICENSE.txt
    └── OPENSSL-LICENSE.txt
```

Generated build files, application binaries, and installer output are excluded from the source repository.

---

## Building from Source

Developers who want to modify or build the application can use the source code in this repository.

### 1. Clone the repository

```cmd
git clone https://github.com/Cptmaverick-22/yt-downloader.git
```

Open the project directory:

```cmd
cd yt-downloader
```

### 2. Create a virtual environment

```cmd
py -3 -m venv .venv
```

Activate it:

```cmd
.venv\Scripts\activate
```

### 3. Install dependencies

```cmd
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Run the application from source

```cmd
python main.py
```

### 5. Build the Windows application

The project includes a Windows build script:

```cmd
build_windows.bat
```

The build process uses PyInstaller to package the application and bundles the required runtime files.

### 6. Create the installer

The project uses Inno Setup to generate the Windows installer.

Open `installer.iss` using Inno Setup Compiler or compile it using:

```cmd
ISCC.exe installer.iss
```

The generated installer is placed in the `installer_output` directory.

---

## Troubleshooting

### Application does not launch

- Make sure the installation completed successfully.
- Try launching YT Downloader from the Start Menu.
- If the problem persists, reinstall the application.

### Download fails

- Check your internet connection.
- Verify that the YouTube URL is valid.
- Make sure the video is publicly accessible.
- Try again later if YouTube is temporarily unavailable.

### Download location problems

- Make sure the selected directory is accessible.
- Verify that you have permission to write to the selected directory.

### Incomplete downloads

If a download is cancelled, the application attempts to remove incomplete temporary files automatically.

---

## Legal Notice

YT Downloader is intended for downloading content that you own, have permission to download, or are otherwise legally authorized to download.

Users are responsible for complying with applicable copyright laws and YouTube's Terms of Service.

This project is not affiliated with, endorsed by, or officially associated with YouTube or Google.

---

## Technology Stack

- **Python** — Application logic and command-line interface.
- **yt-dlp** — Video and audio downloading.
- **FFmpeg** — Video/audio merging and audio conversion.
- **Deno** — JavaScript runtime used by yt-dlp for YouTube support.
- **PyInstaller** — Application packaging.
- **Inno Setup** — Windows installer creation.

---

## License

This project is licensed under the MIT License.

See the [LICENSE](LICENSE) file for details.

Third-party software acknowledgements and licence information are available in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

---

## Release

**YT Downloader v1.0 — Initial Release**

[View Releases](https://github.com/Cptmaverick-22/yt-downloader/releases)

Thank you for using YT Downloader!
