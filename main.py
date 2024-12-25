import os
import httpx
from openai import OpenAI
from deepgram import DeepgramClient, PrerecordedOptions
from pytubefix import YouTube

LINK = "https://www.youtube.com/watch?v=u20SkTIZuNk&list=WL&index=1"

deepgram = DeepgramClient(os.getenv("DEEPGRAM_API_KEY"))
gpt = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def get_video_info(yt) -> dict:
    return {
        "title": yt.title,
        "length": yt.length,
        "views": yt.views,
        "age_restricted": yt.age_restricted,
        "thumbnail_url": yt.thumbnail_url,
        "description": yt.description,
        "keywords": yt.keywords,
        "rating": yt.rating,
        "author": yt.author,
        "channel_url": yt.channel_url,
    }


def download_video_as_mp4(yt):
    save_path = "/Users/guppy57/Downloads/knowledgeworker-ai-downloads"
    mp4_streams = yt.streams.filter(file_extension="mp4")
    d_video = mp4_streams[-1]

    try:
        d_video.download(output_path=save_path)
    except Exception as e:
        print(e)
        print("Some Error!")

    return f"{save_path}/{yt.title}.m4a"


def transcribe_audio(file_path):
    buffer_data = None

    with open(file_path, "rb") as file:
        buffer_data = file.read()

    payload = {"buffer": buffer_data}

    options = PrerecordedOptions(smart_format=True, punctuate=True)

    response = deepgram.listen.rest.v("1").transcribe_file(
        payload,
        options,
        timeout=httpx.Timeout(300.0, connect=10.0),
    )

    return response["results"]["channels"][0]["alternatives"][0]["transcript"]


def summarize_text(transcript):
    response = gpt.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Summarize the following transcript: {transcript}",
            }
        ],
        model="gpt-4o",
    )
    print(response)


def main():
    try:
        yt = YouTube(LINK)
    except:
        # Handle exception
        print("Connection Error")

    video_info = get_video_info(yt)
    file_path = download_video_as_mp4(yt)
    transcription = transcribe_audio(file_path)
    summary = summarize_text(transcription)

    print(summary)
    # create a markdown file based on a template provided for Obsidian
    # somehow get the file to obsidian or something.

    print("Task Completed!")


if __name__ == "__main__":
    main()
