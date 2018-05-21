from PIL import Image
import math
from io import BytesIO
import os
from os import listdir
from os.path import isfile, join, basename, splitext
import boto3

diceDistance = 20

def saveToS3(image, name):
  s3 = boto3.client('s3', aws_access_key_id=os.environ['accessKeyId'], aws_secret_access_key=os.environ['secretAccessKey'])
  out_img = BytesIO()
  image.save(out_img, 'png')
  out_img.seek(0)
  key = 'craps/' + name + '.png'
  s3.put_object(Bucket='garrett-alexa-images', Key=key, Body=out_img, ACL='public-read')

def getDieImage(die):
  left = (die - 1) * dieSize[0]
  top = 0
  return dice.crop((left, top, left + dieSize[0], top + dieSize[1]))

def drawTable(die1, die2):
  image = table.copy()
  left = math.floor((table.size[0] - (2 * dieSize[0] + diceDistance)) / 2)
  top = math.floor((table.size[1] - dieSize[1]) / 2)
  image.paste(getDieImage(die1), (left, top))
  left += (diceDistance + dieSize[0])
  image.paste(getDieImage(die2), (left, top))
  return image

# First load the table and dice
try:
  table = Image.open('images/craps/craps.png')
  dice = Image.open('images/craps/dice.jpg')
  width = math.floor(dice.size[0] / 6)
  height = math.floor(dice.size[1] / 6)
  dieSize = (width, height)

except:
  print('Unable to load image')
  sys.exit(1)

# Draw each of the dice
for die1 in range(1, 7):
  for die2 in range(1, 7):
    diceImage = drawTable(die1, die2)
    name = 'craps' + str(die1) + str(die2)
    saveToS3(diceImage, name)
