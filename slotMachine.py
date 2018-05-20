from PIL import Image
import math
from io import BytesIO
import os
from os import listdir
from os.path import isfile, join, basename, splitext
import boto3

slotDistance = 20

def saveToS3(image, name):
  s3 = boto3.client('s3', aws_access_key_id=os.environ['accessKeyId'], aws_secret_access_key=os.environ['secretAccessKey'])
  out_img = BytesIO()
  image.save(out_img, 'png')
  out_img.seek(0)
  key = 'slots/' + name + '.png'
  s3.put_object(Bucket='garrett-alexa-images', Key=key, Body=out_img, ACL='public-read')

def drawSlotMachine(slots):
  image = machineImage.copy()
  left = math.floor((image.size[0] - (len(slots) * slotSize[0]) - ((len(slots) - 1) * slotDistance)) / 2)
  top = math.floor((image.size[1] - slotSize[1]) / 2)
  for slot in slots:
    image.paste(slotImages.get(slot), (left, top))
    left += (slotDistance + slotSize[0])

  return image

def buildCombos(combos, partial, slots, toFill):
  if (toFill == 0):
    combos.append(partial)
  else:
    for slot in slots:
      newList = list(partial)
      newList.append(slot)
      buildCombos(combos, newList, slots, toFill - 1)

def drawAllCombos(slots, positions):
  combos = []
  buildCombos(combos, [], slots, positions)
  for combo in combos:
    name = ''
    for slot in combo:
      if (len(name) > 0):
        name += '-'
      name += slot
    image = drawSlotMachine(combo)
    saveToS3(image, name)

# First load the background and slots
slotImages = {}

try:
  machineImage = Image.open('images/slots/slot-background.png')
  width = math.floor(machineImage.size[0] / 6)
  height = math.floor(machineImage.size[1] * 0.4)
  slotSize = (width, height)

  slotDir = 'images/slots/slots'
  for f in listdir(slotDir):
    base = basename(f)
    slotImages[splitext(base)[0]] = Image.open(join(slotDir, f)).resize((width, height))

except:
  print('Unable to load image')
  sys.exit(1)

# Add slot combinations to draw and commit to s3
#drawAllCombos(['cherry', 'lemon', 'orange', 'plum', 'bar'], 3)
#drawAllCombos(['cherry', 'blank', 'bar', 'double bar', 'seven'], 3)
#drawAllCombos(['heart', 'bell', 'horseshoe', 'seven', 'gold bar'], 3)
#drawAllCombos(['cherry', 'bell', 'orange', 'bar', 'diamond'], 3)
#drawAllCombos(['cherry', 'plum', 'bell', 'bar', 'seven', 'diamond'], 3)
#drawAllCombos(['heart', 'bell', 'orange', 'bar', 'seven'], 3)
#drawAllCombos(['chicken', 'turkey', 'pork', 'veal', 'steak'], 3)
#drawAllCombos(['cherry', 'heart', 'orange', 'gold bar', 'seven'], 3)
#drawAllCombos(['maggie', 'lisa', 'marge', 'bart', 'homer'], 3)
