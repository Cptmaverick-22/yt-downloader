import shutil
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

import yt_dlp

from config import get_download_dir


AUDIO_BITRATES = [128, 192, 256, 320]


def validate_youtube_url(url):
    """Validate supported YouTube URLs."""

    try:
        parsed = urlparse(url)
        hostname = (parsed.hostname or "").lower()

        return (
            parsed.scheme in ("http", "https")
            and (
                hostname == "youtu.be"
                or hostname == "youtube.com"
                or hostname.endswith(".youtube.com")
            )
        )

    except (ValueError, AttributeError):
        return False


def format_duration(seconds):
    """Convert seconds into HH:MM:SS."""

    if seconds is None:
        return "Unknown"

    hours, remainder = divmod(int(seconds), 3600)
    minutes, seconds = divmod(remainder, 60)

    return f"{hours:02}:{minutes:02}:{seconds:02}"


def format_file_size(size):
    """Convert bytes into a readable file size."""

    if size is None:
        return "Unknown"

    size = float(size)

    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024:
            return f"{size:.1f} {unit}"

        size /= 1024

    return f"{size:.1f} TB"


def get_video_info(url):
    """Retrieve basic video information."""

    if not validate_youtube_url(url):
        print("Invalid YouTube URL.")
        return None

    options = {
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        "skip_download": True,
    }

    try:
        print("\nFetching video information...", end=" ", flush=True)

        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=False)

        print("Done.")

        print(f"\nTitle: {info.get('title', 'Unknown')}")
        print(f"Duration: {format_duration(info.get('duration'))}")

        return info

    except Exception as error:
        print("\nUnable to retrieve video information.")
        show_download_error(error)
        return None


def get_available_video_qualities(info):
    """Find available MP4 video resolutions."""

    qualities = set()

    for video_format in info.get("formats", []):
        height = video_format.get("height")
        extension = video_format.get("ext")
        video_codec = video_format.get("vcodec")

        if (
            height
            and extension == "mp4"
            and video_codec
            and video_codec != "none"
        ):
            qualities.add(height)

    return sorted(qualities, reverse=True)


def display_formats(info):
    """Display available video resolutions."""

    qualities = get_available_video_qualities(info)

    if not qualities:
        print("\nNo supported MP4 resolutions found.")
        return []

    print("\nAvailable resolutions:")

    for index, quality in enumerate(qualities, start=1):
        print(f"{index}. {quality}p")

    return qualities




def show_download_progress(progress):
    """Display a clean, throttled, single-line progress bar."""

    status = progress.get("status")

    # Keep track of the previous display and refresh time.
    if not hasattr(show_download_progress, "last_update"):
        show_download_progress.last_update = 0

    if not hasattr(show_download_progress, "line_length"):
        show_download_progress.line_length = 0

    # Clear the progress line when a stream finishes.
    if status == "finished":
        if show_download_progress.line_length:
            sys.stdout.write(
                "\r" + " " * show_download_progress.line_length + "\r"
            )
            sys.stdout.flush()

            show_download_progress.line_length = 0

        return

    if status != "downloading":
        return

    # Avoid refreshing too frequently.
    now = time.monotonic()

    if now - show_download_progress.last_update < 0.25:
        return

    show_download_progress.last_update = now

    downloaded = progress.get("downloaded_bytes") or 0

    total = (
        progress.get("total_bytes")
        or progress.get("total_bytes_estimate")
    )

    speed = progress.get("speed")
    eta = progress.get("eta")

    bar_width = 16

    if total and total > 0:
        percentage = min(downloaded / total * 100, 100)
        filled = int(bar_width * percentage / 100)

        bar = "█" * filled + "░" * (bar_width - filled)

        progress_text = f"{percentage:5.1f}%"
        total_text = format_file_size(total)
    else:
        bar = "░" * bar_width
        progress_text = "  -- "
        total_text = "Unknown"

    downloaded_text = format_file_size(downloaded)

    speed_text = (
        f"{format_file_size(speed)}/s"
        if speed
        else "Calculating..."
    )

    eta_text = (
        format_duration(eta)
        if eta is not None
        else "Unknown"
    )

    message = (
        f"{progress_text} [{bar}] "
        f"{downloaded_text} / {total_text} "
        f"| {speed_text} | ETA {eta_text}"
    )

    # Keep the output within the terminal width.
    terminal_width = shutil.get_terminal_size(
        fallback=(100, 20)
    ).columns

    message = message[:max(1, terminal_width - 1)]

    # Overwrite the previous line without leaving old characters behind.
    sys.stdout.write(
        "\r" + message.ljust(show_download_progress.line_length)
    )

    sys.stdout.flush()

    show_download_progress.line_length = len(message)


