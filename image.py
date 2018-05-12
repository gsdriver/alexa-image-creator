from PIL import Image
import sys
import math

try:
  im = Image.open('cards.gif')
  cardWidth = math.floor(im.size[0] / 13)
  cardHeight = math.floor(im.size[1] / 5)

except:
  print('Unable to load image')
  sys.exit(1)

def oneCard(rank, suit):
  # cards are 125x181, running 2-A

  # suit is heart, diamond, club, spade
  suits = {'H': 0, 'D': 1, 'C': 2, 'S': 3, 'N': 4}
  if suit == 'N':
    left = 0
  elif rank == 1:
    left = cardWidth * 12
  else:
    left = (rank - 2) * cardWidth

  top = suits.get(suit) * cardHeight
  return im.crop((left, top, left + cardWidth, top + cardHeight))

def drawHand(table, hand, leftOffset, topOffset):
  for card in hand:
    myCard = oneCard(card['rank'], card['suit'])
    table.paste(myCard, (leftOffset, topOffset))
    leftOffset += math.floor(0.25 * cardWidth)
    topOffset += math.floor(0.25 * cardHeight)

def drawDealer(table, hand):
  # dealer goes on right side of screen, cards drawn to the left
  left = table.size[0] - 10 - cardWidth
  top = 10
  for card in hand:
    myCard = oneCard(card['rank'], card['suit'])
    table.paste(myCard, (left, top))
    left -= math.floor(0.25 * cardWidth)
    top += math.floor(0.25 * cardHeight)

def drawTable(userId, player, dealer):
  table = Image.new('RGBA', (1024, 600), (0, 255, 0, 255))
  left = 10
  for hand in player:
    drawHand(table, hand, left, 10)
    left += (10 + math.floor(cardWidth * (1 + 0.25 * (len(hand) - 1))))

  drawDealer(table, dealer)
  table.save(userId + '.png', 'png');

# Draw a hand - each card is 25% shifted on top of the previous card
player = [[{"rank":2,"suit":"C"},{"rank":9,"suit":"S"},{"rank":1,"suit":"D"}],[{"rank":10,"suit":"C"},{"rank":9,"suit":"S"}]]
dealer = [{"rank":0,"suit":"N"},{"rank":9,"suit":"S"}]

drawTable('foo', player, dealer)

