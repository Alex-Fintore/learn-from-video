#!/usr/bin/env python3
"""
get_transcript.py — extracts transcript and metadata from a YouTube video.

Usage:
    python get_transcript.py <youtube_url>

Output:
    JSON to stdout with fields: title, channel, url, transcript, language
"""

import sys
import json
import re
import os

# Force UTF-8 output on Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def extract_video_id(url: str) -> str:
    patterns = [
        r"(?:v=|youtu\.be/)([A-Za-z0-9_-]{11})",
        r"(?:embed/)([A-Za-z0-9_-]{11})",
        r"(?:shorts/)([A-Za-z0-9_-]{11})",
    ]
    for pattern in patterns:
        m = re.search(pattern, url)
        if m:
            return m.group(1)
    raise ValueError(f"Could not extract video ID from URL: {url}")


def get_transcript(video_id: str) -> dict:
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except ImportError:
        return {"error": "youtube_transcript_api not installed. Run: pip install youtube-transcript-api"}

    preferred_languages = ["ru", "en", "en-US", "en-GB"]

    try:
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)

        transcript = None
        lang_used = None

        # Try preferred languages (manual first)
        for lang in preferred_languages:
            try:
                transcript = transcript_list.find_manually_created_transcript([lang])
                lang_used = lang
                break
            except Exception:
                pass

        # Try auto-generated
        if transcript is None:
            for lang in preferred_languages:
                try:
                    transcript = transcript_list.find_generated_transcript([lang])
                    lang_used = f"{lang} (auto)"
                    break
                except Exception:
                    pass

        # Fallback: any available
        if transcript is None:
            available = list(transcript_list)
            if available:
                transcript = available[0]
                lang_used = transcript.language_code

        if transcript is None:
            return {"error": "No transcript available for this video"}

        entries = transcript.fetch()
        full_text = " ".join(entry.text for entry in entries)

        return {
            "video_id": video_id,
            "url": f"https://www.youtube.com/watch?v={video_id}",
            "language": lang_used,
            "transcript": full_text,
            "segments_count": len(entries),
        }

    except Exception as e:
        return {"error": str(e)}


def get_video_metadata(video_id: str) -> dict:
    """Try to get title/channel via yt-dlp Python API."""
    try:
        import yt_dlp
        ydl_opts = {"quiet": True, "no_warnings": True, "skip_download": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(
                f"https://www.youtube.com/watch?v={video_id}", download=False
            )
            return {
                "title": info.get("title", ""),
                "channel": info.get("channel", ""),
            }
    except Exception:
        pass
    return {"title": "", "channel": ""}


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python get_transcript.py <youtube_url>"}))
        sys.exit(1)

    url = sys.argv[1]

    try:
        video_id = extract_video_id(url)
    except ValueError as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

    result = get_transcript(video_id)
    meta = get_video_metadata(video_id)
    result.update(meta)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