def show_postprocessor_progress(progress):
    """Display conversion and merging messages."""

    if progress.get("status") != "started":
        return

    processor = progress.get("postprocessor", "")

    messages = {
        "Merger": "Merging video and audio...",
        "FFmpegExtractAudio": "Converting to MP3...",
    }

    message = messages.get(processor)

    if message:
        print(f"\n{message}")


def show_download_error(error):
    """Display a useful error instead of a long traceback."""

    message = str(error).strip()
    lowered = message.lower()

    if "private video" in lowered:
        print("This video is private or unavailable to your account.")

    elif "video unavailable" in lowered or "unavailable" in lowered:
        print("This video is unavailable.")

    elif "sign in" in lowered or "login required" in lowered:
        print("This video requires authentication.")

    elif "ffmpeg" in lowered or "postprocessing" in lowered:
        print("Media conversion failed. Check your FFmpeg installation.")

    elif "timed out" in lowered or "connection" in lowered:
        print("Network error. Check your internet connection and retry.")

    else:
        print(f"Download failed: {message[:300]}")


def get_output_directory(output_dir=None):
    """Resolve, validate, and create the destination directory."""

    directory = (
        Path(output_dir).expanduser().resolve()
        if output_dir is not None
        else get_download_dir()
    )

    if directory.exists() and not directory.is_dir():
        raise NotADirectoryError(
            f"Download location is not a directory: {directory}"
        )

    directory.mkdir(parents=True, exist_ok=True)

    return directory


def find_existing_download(output_dir, video_id, quality_label, extension):
    """Find an existing download using old or new filename formats."""

    suffixes = (
        f"[{quality_label}] [{video_id}].{extension}",
        f"[{video_id}] [{quality_label}].{extension}",
    )

    for file in output_dir.iterdir():
        if file.is_file() and file.name.endswith(suffixes):
            return file

    return None


def cleanup_incomplete_files(output_dir, video_id):
    """Remove incomplete temporary files for a specific video."""

    if output_dir is None or not video_id:
        return

    video_marker = f"[{video_id}]"
    temporary_suffixes = (".part", ".ytdl")

    removed_count = 0

    print("Cleaning up incomplete files...")

    try:
        for file in output_dir.iterdir():
            if not file.is_file():
                continue

            if video_marker not in file.name:
                continue

            is_temporary = (
                file.name.endswith(temporary_suffixes)
                or ".part-" in file.name
            )

            if not is_temporary:
                continue

            try:
                file.unlink()
                removed_count += 1
                print(f"Removed: {file.name}")

            except OSError as error:
                print(f"Could not remove {file.name}: {error}")

    except OSError as error:
        print(f"Cleanup failed: {error}")

    if removed_count:
        print(f"Removed {removed_count} incomplete file(s).")
    else:
        print("No incomplete files found.")


