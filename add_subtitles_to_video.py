"""Add subtitles to video files"""

import os
import subprocess

import whisper


def audio_file_to_subtitles(path: str) -> str:
    """Get the transcription of an audio file with timestamps for subtitles.

    Args:
        path (str): The path to the file to transcribe.

    Returns:
        str: The transcribed text with timestamps for each segment.
    """
    model = whisper.load_model(
        "large", download_root=os.path.expanduser("~/.cache/whisper")
    )
    result = model.transcribe(path)

    subtitles = []
    for segment in result["segments"]:
        start_time: float = segment[
            "start"
        ]  # pyright: ignore [reportArgumentType, reportAssignmentType]
        end_time: float = segment[
            "end"
        ]  # pyright: ignore [reportArgumentType, reportAssignmentType]
        text = segment["text"]  # pyright: ignore [reportArgumentType]

        start_str = format_time(start_time)
        end_str = format_time(end_time)

        subtitles.append(
            f"{len(subtitles) + 1}\n{start_str} --> {end_str}\n{text}\n"
        )

    return "\n".join(subtitles)


def format_time(seconds: float) -> str:
    """Convert seconds to a time string in the format of
    hours:minutes:seconds,milliseconds (for SRT).

    Args:
        seconds (float): The time in seconds.

    Returns:
        str: The formatted time string.
    """
    millis = int((seconds % 1) * 1000)  # Get milliseconds
    seconds_int = int(seconds)  # Get the whole seconds
    minutes = seconds_int // 60
    hours = minutes // 60
    minutes = minutes % 60
    seconds_int = seconds_int % 60

    return f"{hours:02}:{minutes:02}:{seconds_int:02},{millis:03}"


def save_subtitles_to_file(subtitles: str, filename: str) -> None:
    """Save subtitles to a .srt file.

    Args:
        subtitles (str): The subtitles text.
        filename (str): The file to save subtitles to.
    """
    with open(filename, "w", encoding="utf-8") as f:
        f.write(subtitles)


def add_subtitles_to_video(
    video_path: str, subtitle_path: str, output_path: str
) -> None:
    """Add subtitles to a video file.

    Args:
        video_path (str): The path to the input video.
        subtitle_path (str): The path to the subtitle file.
        output_path (str): The path to the output video.
    """
    command = [
        "ffmpeg",
        "-i",
        video_path,  # Input video file
        "-i",
        subtitle_path,  # Subtitle file
        "-c:v",
        "copy",  # Copy the video codec (no re-encoding)
        "-c:a",
        "copy",  # Copy the audio codec (no re-encoding)
        "-c:s",
        "mov_text",  # Use mov_text codec for subtitles
        "-map",
        "0",  # Map all streams from input
        "-map",
        "1",  # Map subtitle stream
        "-y",  # Overwrite output file if it exists
        output_path,  # Output file path
    ]

    subprocess.run(command, check=True)


def main():
    "The main function."
    filename = ""  # Enter filename here
    video_path = f"{filename}.mp4"
    subtitles = audio_file_to_subtitles(video_path)
    subtitle_path = f"{filename}_subtitles.srt"
    save_subtitles_to_file(subtitles, subtitle_path)

    output_path = f"{filename}_with_subtitles.mp4"
    add_subtitles_to_video(video_path, subtitle_path, output_path)


if __name__ == "__main__":
    main()
