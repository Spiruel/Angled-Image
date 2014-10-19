import PIL
from PIL import Image

basewidth = 20480
img = Image.open('rows.png')
wpercent = (basewidth/float(img.size[0]))
hsize = int((float(img.size[1])*float(wpercent)))
img = img.resize((basewidth,hsize), PIL.Image.ANTIALIAS)
img.save('rows_reducedsize.png')