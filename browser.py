import socket

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
        print(line)
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

def load(url):
    headers, body = request(url)
    show(body)
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    url = "http://www.example.org/index.html"
    load(url)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/