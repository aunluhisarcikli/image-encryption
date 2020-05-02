
# import kivy module
import kivy
# this restrict the kivy version i.e
# below this kivy version you cannot
# use the app or software
kivy.require('1.8.0') # changeable

# base Class of your App inherits from the App class.
# app:always refers to the instance of your application
from kivy.app import App

# BoxLayout arranges widgets in either in
# a vertical fashion that is one on top of
# another or in a horizontal fashion
# that is one after another.
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from PIL import Image
from random import randint
import os
from shift_rotate import *

# create the layout class
class Filechooser(BoxLayout):

    def select(self, *args):
        super(Filechooser, self)
        try:
            self.label.text = args[1][0] # label_text = selected directory
            self.image.source = self.label.text # shows selected image
            self.path = args[1][0] # path of selected directory
            self.tail_name = os.path.split(self.path) # name of the selected file
            self.encr_image.source = '' # clear encrypted image
            self.button_text.text = "ENCRYPT"
            self.secr = self.secr.text
        except:
            pass

    def btn(self):
        try:

            im = Image.open(self.path) # open selected image
            pix = im.load() #load

            # Obtaining the RGB matrices
            r = []
            g = []
            b = []
            for i in range(im.size[0]):
                r.append([]) # [ [] ]
                g.append([]) # [ [] ]
                b.append([]) # [ [] ]
                for j in range(im.size[1]):
                    rgbPerPixel = pix[i, j]
                    r[i].append(rgbPerPixel[0]) # add red values
                    g[i].append(rgbPerPixel[1]) # add green values
                    b[i].append(rgbPerPixel[2]) # add blue values

            m = im.size[0] # width, row
            n = im.size[1] # height, column

            # Vectors Kr and Kc
            alpha = int(self.secr) # checkbox selection
            #if low alpha=4, medium alpha=6, high alpha=8

            # converted Row&Column into an one-dimensional array
            # len(kr) = number of image's rows, len(kc) = number of image's cols
            Kr = [randint(0, pow(2, alpha) - 1) for i in range(m)] # random int between 0,2^alpha -1
            Kc = [randint(0, pow(2, alpha) - 1) for i in range(n)] #default alpha=8 -> (0, 256 - 1) for max security
            ITER_MAX = 1

            #print('Vector Kr : ', Kr)
            #print('Vector Kc : ', Kc)

            '''
            #keep inform about the image in txt for decrypt later
            f = open('keys.txt', 'w+')
            f.write('Vector Kr : \n')
            for a in Kr:
                f.write(str(a) + '\n')
            f.write('Vector Kc : \n')
            for a in Kc:
                f.write(str(a) + '\n')
            f.write('ITER_MAX : \n')
            f.write(str(ITER_MAX) + '\n')
            '''

            for iterations in range(ITER_MAX):
                # For each row
                for i in range(m):
                    rTotalSum = sum(r[i]) # sum all red pixels
                    gTotalSum = sum(g[i]) # #sum all green pixels
                    bTotalSum = sum(b[i]) # #sum all blue pixels

                    rModulus = rTotalSum % 2 # mod(2)
                    gModulus = gTotalSum % 2 # mod(2)
                    bModulus = bTotalSum % 2 # mod(2)

                    if (rModulus == 0): # if divided by 2
                        # Kr[i] values ​​come first from the last in r array
                        r[i] = numpy.roll(r[i], Kr[i]) #'r' rolling with 'Kr[i]' shift, shifting Kr[i] places

                    else: # not leaves a remainder of 0
                        # Kr[i] values ​​go last from the first in r array
                        r[i] = numpy.roll(r[i], -Kr[i])  #'r' rolling with ' -Kr[i]' shift

                    if (gModulus == 0): # leaves a remainder of 0
                        g[i] = numpy.roll(g[i], Kr[i])
                    else:
                        g[i] = numpy.roll(g[i], -Kr[i])
                    if (bModulus == 0): # mod(2) == 0
                        b[i] = numpy.roll(b[i], Kr[i])
                    else:
                        b[i] = numpy.roll(b[i], -Kr[i])


                # For each column
                for i in range(n):
                    rTotalSum = 0
                    gTotalSum = 0
                    bTotalSum = 0
                    for j in range(m):
                        rTotalSum += r[j][i] #r[row][column]
                        gTotalSum += g[j][i] #g[row][column]
                        bTotalSum += b[j][i] #b[row][column]

                    rModulus = rTotalSum % 2 #mod(2)
                    gModulus = gTotalSum % 2
                    bModulus = bTotalSum % 2

                    # almost doing same things with rows
                    if (rModulus == 0): #leaves a remainder of 0
                        upshift(r, i, Kc[i]) #'r' rolling with ' -Kr[i]' shift
                    else:
                        downshift(r, i, Kc[i]) #'r' rolling with ' Kr[i]' shift
                    if (gModulus == 0): # if divided by 2
                        upshift(g, i, Kc[i])
                    else:
                        downshift(g, i, Kc[i]) # shifting Kr[i] places
                    if (bModulus == 0):
                        upshift(b, i, Kc[i])  #'b' rolling with ' -Kr[i]' shift
                    else:
                        downshift(b, i, Kc[i])

                # For each row
                for i in range(m):
                    for j in range(n):
                        if (i % 2 == 1): #if not divided by 2
                            # XOR(^)
                            r[i][j] = r[i][j] ^ Kc[j] # rolled(shifted) red values XOR random column values
                            g[i][j] = g[i][j] ^ Kc[j] # rolled green values XOR random column values
                            b[i][j] = b[i][j] ^ Kc[j] # rolled blue values XOR random column values
                        else:
                            # rotate180 means reversed
                            r[i][j] = r[i][j] ^ rotate180(Kc[j]) # rotate column values by 180
                            g[i][j] = g[i][j] ^ rotate180(Kc[j]) # reversed column values
                            b[i][j] = b[i][j] ^ rotate180(Kc[j]) # rolled blue values XOR reversed rand column values

                # For each column
                for j in range(n):
                    for i in range(m):
                        if (j % 2 == 0):
                            r[i][j] = r[i][j] ^ Kr[i] # rolled(shifted) red values XOR random row values
                            g[i][j] = g[i][j] ^ Kr[i] # rolled green values XOR random row values
                            b[i][j] = b[i][j] ^ Kr[i] # rolled blue values XOR random row values
                        else:
                            r[i][j] = r[i][j] ^ rotate180(Kr[i]) # rolled red values XOR reversed rand row values
                            g[i][j] = g[i][j] ^ rotate180(Kr[i]) # rolled green values XOR reversed rand row values
                            b[i][j] = b[i][j] ^ rotate180(Kr[i]) # rolled blue values XOR image's reversed rand row values

            for i in range(m):
                for j in range(n):
                    pix[i, j] = (r[i][j], g[i][j], b[i][j]) # piece together

            encrypted_image_path = 'encrypted_images/'+ str(self.tail_name[1])
            im.save(encrypted_image_path) # encrypted image
            self.encr_image.source = encrypted_image_path  # shows encrypted image
        except:
            pass


# Create the App class
class FileApp(App):
    def build(self):
        self.title = 'Image Encryption'
        return Filechooser()


# run the App
if __name__ == '__main__':
    FileApp().run()