from PIL import Image, ImageDraw
# from moviepy.editor import *
from PIL import ImageFont


def img_create(text):
    # create a new image
    # image = Image.new('RGB', (500, 500), color='white')
    img_text_size = len(text)*20
    image = Image.new('RGBA', (img_text_size, 100), (255, 255, 255, 0))
    # create a new ImageDraw object
    draw = ImageDraw.Draw(image)
    # set the Hindi font
    hindi_font = ImageFont.truetype('TiroDevanagariHindi-Regular.ttf', size=50)
    # draw Hindi text on the image
    draw.text((0, 35), text, font=hindi_font, fill='white')
    # save the image
    image.save('hindi_text.png')


img_create(u'हमारे संवाददाता नैंसी मिश्रा की एक रिपोर्ट न्यूज़ रूम से')
