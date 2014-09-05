'''
Command line wrapper to help interpret centres in the box.

Turn on or off plots of the existing centres, the four slices we are looking for, the new centres that seem to fit on the slices,
and the camera view on each of these new centres.

-existingcentres <t/f> 
-fourslices <t/f> 
-newcentres <t/f> 
-centresview <t/f> 

'''

import matplotlib.pyplot as pyplot
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import random
import sys

angle = np.arctan2(1,4)
xangle = np.arctan2(1,4)
width = 100/np.cos(angle)
print 'angle:', angle*(180/np.pi)
print 'xangle:', xangle*(180/np.pi)
print 'width:', width

existingcentres = False
fourslices = False
newcentres = False
centresview = False

def totuple(a):
    try:
        return tuple(totuple(i) for i in a)
    except TypeError:
        return a
        
def normalise(vector):
    modulus = np.sqrt(vector[0]**2+vector[1]**2+vector[2])
    return np.array([vector[0]/modulus, vector[1]/modulus, vector[2]/modulus])

def plotSquare(ax,cx,cy,cz, yaw, pitch, diameter):

    colour1 = random.randint(0,255)/256.0
    colour2 = random.randint(0,255)/256.0
    colour3 = random.randint(0,255)/256.0

    centre = np.array([cx,cy,cz])
    radius = diameter/2
    #0,0,0 to 100,25,125 diff
    #100,25,125 /2
    #50,12.5,62.5 /50
    #1.0,0.25,1.25
    d1offset = np.array([np.cos(pitch)*radius,(np.cos(yaw)*radius)+(np.sin(pitch)*radius),np.sin(yaw)*radius])

    c1 = centre - d1offset
    c2 = centre + d1offset

    #100,0,25 to 0,25,100 diff
    #-100,25,75 /2
    #-50,12.5,37.5 /50
    #-1.0,0.25,0.75
    d2offset = np.array([-np.cos(yaw)*radius,(np.cos(pitch)*radius)-(np.sin(yaw)*radius),np.sin(pitch)*radius])

    c3 = centre - d2offset
    c4 = centre + d2offset

    test = False
    if (centre[0] - radius) < 0.0 and (centre[1] - radius) < 0.0:
        test = True
        
        walkX = normalise(c3 - c1)
        walkY = normalise(c1 - c4)

        partitionC1Edge = centre + radius*walkX
        
        lambdaValue = partitionC1Edge[1] / walkY[1];
        
        partitionC1 = partitionC1Edge - lambdaValue*walkY
        
        partitionC2Edge = c1 + lambdaValue*walkY

        partitionC4Up = centre - radius*walkY
        partitionC4Down = centre + radius*walkY
        
        verts = [[totuple(centre),totuple(partitionC1),totuple(c2),totuple(partitionC4Up)]]
        ax.add_collection3d(Poly3DCollection(verts, facecolors=[colour1,colour2,colour3]))
        
        displaceY = np.array([0,-100,-25])
        displaceX = np.array([100,25,0])
        
        displaceXY = displaceX - displaceY
        
        verts = [[totuple(partitionC4Down-displaceY),totuple(c3-displaceY),totuple(partitionC1-displaceY),totuple(centre-displaceY)]]
        ax.add_collection3d(Poly3DCollection(verts, facecolors=[colour1,colour2,colour3]))
        
        verts = [[totuple(partitionC2Edge+displaceX),totuple(partitionC4Down+displaceX),totuple(partitionC4Up+displaceX),totuple(c4+displaceX)]]
        ax.add_collection3d(Poly3DCollection(verts, facecolors=[colour1,colour2,colour3]))
        
        verts = [[totuple(c1+displaceXY),totuple(partitionC4Down+displaceXY),totuple(partitionC2Edge+displaceXY)]]
        ax.add_collection3d(Poly3DCollection(verts, facecolors=[colour1,colour2,colour3]))
        
        #ax.scatter([partitionC1[0], partitionC4Up[0], centre[0], partitionC4Down[0], partitionC1Edge[0]], [partitionC1[1], partitionC4Up[1], centre[1], partitionC4Down[1], partitionC1Edge[1]], [partitionC1[2], partitionC4Up[2], centre[2], partitionC4Down[2], partitionC1Edge[2]], zdir='z', s=20, c='k', zorder=1)
        
    elif (centre[0] - radius) < 0.0:
        test = True

        walk = c3 - c1
        lambdaValue = -c1[0] / walk[0];

        partitionC1 = c1 + lambdaValue*walk

        lambdaValue = -c4[0] / walk[0];

        partitionC4 = c4 + lambdaValue*walk

        verts = [[totuple(partitionC1),totuple(c3),totuple(c2),totuple(partitionC4)]]
        ax.add_collection3d(Poly3DCollection(verts, facecolors=[colour1,colour2,colour3]))

        displace = np.array([100,25,0])
        #displace = normalise(walk)*100

        verts = [[totuple(c1+displace),totuple(partitionC1+displace),totuple(partitionC4+displace),totuple(c4+displace)]]
        ax.add_collection3d(Poly3DCollection(verts, facecolors=[colour1,colour2,colour3]))

    elif (centre[1] - radius) < 0.0:
        test = True

        walk = c1 - c4
        lambdaValue = -c4[1] / walk[1];

        partitionC4 = c4 + lambdaValue*walk

        lambdaValue = -c2[1] / walk[1];

        partitionC2 = c2 + lambdaValue*walk

        #c4 = partitionC4
        #c2 = partitionC2

        verts = [[totuple(partitionC4),totuple(partitionC2),totuple(c2),totuple(c4)]]
        ax.add_collection3d(Poly3DCollection(verts, facecolors=[colour1,colour2,colour3]))
        
        #displace = (normalise(walk)*100).astype(int)
        displace = np.array([0,-100,-25])
        #print (normalise(walk)*100).astype(int)
        #displace = normalise(walk)*100
        
        verts = [[totuple(c1-displace),totuple(c3-displace),totuple(partitionC2-displace),totuple(partitionC4-displace)]]
        ax.add_collection3d(Poly3DCollection(verts, facecolors=[colour1,colour2,colour3]))

    if test == False:
        verts = [[totuple(c1),totuple(c3),totuple(c2),totuple(c4)]]
        ax.add_collection3d(Poly3DCollection(verts, facecolors=[colour1,colour2,colour3]))

