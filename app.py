from flask import Flask, Response
import requests
from urllib.parse import urljoin

app = Flask(__name__)

MASTER_URL = "https://l4.cloudskep.com/alphacyp/acy/playlist.m3u8"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.alphacyprus.com.cy/",
    "Origin": "https://www.alphacyprus.com.cy"
}

def get_master():
    r = requests.get(MASTER_URL, headers=HEADERS)
    r.raise_for_status()
    return r.text

def extract_fhd(master):
    for line in master.splitlines():
        if "/fhd/" in line and "chunks.m3u8" in line:
            return line

def fetch_playlist(url):
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    return r.text

def rewrite_playlist(content, base_url):
    base = base_url.rsplit("/",1)[0] + "/"
    lines = []
    for line in content.splitlines():
        if line.startswith("#") or line.strip() == "":
            lines.append(line)
        else:
            # Absolute URL voor VLC
            lines.append(urljoin(base, line))
    return "\n".join(lines)

@app.route("/live.m3u8")
def stream():
    master = get_master()
    fhd = extract_fhd(master)
    playlist = fetch_playlist(fhd)
    fixed = rewrite_playlist(playlist, fhd)
    return Response(fixed, mimetype="application/vnd.apple.mpegurl")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
