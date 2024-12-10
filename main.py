import os
import ffmpeg
from pytubefix import YouTube

SAVE_PATH = "/Users/guppythegod/Desktop/knowledgeworker-ai-downloads"
LINK = "https://www.youtube.com/watch?v=xWOoBJUqlbI"

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
        "channel_url": yt.channel_url
    }

def download_video_as_mp4(yt):
    # Get all streams and filter for mp4 files
    mp4_streams = yt.streams.filter(file_extension="mp4")

    # Get the video with the highest resolution
    d_video = mp4_streams[-1]

    print(d_video)

    try:
        # Download the video
        d_video.download(output_path=SAVE_PATH)
        print("Video downloaded successfully!")
    except:
        print("Some Error!")

def convert_to_audio(title):
    # Get the video file
    video_file = os.path.join(SAVE_PATH, title + ".mp4")
    output_file = os.path.join(SAVE_PATH, title + ".mp3")

    try:
        # Convert to audio using ffmpeg-python
        stream = ffmpeg.input(video_file)
        stream = ffmpeg.output(stream, output_file, acodec='libmp3lame', q='2', vn=None)
        ffmpeg.run(stream, overwrite_output=True)
        print("Audio converted successfully!")
    except ffmpeg.Error as e:
        print(f"An error occurred: {e.stderr.decode()}")


def main():
    try:
        # Object creation using YouTube
        # which was imported in the beginning
        yt = YouTube(LINK)
    except:
        # Handle exception
        print("Connection Error")

    video_info = get_video_info(yt)
    print(video_info)
    download_video_as_mp4(yt)
    convert_to_audio(video_info["title"])

    print("Task Completed!")

if __name__ == "__main__":
    main()