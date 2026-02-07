from youtube_transcript_api import (
    YouTubeTranscriptApi,
    VideoUnavailable,
    TranscriptsDisabled,
    NoTranscriptFound,
)

from time import sleep
import yt_dlp


def banner():
    LIGHT_RED = "\033[1;31m"
    END = "\033[0m"

    banner = f"""{LIGHT_RED}

██╗   ██╗ ██████╗ ███████╗██╗███╗   ██╗████████╗
╚██╗ ██╔╝██╔═══██╗██╔════╝██║████╗  ██║╚══██╔══╝
 ╚████╔╝ ██║   ██║███████╗██║██╔██╗ ██║   ██║   
  ╚██╔╝  ██║   ██║╚════██║██║██║╚██╗██║   ██║   
   ██║   ╚██████╔╝███████║██║██║ ╚████║   ██║   
   ╚═╝    ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝   
    {END}
    author MuteAvery
    """
    print(banner)


# fetch the transript from the youtube video
def fetch_transcript_singleVideo(videoID, text_to_find):
    try:
        # fetch the transcript
        ytt_api = YouTubeTranscriptApi()
        fetched_transcript = ytt_api.fetch(videoID)

        # search for matches
        matches = [
            entry
            for entry in fetched_transcript
            if text_to_find.lower() in entry.text.lower()
        ]

        if not matches:
            print("No matches found.")
            return

        for idx, match in enumerate(matches, start=1):
            print(f"\nMatch {idx}")
            print("=" * 25)
            print(
                f"Text = {match.text}\nStart = {match.start}\nDuration = {match.duration}"
            )
            print("=" * 25)

    except Exception as e:
        print(f"Error while searching transcript: {type(e).__name__}: {e}")


# scrape a youtubers video IDs
def get_video_ids():
    url = input("Channel videos URL: ")

    ydl_opts = {
        "skip_download": True,
        "extract_flat": "in_playlist",
        "quiet": True,
        # Safety
        "socket_timeout": 30,
        "retries": 3,
        "fragment_retries": 3,
        "http_chunk_size": 10485760,  # 10MB (prevents bursts)
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    return [entry["id"] for entry in info.get("entries", []) if entry and "id" in entry]


def get_all_cases_of_text(
    text_to_find,
):
    video_ids = get_video_ids()
    ytt_api = YouTubeTranscriptApi()
    print("Looking through the transcript's,  this may take a while!")
    # itterate thru each videoID and search for the text
    for v in video_ids:
        try:
            videoID = v
            # sleep for rate limit
            sleep(5)
            fetched_transcript = ytt_api.fetch(videoID)

            # search for matches
            matches = [
                entry
                for entry in fetched_transcript
                if text_to_find.lower() in entry.text.lower()
            ]

            if not matches:
                print(f"No matches found in video {videoID}.")

            for idx, match in enumerate(matches, start=1):
                print(f"\nMatch {idx}, VideoID: {videoID}")
                print("=" * 25)
                print(
                    f"Text = {match.text}\nStart = {match.start}\nDuration = {match.duration},\nVideo_link https://youtube.com/watch?={videoID}"
                )
                print("=" * 25)
        except VideoUnavailable:
            print(f"\nFailed to find video Moving on... .{videoID}")
            continue
        except TranscriptsDisabled:
            print(f"\nTranscipt was disabled on this video {videoID}")
            continue
        except NoTranscriptFound:
            print(f"\nTranscipt could not be found: {videoID}")
            continue


def main():
    banner()

    print("Main Menu!")
    while True:
        print("1. Search single video")
        print("2. Search full channel (Warning slow ... so so slow)")
        print("0. Exit")

        try:
            choice = int(input("Select an option: "))
        except ValueError:
            print("\nError please select an option i,e 1\n")
            continue

        match choice:
            case 1:
                videoID = input("Please submit the video ID: ")
                text_to_find = input("Please submit the text you wish to search for: ")
                fetch_transcript_singleVideo(videoID, text_to_find)
                break
            case 2:
                text_to_find = input("Please submit the text you wish to search for: ")
                get_all_cases_of_text(text_to_find)
                break
            case 0:
                print("Goodbye... .")
                break


if __name__ == "__main__":
    main()
