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
    return r.text

def extract(master, quality):

    for line in master.splitlines():

        if quality in line and "chunks.m3u8" in line:
            return line

def rewrite(content, base):

    base_url = base.rsplit("/",1)[0] + "/"
    lines = []

    for line in content.splitlines():

        if line.startswith("#"):
            lines.append(line)

        else:
            lines.append(urljoin(base_url, line))

    return "\n".join(lines)

@app.route("/live/<quality>.m3u8")
def stream(quality):

    master = get_master()

    stream = extract(master, quality)

    r = requests.get(stream, headers=HEADERS)

    playlist = rewrite(r.text, stream)

    return Response(playlist, mimetype="application/vnd.apple.mpegurl")


@app.route("/iptv.m3u")
def iptv():

    return """
#EXTM3U
#EXTINF:-1,Alpha Cyprus FHD
http://localhost:8080/live/fhd.m3u8
#EXTINF:-1,Alpha Cyprus HD
http://localhost:8080/live/hd.m3u8
#EXTINF:-1,Alpha Cyprus SD
http://localhost:8080/live/sd.m3u8
"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
