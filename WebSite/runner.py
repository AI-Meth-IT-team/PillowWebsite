import http.server
import socketserver

PORT = 8000

DIRECTORY = "/home/integralsenso/Desktop/repo/PillowWebsite/WebSite/"

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

# Start the server
with socketserver.TCPServer(("0.0.0.0", PORT), CustomHandler) as httpd:
    print(f"Serving at http://192.168.4.1:{PORT}")
    httpd.serve_forever()
