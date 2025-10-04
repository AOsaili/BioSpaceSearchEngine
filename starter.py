import http.server
import socketserver
import webbrowser
import threading

PORT = 8000
DIRECTORY = "."  # serve current folder

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def open_browser():
    webbrowser.open(f"http://localhost:{PORT}/mycode2.html")

def start_server():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"🚀 Serving at: http://localhost:{PORT}")
        print("Press CTRL+C to stop.")
        httpd.serve_forever()

if __name__ == "__main__":
    threading.Timer(1.0, open_browser).start()
    start_server()
