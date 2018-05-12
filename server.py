from blackjackTable import drawTable
from PIL import Image
import sys
import math

try:
  cardImages = Image.open('cards.gif')
  width = math.floor(cardImages.size[0] / 13)
  height = math.floor(cardImages.size[1] / 5)
  cardSize = (width, height)

except:
  print('Unable to load image')
  sys.exit(1)

# Draw a hand - each card is 25% shifted on top of the previous card
player = [[{"rank":2,"suit":"C"},{"rank":9,"suit":"S"},{"rank":1,"suit":"D"}],[{"rank":10,"suit":"C"},{"rank":9,"suit":"S"}]]
dealer = [{"rank":0,"suit":"N"},{"rank":9,"suit":"S"}]
userId = 'foo'

table = drawTable(cardImages, cardSize, player, dealer)
table.save(userId + '.png', 'png')
