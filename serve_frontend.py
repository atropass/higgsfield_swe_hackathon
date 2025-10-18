#EXAMPLE FRONTEND FOR my vibe code frontender friend
"""Simple HTTP server to serve the frontend."""

import http.server
import socketserver

PORT = 3000

class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), CORSRequestHandler) as httpd:
        print(f"\n{'='*60}")
        print(f"🌐 Frontend server running at http://localhost:{PORT}")
        print(f"{'='*60}")
        print(f"\n📂 Open http://localhost:{PORT}/frontend.html in your browser")
        print(f"\n⚠️  Make sure the API is running on http://localhost:8000\n")
        httpd.serve_forever()

