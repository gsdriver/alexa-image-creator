from PIL import Image
import sys
import math

cardWidth = 125
cardHeight = 181
result = Image.new('RGBA', (1024, 600), (0, 255, 0, 255))

try:
  im = Image.open('cards.gif')

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

def drawHand(hand, leftOffset, topOffset):
  for card in hand:
    myCard = oneCard(card['rank'], card['suit'])
    result.paste(myCard, (leftOffset, topOffset))
    leftOffset += math.floor(0.25 * cardWidth)
    topOffset += math.floor(0.25 * cardHeight)

# Draw a hand - each card is 25% shifted on top of the previous card
hands = [{"bet":100,"busted":False,"total":19,"cards":[{"rank":10,"suit":"C"},{"rank":9,"suit":"S"}],"outcome":"playing","soft":False},
      {"bet":100,"busted":False,"total":19,"cards":[{"rank":10,"suit":"C"},{"rank":9,"suit":"S"}],"outcome":"playing","soft":False}]

left = 10
for i in range(0, len(hands)):
  if i > 0:
    left += (10 + math.floor(cardWidth * (1 + 0.25 * (len(hands[i - 1]['cards']) - 1))))

  drawHand(hands[i]['cards'], left, 10)
result.show()
