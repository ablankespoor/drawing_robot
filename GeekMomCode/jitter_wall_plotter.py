#!/usr/bin/env python

# Serial comminucation
import serial

# Image processing/Array maniuplation
from PIL import Image
##import PIL.ImageOps
import numpy as np
from scipy import ndimage as ndimage

# Display of image and drawing progress
import pygame

# GUI interface
import tkinter
from tkinter import filedialog

# math
import math

# Plotting
import matplotlib.pyplot as plt


# Physical canvas dimensions - should probably read these from Arduino.  Units are 0.1 mm
canvasorigin = [2000, 2700]
canvassize = [4000, 3500]
canvascenter = [canvasorigin[0] + canvassize[0]/2, canvasorigin[1] + canvassize[1]/2]


# Maximum pixels allowed per side in the image to plot
# Eventually we want to make this a user input to allow for greater image detail
# We assume all pixels are square
MAXIMSIZE = 64

CMD_UNKNOWN = 0
CMD_OK = 1
CMD_CONSOLE = 2

PEN_UP = 0
PEN_DOWN = 1

DIR_CW = 0
DIR_CCW = 1

IMG_SCALAR_SHADED = 0
IMG_SCALAR_CROSSHATCH = 1
IMG_VECTOR_SVG = 2

OS_WINDOWS = 0
OS_RASPBIAN = 1
#Set this to the current machine OS
CURRENT_OS = OS_RASPBIAN

# Helper functions
# Returns rounded interger
def rint(x):
    return int(round(x))


                                                  
                                                   
# Converts a pygame surface to grayscale values
def grayscale_surface(surf):
    width, height = surf.get_size()
    for x in range(width):
        for y in range(height):
            red, green, blue, alpha = surf.get_at((x, y))
            L = 0.3 * red + 0.59 * green + 0.11 * blue
            gs_color = (L, L, L, alpha)
            surf.set_at((x, y), gs_color)
    return surf

# Set any transparent pixels to white in a PIL image 
def transparent_to_white(im):
    if (im.mode == 'RGBA'):
        bottom_im = Image.new("RGBA", (im.size[0], im.size[1]), "white") 
        r,g,b,a = im.split()
        im = Image.merge("RGB", (r, g, b))
        mask = Image.merge("L", (a, ))
        bottom_im.paste(im, (0,0), mask)
        return bottom_im
    else:
        return im



# Inverts the colors in a Surface Array - by converting to image
def invert_surface(sur):
    inv = pygame.Surface(sur.get_rect().size, pygame.SRCALPHA)
    inv.fill((255,255,255,255))
    inv.blit(sur, (0,0), None, pygame.BLEND_RGB_SUB)
    return inv
    

# Takes a PIL image, then displays it with pygame and returns the pygame surface
def showimg(img):
    window_size = (640, 480)
    if (CURRENT_OS == OS_RASPBIAN):
        window_size = (480, 320)
    img_size = img.size

    # Maximize the size of the displayed image
    scalefactor = min(window_size[0]/img_size[0], window_size[1]/img_size[1])

    # Create the window for the display
    screen = pygame.display.set_mode(window_size)

    # Convert PIL image to Pygame Surface
    # Pygame doesn't handle 8-bit images well, so convert to RBG if it is Grayscale
    if (img.mode == 'L'):
        img = img.convert('RGB')
    # imstring = img.tostring()    # .tostring() is deprecated?
    imstring = img.tobytes()
    sur = pygame.image.fromstring(imstring, img.size, img.mode)
    # Convert to grayscale
    sur = grayscale_surface(sur)

    # Scale the image up to an appropriate size for display
    (w, h) = sur.get_size()
    factor = int(scalefactor)
    #print("factor = ", factor)
    sur = pygame.transform.scale(sur, (w*factor, h*factor))

    screen.blit(sur, (0, 0))
    pygame.display.flip()

    



