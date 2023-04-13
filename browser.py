import socket
import tkinter

def request(url):

    assert url.startswith("http://")
    url = url[len("http://"):]
    ip = socket.gethostbyname('www.google.com')

    host, path = url.split("/", 1)
    path = "/" + path

    s = socket.socket(
        family=socket.AF_INET,
        type=socket.SOCK_STREAM,
        proto=socket.IPPROTO_TCP,
    )

    s.connect((host, 80))

    s.send("GET {} HTTP/1.0\r\n".format(path).encode("utf8") +
           "Host: {}\r\n\r\n".format(host).encode("utf8"))

    response = s.makefile("r", encoding="utf8", newline="\r\n")

    statusline = response.readline()
    version, status, explanation = statusline.split(" ", 2)
    assert status == "200", "{}: {}".format(status, explanation)

    headers = {}
    while True:
        line = response.readline()
        if line == "\r\n": break
        header, value = line.split(":", 1)
        headers[header.lower()] = value.strip()

    assert "transfer-encoding" not in headers
    assert "content-encoding" not in headers

    body = response.read()
    s.close()

    return headers, body

def show(body):
    in_angle = False
    for c in body:
        if c == "<":
            in_angle = True
        elif c == ">":
            in_angle = False
        elif not in_angle:
            print(c, end="")


def lex(input):
    body = ""
    i = 0
    in_body = False
    print(len(input))
    for c in input:
        if c == "<" and  "b" == input[i + 1] and  "o" == input[i + 2] and  "d" == input[i + 3] and  "y" == input[i + 4] and ">" == input[i + 5]:
            in_body = True
            print(i)
            print(input[i+1])
        elif c == "<" and "/" == input[i + 1] and "b" == input[i + 2]:
            in_body = False
        elif in_body:
            body += c
        i += 1
    body = body[4:-1]

    in_angle = False
    bodyLex = ""
    for c in body:
        if c == "<":
            in_angle = True
        elif c == ">":
            in_angle = False
        elif not in_angle:
            print(c, end="")
            bodyLex += c

    return bodyLex

def layout(text):
    display_list = []
    cursor_x, cursor_y = 20, 10
    for c in text:
        display_list.append((cursor_x, cursor_y, c))
        cursor_x += 10
        if cursor_x > 200:
            cursor_y += 10
            cursor_x = 10
    return display_list
class Browser:
    def __init__(self):
        self.WIDTH, self.HEIGHT = 800, 600
        self.scroll = 0
        self.window = tkinter.Tk()
        self.window.bind("<Down>", self.scrolldown)
        self.canvas = tkinter.Canvas(
            self.window,
            width=self.WIDTH,
            height=self.HEIGHT
        )
        self.canvas.pack()

    def scrolldown(self, e):
        self.scroll += 10
        self.draw()
    def load(self, url):
        headers , response = request(url)
        respone = lex(response)
        self.display_list = layout(respone)
        self.draw()
    def draw(self):
        self.canvas.delete("all")
        for x, y, c in self.display_list:
            self.canvas.create_text(x, y - self.scroll, text=c)
            x += 10
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    url = "http://www.example.org/index.html"
 #   load(url)
    Browser().load(url)
    tkinter.mainloop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
