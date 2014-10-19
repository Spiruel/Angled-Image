from PIL import Image
import getopt, sys

args = sys.argv
ImageFileList = []
MasterWidth = 0
MasterHeight = 0
filename = ""
row = True
realign = False
colour = 'black'

print """
Usage: python imageconnector.py  [OPTIONS] [FILENAME] [FILE1] [FILE2] ...
Combines [FILE]s into one file called [FILENAME]

OPTIONS:

-o <r/c>    Orientation. Stitch images into a row or a column. Unless specified otherwise, orientation is row.
-a <offset> Alignment. Offsets the whole row by the given amount in pixels.
-c <colour> Background colour. Change background fill colour. Unless specified otherwise, background colour is black.
"""

def main(argv):
    global args, MasterWidth, MasterHeight, ImageFileList, filename, deletename, row, realign, colour
    try:
        opts, args_files = getopt.getopt(argv, 'o:c:a:')
    except getopt.GetoptError:
        print "Illegal arguments!"
        sys.exit(-1)

    if '-o' in args:
        index = args.index('-o')
        cr = args[index + 1]
        if cr == 'r':
            row = True
        elif cr == 'c':
            row = False
        else: 
            row == True
       
    if '-a' in args:
        index = args.index('-a')
        alignValue = int(args[index + 1])
        realign = True
            
    if '-c' in args:
        index = args.index('-c')
        colour = args[index + 1]

    filename = args_files.pop(0)
    
    if row == True:
        rc = 'row'
    else:
        rc = 'column'
    if realign == True:
        al = ' with an offset of ' + str(alignValue) + ' pixels:'
    else:
        al = ':'
    print 'Combining the following images in a', rc + al
    if row:
        for x in args_files:
            try:
                im = Image.open(x)
                print(x)
               
                MasterWidth += im.size[0]
                if im.size[1] > MasterHeight:
                    MasterHeight = im.size[1]
                else:
                    MasterHeight = MasterHeight
              
              
                ImageFileList.append(x)  
            except:
                raise
                         
        final_image = Image.new("RGB", (MasterWidth, MasterHeight), colour)
        if realign == True:
            offset = alignValue
        else:
            offset = 0
        for x in ImageFileList:
            if realign == True:
                if ImageFileList.index(x) == len(ImageFileList) - 1:
                    temp_image = Image.open(x)
                    width,height = temp_image.size
                    box = (0, 0, width - alignValue, height)
                    reduced_im = temp_image.crop(box)
                    final_image.paste(temp_image, (offset, 0))
                    box = (width - alignValue, 0, width, height)
                    cropped_im = temp_image.crop(box)
                    final_image.paste(cropped_im, (0, 0))
                else:
                    temp_image = Image.open(x)
                    final_image.paste(temp_image, (offset, 0))
                    offset += temp_image.size[0]
            else:
                temp_image = Image.open(x)
                final_image.paste(temp_image, (offset, 0))
                offset += temp_image.size[0]

        final_image.save(filename)
    else:
        for x in args_files:
            try:
                im = Image.open(x)
                print(x)
        
        
                MasterHeight += im.size[1]
                if im.size[0] > MasterWidth:
                    MasterWidth = im.size[0]
                else:
                    MasterWidth = MasterWidth
         
                ImageFileList.append(x)  
            except:
                raise
        
        final_image = Image.new("RGB", (MasterWidth, MasterHeight), colour)
        offset = 0
        for x in ImageFileList:
            temp_image = Image.open(x)
            final_image.paste(temp_image, (0, offset))
            offset += temp_image.size[1]
                        
        final_image.save(filename)
        
if __name__ == "__main__":
  try:
    main(sys.argv[1:])
  except IOError:
    print 'One of more of the input image files is not valid.'
    sys.exit(-1)
    
  except SystemExit:
    pass

  except ValueError:
    print 'Not a valid colour value.'