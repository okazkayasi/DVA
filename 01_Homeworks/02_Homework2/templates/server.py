from http.server import BaseHTTPRequestHandler, HTTPServer

# HTTPRequestHandler class

class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):

    # GET
    def do_GET(self):
        # send response status code
        self.send_response(200)
        
        # send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # send message back to client
        message = "Hello World"
        # write content as utf-8 data
        self.wfile.write(bytes(message, 'utf-8'))
        return

def run():
    print('starting server...')

    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server
    # you need root access
    server_address = ('127.0.0.1', 8080)
    httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
    print('running server...')
    httpd.serve_forever()


run()