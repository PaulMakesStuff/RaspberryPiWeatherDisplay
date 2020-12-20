from PIL import Image, ImageFont, ImageDraw
from inky.auto import auto
import os

class InfoWindow():
  def __init__(self):
    try:
      self.inkyphat = auto(ask_user=False, verbose=True)
    except TypeError:
      raise TypeError("You need to update the Inky library to >= v1.1.0")
    self.inkyphat.h_flip = True
    self.inkyphat.v_flip = True
    self.width = 250
    self.height = 122
    self.image = Image.new("P", (self.width, self.height), 0)
    self.image.putpalette([ 0, 0, 0, 255, 255, 255, ])
    self.draw = ImageDraw.Draw(self.image)
    self.initFonts()

  def initFonts(self):
    chikarego = "fonts/chikarego/"
    self.fonts = {
      'chikarego16': ImageFont.truetype(chikarego + "ChiKareGo.ttf", 16),
      'chikarego18': ImageFont.truetype(chikarego + "ChiKareGo.ttf", 18),
      'chikarego20': ImageFont.truetype(chikarego + "ChiKareGo.ttf", 20),
      'chikarego22': ImageFont.truetype(chikarego + "ChiKareGo.ttf", 22),
      'chikarego24': ImageFont.truetype(chikarego + "ChiKareGo.ttf", 24),
      'chikarego26': ImageFont.truetype(chikarego + "ChiKareGo.ttf", 26),
      'chikarego28': ImageFont.truetype(chikarego + "ChiKareGo.ttf", 28),
      'chikarego30': ImageFont.truetype(chikarego + "ChiKareGo.ttf", 30),
    }

  def getFont(self, font_name):
    return self.fonts[font_name]

  def text(self, left, top, text, font, fill, anchor = "lt"):
    text = self.truncate(text, font)
    font = self.fonts[font]
    self.draw.text((left, top), text, font = font, fill = fill, anchor = anchor)
    return self.draw.textsize(text, font = font)

  def line(self, left_1, top_1, left_2, top_2, fill, width=1):
    self.draw.line((left_1, top_1, left_2, top_2), fill=fill)

  def truncate(self, str, font):
    for char in str:
      (np_x, np_y) = self.getFont(font).getsize(str)
      if np_x >= 235:
        str = str[:-1]
        if np_x <= 235:
          return str 
    return str

  def setIcon(self, x, y, im ):
    self.draw.bitmap((x, y), im.convert("1"), 1 )

  def displayImage(self):
    self.inkyphat.set_image(self.image)
    self.inkyphat.show()
