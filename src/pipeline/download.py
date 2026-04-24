import yt_dlp
from pathlib import Path

def download_video(url: str,
                   download: bool = True,
                   save_dir: Path | str = "./downloads",
                   max_height: int = 480) -> tuple[str, str, str, Path]:
    save_dir = Path(save_dir)
    save_dir.mkdir(parents=True, exist_ok=True)
    outtmpl = str(save_dir / "%(title)s [%(id)s].%(ext)s")
    fmt = f"best[height<={max_height}]/best"
    with yt_dlp.YoutubeDL({"outtmpl": outtmpl, "format": fmt}) as ydl:
        info = ydl.extract_info(url, download=download)
        video_path = Path(ydl.prepare_filename(info))
    return info["title"], info["description"], info["id"], video_path