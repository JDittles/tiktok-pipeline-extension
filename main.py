import sys
from dotenv import load_dotenv
from src.pipeline.classify import classify_video

def main():
    load_dotenv()
    if len(sys.argv) < 2:
        print("Usage: python main.py <tiktok_url>")
        print("       python main.py --serve")
        sys.exit(1)

    if sys.argv[1] == "--serve":
        import uvicorn
        uvicorn.run("src.api:app", host="0.0.0.0", port=8000, reload=True)
    else:
        url = sys.argv[1]
        result = classify_video(url)
        print(result)

if __name__ == "__main__":
    main()
