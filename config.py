
import json
import os
import sys
from pathlib import Path


APP_NAME = "YT Downloader"
APP_VERSION = "1.0"


# Detect whether the application is running as a packaged executable.
IS_FROZEN = getattr(sys, "frozen", False)

if IS_FROZEN:
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    BASE_DIR = Path(__file__).resolve().parent


def get_config_directory():
    """Return the appropriate user-specific configuration directory."""

    if sys.platform == "win32":
        app_data = Path(
            os.environ.get(
                "APPDATA",
                Path.home() / "AppData" / "Roaming"
            )
        )
        return app_data / APP_NAME

    if sys.platform == "darwin":
        return (
            Path.home()
            / "Library"
            / "Application Support"
            / APP_NAME
        )

    config_home = Path(
        os.environ.get(
            "XDG_CONFIG_HOME",
            Path.home() / ".config"
        )
    )

    return config_home / "yt-downloader"


if IS_FROZEN:
    CONFIG_DIR = get_config_directory()
    SETTINGS_FILE = CONFIG_DIR / "settings.json"
    DEFAULT_DOWNLOAD_DIR = (
        Path.home() / "Downloads" / APP_NAME
    )
else:
    # Preserve the existing development environment.
    SETTINGS_FILE = BASE_DIR / "settings.json"
    DEFAULT_DOWNLOAD_DIR = BASE_DIR / "downloads"


# Used to migrate settings from an older source installation.
LEGACY_SETTINGS_FILE = BASE_DIR / "settings.json"


def _read_settings(path):
    """Read and validate a settings JSON file."""

    settings = json.loads(path.read_text(encoding="utf-8"))

    if not isinstance(settings, dict):
        raise ValueError("Settings must contain a JSON object.")

    return settings


def _write_settings(settings):
    """Write settings safely using an atomic replacement."""

    SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)

    temporary_file = SETTINGS_FILE.with_name(
        SETTINGS_FILE.name + ".tmp"
    )

    try:
        temporary_file.write_text(
            json.dumps(settings, indent=4),
            encoding="utf-8"
        )

        temporary_file.replace(SETTINGS_FILE)

    finally:
        if temporary_file.exists():
            temporary_file.unlink()


def get_download_dir():
    """Load the saved directory, falling back to the default."""

    try:
        if SETTINGS_FILE.exists():
            settings = _read_settings(SETTINGS_FILE)

        elif (
            IS_FROZEN
            and LEGACY_SETTINGS_FILE != SETTINGS_FILE
            and LEGACY_SETTINGS_FILE.exists()
        ):
            # Migrate settings from an older installation.
            settings = _read_settings(LEGACY_SETTINGS_FILE)
            _write_settings(settings)

        else:
            settings = {}

        saved_path = settings.get("download_dir")

        if isinstance(saved_path, str) and saved_path.strip():
            download_dir = Path(saved_path).expanduser()
        else:
            download_dir = DEFAULT_DOWNLOAD_DIR

        download_dir = download_dir.resolve()

        if download_dir.exists() and not download_dir.is_dir():
            raise ValueError(
                "Saved download path is not a directory."
            )

        download_dir.mkdir(parents=True, exist_ok=True)

        return download_dir

    except (OSError, ValueError, TypeError, json.JSONDecodeError) as error:
        print(
            f"\nWarning: Could not load saved download location: {error}"
        )
        print("Using the default downloads directory.")

        DEFAULT_DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

        return DEFAULT_DOWNLOAD_DIR.resolve()


def save_download_dir(path):
    """Validate and save the preferred download directory."""

    if not str(path).strip():
        raise ValueError("Directory cannot be empty.")

    download_dir = Path(path).expanduser().resolve()

    if download_dir.exists() and not download_dir.is_dir():
        raise ValueError("The selected path is not a directory.")

    download_dir.mkdir(parents=True, exist_ok=True)

    settings = {
        "download_dir": str(download_dir)
    }

    _write_settings(settings)

    return download_dir


DOWNLOAD_DIR = get_download_dir()
