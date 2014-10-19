from PIL import Image

img = Image.open("final.png")
(width, height)=img.size
size = 256, 256
count = 0

def savename():
    global count
    count = count + 1
    letters = ['q','r','s','t']
    if count > len(letters)-1:
        count = count - len(letters)-1
    return "t" + str(letters[count]) + str(letters[count]) + str(letters[count])

for i in range(0,15):
    e = 2**i
    gridx=width/2
    gridy=height/2
    print gridx, gridy
    rangex=width/gridx
    rangey=height/gridy
    print rangex*rangey
    for x in xrange(rangex):
        for y in xrange(rangey):
            box=(x*gridx, y*gridy, x*gridx+gridx, y*gridy+gridy)
            crop=img.crop(box)
            crop.thumbnail(size, Image.ANTIALIAS)
            crop.save('map/xmap_'+str(savename())+'.png', optimize=True, bits=6)
            print 'map/xmap_'+str(savename()) +'.png'
            #crop.save('map/xmap_'+str(x)+'_'+str(y)+'.png', optimize=True, bits=6)
            #print 'map/xmap_'+str(x)+'_'+str(y)+'.png'
    print width  

'''
size = 256, 256

input_image = Image.open('final.png')
width,height = input_image.size

for i in range(0,8,2):
    list = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u']
    e = 2**i
    a = width/e
    b = height/e
    box = (0, 0, width/2, height/2) #top left
    crop = input_image.crop(box)
    crop.thumbnail(size, Image.ANTIALIAS)
    crop.save('1' + str(list[i]) + '.png')
    box = (width/2, 0, width, height/2) #top right
    crop = input_image.crop(box)
    crop.thumbnail(size, Image.ANTIALIAS)
    crop.save('2' + str(list[i]) + '.png')
    box = (0, height/2, width/2, height) #bottom left
    crop = input_image.crop(box)
    crop.thumbnail(size, Image.ANTIALIAS)
    crop.save('3' + str(list[i]) + '.png')
    box = (width/2, height/2, width, height) #bottom right
    crop = input_image.crop(box)
    crop.thumbnail(size, Image.ANTIALIAS)
    crop.save('4' + str(list[i]) + '.png')
'''