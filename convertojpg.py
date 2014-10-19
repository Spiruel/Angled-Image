from PIL import Image
input = raw_input('Input file (.png): ')
im = Image.open(input)
im.save(input, "JPEG")