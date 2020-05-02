# Image Encryption in Mobile Devices

**Image encryption** can be defined in such a way that it is the process of encoding secret image with the help of some encryption algorithm in such a way that unauthorized users can't access it. So, it is quite useful for communicate confidential information for which countless procedures are unearthed. 

It can also be used as an app to encrypt,hide personal photos on smartphones. This is the subject of this repository.

**If the algorithm is explained simply:**

* Random numbers are generated for each row and column pixels at certain intervals for encryption. 
``` 
# converted Row&Column into an one-dimensional array
# len(kr) = number of image's rows, len(kc) = number of image's cols
Kr = [randint(0, pow(2, alpha) - 1) for i in range(m)] # random int between 0,2^alpha -1
Kc = [randint(0, pow(2, alpha) - 1) for i in range(n)] 
``` 

* Real image pixels are rolled  along the random matrix values. Basically what happens is that elements of the input array are being shifted.
```
# Kr[i] values come first from the last in r array
r[i] = numpy.roll(r[i], Kr[i]) #'r' rolling with 'Kr[i]' shift, shifting Kr[i] places
g[i] = numpy.roll(g[i], Kr[i]) #green
b[i] = numpy.roll(b[i], Kr[i]) #blue
```

* XOR operation is applied for rolled(shifted) values and random values.
```
# XOR(^)
r[i][j] = r[i][j] ^ Kc[j] # rolled(shifted) red values XOR random column values
r[i][j] = r[i][j] ^ Kr[i] # rolled red values XOR random row values
```

* Last, These values are pieced together and written in place of each pixel value of the image. In this way, values to be entered randomly instead of the main pixel values of the image make the image encrypted .

```
for i in range(m):
  for j in range(n):
    pix[i, j] = (r[i][j], g[i][j], b[i][j]) # piece together
```                    
<p align="center">
<img src="Encrypt_1.png" width="800" height="232" ><br> 
   <b>Encrypted Image Sample</b>
</p>	

Multilevel encryption is done by changing the random pixel value range generated. Such as, (0,15) **low**, (0,63) **medium**, (0,255) **high** security level.
``` 
alpha = int(self.secr) # get checkbox selection

# if alpha = 4(Low) , generate numbers between (0,15)
# alpha = 6(Medium), generate numbers between (0,63)
# alpha = 8(High), generate numbers between (0,255) depending on the following

Kr,Kc = [randint(0, pow(2, alpha) - 1) for i in range(m,n)] 
``` 
<p align="center">
<img src="Encrypt_2.jpg" width="530" height="430" ><br> 
  <b>Multi-level Outputs</b>
</p>	

### KİVY

<a href="https://kivy.org/#homeKivy">**Kivy**</a> is a free and open source Python library for developing mobile apps and other multitouch application software with a natural user interface. The fundamental idea behind <a href="https://kivy.org/#homeKivy">Kivy</a> is to enable the developer to build an app once and use it across all devices, making the code reusable and deployable, allowing for quick and easy interaction design and rapid prototyping. 

So, you can create your own apk or ipa by following these paths for your **Android** and **IOS** devices.<br>
For Android devices(apk): <br>
https://kivy.org/doc/stable/guide/packaging-android.html <br>
For IOS devices(ipa): <br>
https://kivy.org/doc/stable/guide/packaging-ios.html <br>


## Installation
* **Clone** this repository to your local machine using ` https://github.com/aunluhisarcikli/image-encryption.git `

* **Requirements** are :
  * Python
  * Kivy
  * Pillow
      
      
## Sample
<img src="demo.gif" width="720" height="480">  


                    
