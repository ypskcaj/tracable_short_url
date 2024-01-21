from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import re
import user_agents
import uuid

from jinja2 import Template
from RedisConnector import RedisConnector
from URLConverter import URLConverter
from EventLogger import EventLogger


hostName = "localhost"
serverPort = 8080
redisHost = "localhost"
redisPort = 6379
redisAuthentication = None

def loadHTMLTemplate(filename):
    with open(filename) as file:
        template_content = file.read()
    return Template(template_content)

class MyServer(BaseHTTPRequestHandler):

    def normalHeader(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def checkShortURLSession(self):
        s = self.headers.get('cookie')
        if s is not None:
            cookies = s.split(';')
            for c in cookies:
                (n, v) = c.split('=')
                if n.lstrip().rstrip() == "ShortURLSession":
                    return v.lstrip().rstrip()
        return None

    def newShortURLSession(self):
        self.send_header("Set-Cookie","ShortURLSession=" + str(uuid.uuid4()))

    def do_GET(self):

        if self.path == "/":
            # show Short URL creation form
            self.normalHeader()
            self.wfile.write(bytes(htmlTemplateCreateForm.render(),"utf-8"))

        elif re.match(r'/r/', self.path):
            # Covert from short URL to long URL
            # 1st get client parameters
            (clientAddress, clientPort) = self.client_address
            user_agent = user_agents.parse(self.headers.get('User-Agent'))

            # 2nd get original URL & label
            matchObj = re.match(r'/r/(.*)', self.path)
            shortURLCode = matchObj.group(1)
            (longURL, label) = uc.getLong(shortURLCode)

            # re-redirect to original URL, and log the event
            if longURL is not None:
                session = self.checkShortURLSession()
                if session is None:
                    # In case if the first time visit, assign a new cookie with dedicated pages
                    self.send_response(200)
                    self.newShortURLSession()
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(bytes(htmlTemplateRedirect.render(longURL=longURL),"utf-8"))

                else:
                    # already has session, just re-direct to the original URL
                    self.send_response(301)
                    self.send_header("location", longURL)
                    self.end_headers()
                el.log([clientAddress,
                        label,
                        session,
                        user_agent.browser.family,
                        user_agent.browser.version_string,
                        user_agent.os.family,
                        user_agent.os.version_string,
                        user_agent.device.family,
                        user_agent.device.brand,
                        user_agent.device.model,
                        shortURLCode,
                        longURL])
            else:
                self.normalHeader()
                self.wfile.write(bytes(htmlTemplateInfo.render(title="Wrong URL",
                    message="URL Code: " + shortURLCode + " deos not exist"),"utf-8"))
        elif self.path == "/favicon.ico":
            self.send_response(404)
        else:
            self.normalHeader()
            self.wfile.write(bytes(htmlTemplateInfo.render(title="Wrong parameters",
                message="Please input correct parameters."),"utf-8"))

    def do_POST(self):
        if self.path == "/ShortenURL":
            content_length = int(self.headers['Content-Length'])
            data = urllib.parse.parse_qs(self.rfile.read(content_length).decode('utf-8'))
            urls = data.get('ourl')
            labels = data.get('label')
            if urls is None:
                self.normalHeader()
                self.wfile.write(bytes(htmlTemplateInfo.render(title="Wrong parameters",
                    message="Please input correct parameters."),"utf-8"))
            else:
                longURL = urls[0]
                label = None
                if labels is not None:
                    label = labels[0]
                newURLCode = uc.shorten(longURL, label)
                newURL = "http://" + hostName + ":" + str(serverPort) + "/r/" + newURLCode
                self.normalHeader()
                self.wfile.write(bytes(htmlTemplateCreateDone.render(o_url=longURL, n_url=newURL),"utf-8"))
        else:
            self.normalHeader()
            self.wfile.write(bytes(htmlTemplateInfo.render(title="Wrong parameters",
                message="Please input correct parameters."),"utf-8"))

if __name__ == "__main__":
    # load HTML templates
    htmlTemplateCreateForm = loadHTMLTemplate("template/URLCreateForm.html")
    htmlTemplateCreateDone = loadHTMLTemplate("template/URLCreateDone.html")
    htmlTemplateInfo = loadHTMLTemplate("template/URLInfo.html")
    htmlTemplateRedirect = loadHTMLTemplate("template/URLRedirect.html")

    # create converter connecting to redis
    uc = URLConverter(RedisConnector(redisHost, redisPort, redisAuthentication))

    el = EventLogger("./logs/ShortUrlVisit",["clientAddress",
            "label",
            "session",
            "user_agent.browser.family",
            "user_agent.browser.version_string",
            "user_agent.os.family",
            "user_agent.os.version_string",
            "user_agent.device.family",
            "user_agent.device.brand",
            "user_agent.device.model",
            "shortURLCode",
            "longURL"])
    # create
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
