# AI Subtitles

A simple script to extract audio from videos, generate subtitles using Whisper AI, and embed them back into the video.

## Description

This script:

1. Transcribes audio from MP4 videos using OpenAI's Whisper model
2. Generates SRT subtitle files with precise timing
3. Embeds subtitles into new video files using ffmpeg

## Installation

### Python dependencies

```bash
pip install whisper
```

### System dependencies (install ffmpeg)
Ubuntu/Debian:
```bash
sudo apt install ffmpeg
```

Fedora:
```bash
sudo dnf install ffmpeg-free
```

Arch:
```bash
sudo pacman -S ffmpeg
```

## Usage
Replace the filename variable in the main function with your video file name (without extension)

Run the script:
```bash
python3 add_subtitles_to_video.py
```

Input file:

- `your_video.mp4`

Output files:

- `your_video_subtitles.srt` (raw subtitle file)
- `your_video_with_subtitles.mp4` (final video with embedded subtitles)

Note: Uses the "large" Whisper model for best accuracy, which requires ~3GB disk space and ~10GB VRAM
