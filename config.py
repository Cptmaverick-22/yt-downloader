
import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

DEFAULT_DOWNLOAD_DIR = BASE_DIR / "downloads"
SETTINGS_FILE = BASE_DIR / "settings.json"

APP_NAME = "YT Downloader"
APP_VERSION = "1.0"


def get_download_dir():
    """Load the saved directory, falling back to the default."""

    try:
        if SETTINGS_FILE.exists():
            settings = json.loads(
                SETTINGS_FILE.read_text(encoding="utf-8")
            )

            if not isinstance(settings, dict):
                raise ValueError("Settings must contain a JSON object.")

            saved_path = settings.get("download_dir")

            if isinstance(saved_path, str) and saved_path.strip():
                download_dir = Path(saved_path).expanduser()
            else:
                download_dir = DEFAULT_DOWNLOAD_DIR
        else:
            download_dir = DEFAULT_DOWNLOAD_DIR

        download_dir = download_dir.resolve()

        if download_dir.exists() and not download_dir.is_dir():
            raise ValueError("Saved download path is not a directory.")

        download_dir.mkdir(parents=True, exist_ok=True)

        return download_dir

    except (OSError, ValueError, TypeError, json.JSONDecodeError) as error:
        print(f"\nWarning: Could not load saved download location: {error}")
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

    temporary_file = SETTINGS_FILE.with_suffix(".tmp")

    settings = {
        "download_dir": str(download_dir)
    }

    temporary_file.write_text(
        json.dumps(settings, indent=4),
        encoding="utf-8"
    )

    temporary_file.replace(SETTINGS_FILE)

    return download_dir


DOWNLOAD_DIR = get_download_dir()
