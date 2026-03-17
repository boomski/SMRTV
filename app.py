from flask import Flask, Response
import requests
import re

app = Flask(__name__)

BASE_URL = "https://www.sanmarinortv.sm"

CHANNEL_PAGES = {
    "ch01": "/programmi/web-tv",
    "ch02": "/programmi/web-tv-sport"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": BASE_URL,
    "Origin": BASE_URL
}

def get_stream(page_path):
    url = BASE_URL + page_path
    r = requests.get(url, headers=HEADERS, timeout=10)

    match = re.search(r'https://smrtvlive\.b-cdn\.net[^"]+playlist\.m3u8', r.text)
    return match.group(0) if match else None


@app.route("/<channel>.m3u8")
def proxy(channel):
    if channel not in CHANNEL_PAGES:
        return "Channel not found", 404

    stream_url = get_stream(CHANNEL_PAGES[channel])

    if not stream_url:
        return "Stream not found", 500

    r = requests.get(stream_url, headers=HEADERS, timeout=10)

    return Response(
        r.content,
        content_type="application/vnd.apple.mpegurl"
    )


@app.route("/")
def index():
    return {
        "channels": {
            "ch01": "/ch01.m3u8",
            "ch02": "/ch02.m3u8"
        }
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
