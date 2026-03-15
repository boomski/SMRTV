from playwright.sync_api import sync_playwright

URL = "https://www.alphacyprus.com.cy/live"

stream_url = None

with sync_playwright() as p:
    browser = p.firefox.launch(headless=True)
    page = browser.new_page()

    def handle_request(request):
        global stream_url
        url = request.url
        if "playlist.m3u8" in url and "wmsAuthSign" in url:
            stream_url = url

    page.on("request", handle_request)

    page.goto(URL)
    page.wait_for_timeout(5000)

    browser.close()

if stream_url:
    playlist = f"""#EXTM3U
#EXTINF:-1,Alpha Cyprus
{stream_url}
"""

    with open("alpha.m3u8", "w") as f:
        f.write(playlist)

    print("Echte stream:", stream_url)
else:
    print("Geen stream gevonden")
