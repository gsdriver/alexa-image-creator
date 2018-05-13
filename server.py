import http.server
import socketserver
from blackjackTable import drawTable
from PIL import Image
import sys
import math
from urllib import parse
import json
import boto3
from io import BytesIO
import os

class Handler(http.server.SimpleHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _set_error(self, err):
        self.send_response(err)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        params = parse.parse_qs(parse.urlsplit(self.path).query)
        try:
          game = params['game'][0]
          if game == 'blackjack':
            userId = params['userId'][0]
            dealer = json.loads(params['dealer'][0])
            player = json.loads(params['player'][0])
          else:
            self._set_error(400)

        except:
          print('Exception!')
          self._set_error(400)
          return

        # Now draw the table and store in S3
        table = drawTable(cardImages, cardSize, player, dealer)
        s3 = boto3.resource('s3', aws_access_key_id=os.environ['accessKeyId'], aws_secret_access_key=os.environ['secretAccessKey'])
        out_img = BytesIO()
        table.save(out_img, 'png')
        out_img.seek(0)
        s3.Bucket('garrett-alexa-images').put_object(Key='blackjack/' + userId + '.png', Body=out_img)

        # Let them know the location in the response
        self.send_response(200)
        response = BytesIO()
        s3file = {'file': 'https://s3.amazonaws.com/garrett-alexa-images/blackjack/' + userId + '.png'}
        b = bytearray()
        b.extend(map(ord, json.dumps(s3file)))
        response.write(b)
        self.wfile.write(response.getvalue());

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
