from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

JOURNEY = '''Fill "Email" with "test@example.com"
Fill secret "Password" with "PR_TEST_PASSWORD"
Click "Sign In"
Verify visible "Dashboard"
Click "Add to cart"
Verify "cart-count" equals "1"
Verify "cart-total" equals "R$ 100,00"'''

@contextmanager
def demo_server():
    body = Path(__file__).with_name("demo.html").read_bytes()
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(body)
        def log_message(self, *args):
            pass
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}/"
    finally:
        server.shutdown()
        server.server_close()
        thread.join()