# im is a 2-D numpy array containing image values.  Takes a numpy array
def make_shaded_image(scalefactor, imarray):
    
    # Maximum intensity of image pixel
    MAXINTENSITY = math.ceil(imarray.max())

    imsize = imarray.shape
    imwidth = imsize[1]
    imheight = imsize[0]
    startx = canvascenter[0] - imwidth*scalefactor/2
    starty = canvascenter[1] - imheight*scalefactor/2
    lastx = startx
    lasty = starty

    # First instruction sends pen to starting point
    instructions = [['M', rint(startx), rint(starty)]]

    # Maximum number of strokes per pixel.  Calculted to make stroke size a minumum of around 1 mm
    MAXSTROKES = int(canvassize[0]/(MAXIMSIZE*10))

    # Try larger MAXSTROKES to see what happens (usually = 6)
    #MAXSTROKES = 10
    
    jitterheight = 2*scalefactor/3           #Height of pen strokes
    direction = 1
    # Step through rows of the image
    for i, row in enumerate(imarray):
        # Step through pixels in the row
        for j, pixel in (enumerate(row) if (direction > 0) else reversed(list(enumerate(row)))):
            # Invert image intensity (white=low/dark=high)
            intensity = (MAXINTENSITY - pixel)/MAXINTENSITY
            jitter = rint(MAXSTROKES*intensity) 
            if jitter == 0:
                lastx = lastx + direction*scalefactor
                instructions.append(['L', rint(lastx), rint(lasty)])
            else:
                jitterwidth = scalefactor/jitter
                dx = jitterwidth/2
                for k in range (0, jitter):
                    instructions.append(['L', rint(lastx), rint(lasty + jitterheight)])
                    instructions.append(['L', rint(lastx + direction*dx), rint(lasty + jitterheight)])
                    instructions.append(['L', rint(lastx + direction*dx), rint(lasty)])
                    instructions.append(['L', rint(lastx + direction*2*dx), rint(lasty)])
                    lastx = lastx + direction*jitterwidth
                    # Next pixel
        lasty = starty + (i+1)*scalefactor
        direction = -1*direction
        #Lift the pen carriage up to get to the new line
        instructions.append(['M', rint(lastx), rint(lasty)])
        
    # Get the pen carriage up and out of the way when done
    #instructions.append(['M', canvasorigin[0], canvasorigin[1]])

    return instructions

# Create instructions list from image
def scalarimage(imfile, shadetype):

    # Import and manipulate the picture
    im = Image.open(imfile)

    # See if aspect ratio of image is greater or less than canvas aspect ratio.
    # Then scalefactor up the image to MAXIMSIZE pixels on the largest side.
    # Add a slight margin for error to make sure we don't exceed boundaries
    scalefactor = 1
    margin = 200
    if im.size[1]/im.size[0] > canvassize[1]/canvassize[0]:
        scalefactor = (canvassize[1] - margin)/MAXIMSIZE
    else:
        scalefactor = (canvassize[0] - margin)/MAXIMSIZE
    im.thumbnail((MAXIMSIZE, MAXIMSIZE), Image.ANTIALIAS)    

    # Get new size
    imsize = im.size
    print("imsize = ", imsize)
    print("scalefactor = ", scalefactor)

    #If the image has an alpha channel set all transparent pixels to white
    im = transparent_to_white(im)

    # Show the image on the screen
    #showimg(im)

    # Convert image to array
    imarray = np.array(im.convert('L'))

    
    instructions = []
    instructions = make_shaded_image(scalefactor, imarray)

    return instructions





#def main():

# Show askopenfilename dialog without the Tkinter window
#root = tkinter.Tk()
#root.withdraw()

filename = "C:/Users/Adam/Documents/drawing_robot/DrawingInputFiles/puma.jpg"
print(filename)

# M -> move with the pen up,
# L -> line
# x y -> coordinates, with 0.1mm resolution 
instructions = []
instructions = scalarimage(filename, IMG_SCALAR_SHADED)

print()
print("instructions: ", instructions[:10])

# Convert list of instructions to xy coordinate array
instructions_xy = []
for row in instructions:
    instructions_xy.append(row[1:])
xy = np.array(instructions_xy)/10
xy = xy - xy[0]
xy = -xy
print()
print("instructions_xy: ")
print(xy[0:10])


plt.plot(xy[:,0],xy[:,1],'-')
plt.plot(xy[0,0],xy[0,1],'or')
plt.grid(True)
plt.show()
        

#main()
    

