import cv2
import base64
from moviepy import VideoFileClip
from pathlib import Path
from typing import Any
import tempfile

def prepare_gemma4_input(video_path: Path,
                         fps: int = 1,
                         frame_size: tuple[int, int] = (448, 448),
                         extract_audio: bool = False) -> list[dict[str, Any]]:
    """
    Extracts frames and audio from a video file for Gemma 4.
    """
    inputs = []
    if extract_audio:
        # --- 1. Extract Audio ---
        # Gemma 4:e4b accepts audio tokens (base64 encoded)
        # But we haven't implemented this fully yet so by default it's off
        with VideoFileClip(video_path) as video_clip:
            audio_path = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False).name
            video_clip.audio.write_audiofile(audio_path, logger=None)
        
        with open(audio_path, "rb") as f:
            audio_b64 = base64.b64encode(f.read()).decode("utf-8")
        
        inputs.append({
            "type": "input_audio", 
            "input_audio": {"data": audio_b64, "format": "mp3"}
        })
        Path(audio_path).unlink()

    # --- 2. Extract Frames ---
    video = cv2.VideoCapture(video_path)
    video_fps = video.get(cv2.CAP_PROP_FPS)
    frame_interval = int(video_fps / fps)
    
    success, frame_count = True, 0
    while success:
        success, frame = video.read()
        if success and frame_count % frame_interval == 0:
            frame = cv2.resize(frame, frame_size)
            _, buffer = cv2.imencode(".jpg", frame)
            img_b64 = base64.b64encode(buffer).decode("utf-8")
            inputs.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}
            })
        frame_count += 1
        
    video.release()
    return inputs
