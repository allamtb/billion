import shutil

shutil.rmtree(f"E:/project/billions/billions/image/d1ev/20230303135008559948")


def run(server_class=BaseHTTPServer.HTTPServer,
        handler_class=BaseHTTPServer.BaseHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()