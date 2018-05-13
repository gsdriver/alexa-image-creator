import http.server
import socketserver
from blackjackTable import drawTable
from PIL import Image
import sys
import math
from urllib import parse
import json

class Handler(http.server.SimpleHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        params = parse.parse_qs(parse.urlsplit(self.path).query)
        try:
          userId = params['userId'][0]
          dealer = json.loads(params['dealer'][0])
          player = json.loads(params['player'][0])

        except:
          print('Exception!')
          self.send_response(400)
          self.send_header('Content-type', 'text/html')
          self.end_headers()
          return

        # Now draw the table
        table = drawTable(cardImages, cardSize, player, dealer)
        table.save(userId + '.png', 'png')
        self._set_headers()

    def do_HEAD(self):
        self._set_headers()

httpd = socketserver.TCPServer(("", 8000), Handler)

# First load the card images since we'll need those a lot
try:
  cardImages = Image.open('cards.gif')
  width = math.floor(cardImages.size[0] / 13)
  height = math.floor(cardImages.size[1] / 5)
  cardSize = (width, height)

except:
  print('Unable to load image')
  sys.exit(1)

print('Starting httpd...')
httpd.serve_forever()
