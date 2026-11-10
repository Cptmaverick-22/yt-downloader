
from config import (
    APP_NAME,
    APP_VERSION,
    get_download_dir,
    save_download_dir,
)

from downloader import (
    get_video_info,
    display_formats,
    download_video,
    download_audio,
)


AUDIO_BITRATES = [128, 192, 256, 320]


def show_menu():
    print(f"\n{APP_NAME} v{APP_VERSION}")
    print("-" * 28)
    print("1. Download Video")
    print("2. Download Audio (MP3)")
    print("3. Change Download Location")
    print("4. Exit")


def select_option(options, label):
    while True:
        choice = input(
            f"\nSelect {label} (Q to cancel): "
        ).strip().lower()

        if choice == "q":
            return None

        if choice.isdigit():
            index = int(choice)

            if 1 <= index <= len(options):
                return options[index - 1]

        print("Invalid selection. Try again.")


def get_url():
    url = input("\nYouTube URL: ").strip()

    if not url:
        print("URL cannot be empty.")
        return None

    return url


def inspect_video():
    url = get_url()

    if not url:
        return

    info = get_video_info(url)

    if not info:
        return

    qualities = display_formats(info)

    if not qualities:
        return

    quality = select_option(qualities, "resolution")

    if quality is None:
        print("Cancelled.")
        return

    print(f"\nSelected: {quality}p MP4")

    if input("Start download? (y/n): ").strip().lower() == "y":
        download_video(url, quality, info=info)
    else:
        print("Cancelled.")


def inspect_audio():
    url = get_url()

    if not url:
        return

    info = get_video_info(url)

    if not info:
        return

    print("\nAvailable MP3 bitrates:")

    for index, bitrate in enumerate(AUDIO_BITRATES, start=1):
        print(f"{index}. {bitrate} kbps")

    bitrate = select_option(AUDIO_BITRATES, "bitrate")

    if bitrate is None:
        print("Cancelled.")
        return

    print(f"\nSelected: {bitrate} kbps MP3")

    if input("Start download? (y/n): ").strip().lower() == "y":
        download_audio(url, bitrate, info=info)
    else:
        print("Cancelled.")


def change_download_location():
    """Change and save the download directory."""

    try:
        current_dir = get_download_dir()
        print(f"\nCurrent location:\n{current_dir}")

        new_path = input(
            "\nNew download directory (Q to cancel): "
        ).strip()

        if new_path.lower() == "q":
            print("Cancelled.")
            return

        if not new_path:
            print("Directory cannot be empty.")
            return

        new_dir = save_download_dir(new_path)

        print(f"\nDownload location updated:\n{new_dir}")

    except (OSError, ValueError) as error:
        print(f"\nUnable to change download location: {error}")


def main():
    print(f"\nWelcome to {APP_NAME}!")

    while True:
        show_menu()

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            inspect_video()

        elif choice == "2":
            inspect_audio()

        elif choice == "3":
            change_download_location()

        elif choice == "4":
            print("\nGoodbye!")
            break

        else:
            print("\nInvalid option.")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print("\n\nApplication interrupted. Goodbye!")
