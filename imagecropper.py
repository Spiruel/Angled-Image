from PIL import Image

input_img = Image.open('row1.png')
width, height = input_img.size
box = (0, 25, width, height)
output_img = input_img.crop(box)
output_img.save('output.png')