args = sys.argv

if '-existingcentres' in args:
    index = args.index('-existingcentres')
    tf = args[index + 1]

    if tf == 't':
        existingcentres = True

    elif tf == 'f':
        existingcentres = False

    else:
        existingcentres = False
        
if '-fourslices' in args:
    index = args.index('-fourslices')
    tf = args[index + 1]

    if tf == 't':
        fourslices = True

    elif tf == 'f':
        fourslices = False

    else:
        fourslices = False
        
if '-newcentres' in args:
    index = args.index('-newcentres')
    tf = args[index + 1]

    if tf == 't':
        newcentres = True

    elif tf == 'f':
        newcentres = False

    else:
        newcentres = False
        
if '-centresview' in args:
    index = args.index('-centresview')
    tf = args[index + 1]

    if tf == 't':
        centresview = True

    elif tf == 'f':
        centresview = False

    else:
        centresview = False

if fourslices and centresview:
    print '>>>The four slices and centre views are being obscured. \n>>>Only have one visible at a time please!'

x1       = [0, 0, 0, 0, 50, 50, 50, 50]
y1       = [50,50,50,50,50,50,50,50]
z1       = [12.5,37.5,62.5,87.5,25,50,75,0]

x2   = [0,0,0,0,0,0,0,0,50,50,50,50,50,50,50,50]
y2   = [0,50,0,50,0,50,0,50,0,50,0,50,0,50,0,50]
z2  = [0,12.5,25,37.5,50,62.5,75,87.5,12.5,25,37.5,50,62.5,75,87.5,0]

fig = pyplot.figure()
ax  = fig.add_subplot(111, projection = '3d')

ax.set_xlim(0,100)
ax.set_ylim(0,100)
ax.set_zlim(0,100)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
#ax.view_init(elev=90, azim=90)
#ax.scatter(x1, y1, z1, zdir='z', s=20, c='g') 
if existingcentres:
    ax.scatter(x2, y2, z2, zdir='z', s=20, c='r') #EXISTING COORDINATES notice how they do not lie on the plane

if fourslices:
    xa = [0,100,100,0]
    ya = [0,0,100,100]
    za = [0,-6.25,18.75,25]
    verts = [zip(xa,ya,za)]
    ax.add_collection3d(Poly3DCollection(verts))

    xb = [0,100,100,0]
    yb = [0,0,100,100]
    zb = [25,-6.25+25,18.75+25,50]
    verts = [zip(xb,yb,zb)]
    ax.add_collection3d(Poly3DCollection(verts))

    xc = [0,100,100,0]
    yc = [0,0,100,100]
    zc = [50,-6.25+25*2,18.75+25*2,75]
    verts = [zip(xc,yc,zc)]
    ax.add_collection3d(Poly3DCollection(verts))

    xd = [0,100,100,0]
    yd = [0,0,100,100]
    zd = [75,-6.25+25*3,18.75+25*3,100]
    verts = [zip(xd,yd,zd)]
    ax.add_collection3d(Poly3DCollection(verts))
        
x = [0]
y = [0]
z = [0]

for i in range(1,32):
    new_x = x[(len(x)-1)] + 50
    new_y = y[(len(y)-1)] + 12.5
    new_z = z[(len(z)-1)] 
    if new_x >= 100:
        new_x = new_x - 100
        new_z = new_z + 6.25
    if new_y >= 100:
        new_y = new_y - 100
    if new_z >= 100:
        new_z = new_z - 100
        
    if new_x == 0 and new_y == 0 and new_z == 0:
        print 'centres are wrapping round on themselves!', i
    
    x.append(new_x)
    y.append(new_y)
    z.append(new_z)

#print zip(x,y,z)
    
count = 0
for i in range(2,32,4):

    pos = i - count

    x.pop(pos)
    x.pop(pos)
    y.pop(pos)
    y.pop(pos)
    z.pop(pos)
    z.pop(pos)
    #print i
    #print i+1
    count = count + 2
   
#print zip(x,y,z)
if newcentres:
    ax.scatter(x, y, z, zdir='z', s=20, c='k', zorder=1)

if centresview:
    storedcoordinates = zip(x,y,z)
    for x,y,z in storedcoordinates:
        plotSquare(ax,x,y,z,xangle,angle, width/2)
    
pyplot.show()