def download_video(url, selected_quality, output_dir=None, info=None):
    """Download and merge video and audio into an MP4 file."""

    if not validate_youtube_url(url):
        print("Invalid YouTube URL.")
        return False

    if (
        not isinstance(selected_quality, int)
        or isinstance(selected_quality, bool)
        or selected_quality <= 0
    ):
        print("Invalid video resolution.")
        return False

    if not shutil.which("ffmpeg"):
        print("FFmpeg is required but was not found.")
        return False

    resolved_output_dir = None
    video_id = None

    try:
        resolved_output_dir = get_output_directory(output_dir)

        if info is None:
            with yt_dlp.YoutubeDL({
                "quiet": True,
                "no_warnings": True,
                "noplaylist": True,
            }) as ydl:
                info = ydl.extract_info(url, download=False)

        video_id = info.get("id")

        if not video_id:
            print("Could not identify this video.")
            return False

        existing_file = find_existing_download(
            resolved_output_dir,
            video_id,
            f"{selected_quality}p",
            "mp4",
        )

        if existing_file:
            print("\nThis video has already been downloaded.")
            print(f"File: {existing_file.name}")
            return False

        print(f"\nDownloading MP4 ({selected_quality}p)...")
        print(f"Location: {resolved_output_dir}")

        options = {
            "format": (
                f"bestvideo[height={selected_quality}][ext=mp4]"
                f"+bestaudio[ext=m4a]/"
                f"best[height={selected_quality}][ext=mp4]"
            ),
            "merge_output_format": "mp4",
            "outtmpl": str(
                resolved_output_dir
                / "%(title).150B [%(height)sp] [%(id)s].%(ext)s"
            ),
            "trim_file_name": 180,
            "windowsfilenames": True,
            "noplaylist": True,
            "quiet": True,
            "no_warnings": True,
            "noprogress": True,
            "nooverwrites": True,
            "retries": 5,
            "continuedl": True,
            "progress_hooks": [show_download_progress],
            "postprocessor_hooks": [show_postprocessor_progress],
        }

        try:
            with yt_dlp.YoutubeDL(options) as ydl:
                ydl.download([url])

        finally:
            print()

        print("Download completed successfully!")
        return True

    except KeyboardInterrupt:
        print("\nDownload cancelled.")
        cleanup_incomplete_files(resolved_output_dir, video_id)
        return False

    except Exception as error:
        print()
        show_download_error(error)
        return False


def download_audio(url, bitrate, output_dir=None, info=None):
    """Download audio and convert it to MP3."""

    if not validate_youtube_url(url):
        print("Invalid YouTube URL.")
        return False

    if (
        not isinstance(bitrate, int)
        or isinstance(bitrate, bool)
        or bitrate not in AUDIO_BITRATES
    ):
        print("Unsupported audio bitrate.")
        return False

    if not shutil.which("ffmpeg"):
        print("FFmpeg is required but was not found.")
        return False

    resolved_output_dir = None
    video_id = None

    try:
        resolved_output_dir = get_output_directory(output_dir)

        if info is None:
            with yt_dlp.YoutubeDL({
                "quiet": True,
                "no_warnings": True,
                "noplaylist": True,
            }) as ydl:
                info = ydl.extract_info(url, download=False)

        video_id = info.get("id")

        if not video_id:
            print("Could not identify this video.")
            return False

        existing_file = find_existing_download(
            resolved_output_dir,
            video_id,
            f"{bitrate}kbps",
            "mp3",
        )

        if existing_file:
            print("\nThis audio has already been downloaded.")
            print(f"File: {existing_file.name}")
            return False

        print(f"\nDownloading MP3 ({bitrate} kbps)...")
        print(f"Location: {resolved_output_dir}")

        options = {
            "format": "bestaudio/best",
            "outtmpl": str(
                resolved_output_dir
                / f"%(title).150B [{bitrate}kbps] [%(id)s].%(ext)s"
            ),
            "trim_file_name": 180,
            "windowsfilenames": True,
            "noplaylist": True,
            "quiet": True,
            "no_warnings": True,
            "noprogress": True,
            "nooverwrites": True,
            "retries": 5,
            "continuedl": True,
            "progress_hooks": [show_download_progress],
            "postprocessor_hooks": [show_postprocessor_progress],
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": str(bitrate),
                }
            ],
        }

        try:
            with yt_dlp.YoutubeDL(options) as ydl:
                ydl.download([url])

        finally:
            print()

        print("Download completed successfully!")
        return True

    except KeyboardInterrupt:
        print("\nDownload cancelled.")
        cleanup_incomplete_files(resolved_output_dir, video_id)
        return False

    except Exception as error:
        print()
        show_download_error(error)
        return False
