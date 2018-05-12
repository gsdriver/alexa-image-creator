from PIL import Image
import math

def oneCard(cardImages, cardSize, rank, suit):
  # cards are 125x181, running 2-A

  # suit is heart, diamond, club, spade
  suits = {'H': 0, 'D': 1, 'C': 2, 'S': 3, 'N': 4}
  if suit == 'N':
    left = 0
  elif rank == 1:
    left = cardSize[0] * 12
  else:
    left = (rank - 2) * cardSize[0]

  top = suits.get(suit) * cardSize[1]
  return cardImages.crop((left, top, left + cardSize[0], top + cardSize[1]))

def drawHand(cardImages, cardSize, hand, leftOffset, topOffset):
  for card in hand:
    myCard = oneCard(cardImages, cardSize, card['rank'], card['suit'])
    table.paste(myCard, (leftOffset, topOffset))
    leftOffset += math.floor(0.25 * cardSize[0])
    topOffset += math.floor(0.25 * cardSize[1])

def drawDealer(cardImages, cardSize, hand):
  # dealer goes on right side of screen, cards drawn to the left
  left = table.size[0] - 10 - cardSize[0]
  top = 10
  for card in hand:
    myCard = oneCard(cardImages, cardSize, card['rank'], card['suit'])
    table.paste(myCard, (left, top))
    left -= math.floor(0.25 * cardSize[0])
    top += math.floor(0.25 * cardSize[1])

def drawTable(cardImages, cardSize, player, dealer):
  global table
  table = Image.new('RGBA', (1024, 600), (0, 255, 0, 255))
  left = 10
  for hand in player:
    drawHand(cardImages, cardSize, hand, left, 10)
    left += (10 + math.floor(cardSize[0] * (1 + 0.25 * (len(hand) - 1))))

  drawDealer(cardImages, cardSize, dealer)
  return table
