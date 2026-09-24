import http.server
import socketserver
import os

PORT = 8765
DIR = r"C:\OLIVERS WEB\olivers-site"

class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIR, **kwargs)
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()
    def log_message(self, fmt, *args):
        pass

socketserver.TCPServer.allow_reuse_address = True

class ThreadingServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True

with ThreadingServer(("127.0.0.1", PORT), NoCacheHandler) as httpd:
    print(f"Serving {DIR} on http://localhost:{PORT} (no-cache, threaded)")
    httpd.serve_forever()
