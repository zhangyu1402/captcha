from PIL import Image
import hashlib
import time
import os
import math
iconset = ['0','1','2','3','4','5','6','7','8','9','0','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
class VectorCompare:
    def magnitude(self,concordance):
        total = 0
        for word,count in concordance.items():
            total += count ** 2
        return math.sqrt(total)
    def relation(self,concordance1,concordance2):
        relevance = 0
        topvalue = 0
        for word ,count in concordance1.items():
            if word in concordance2:
                topvalue += count * concordance2[word]
        return topvalue/(self.magnitude(concordance1)*self.magnitude(concordance2))

def buildvector(image):
    d1 ={}
    count = 0
    for i in image.getdata():
        d1[count] = i
        count +=1
    return d1
v = VectorCompare()
#加载训练集
imageset = []
for letter in iconset:
    for image in os.listdir('./iconset/%s/'%(letter)):
        temp = []
        if image != "Thumbs.db" and image != ".DS_Store":
            temp.append(buildvector(Image.open("./iconset/%s/%s"%(letter,image))))
        imageset.append({letter:temp})#temp:每个字母的特征向量，list

#加载图片
image = Image.open("captcha.gif")
image.convert("P")
image2 = Image.new("P",image.size,255)

#将原图像转换成黑白二值图像
for x in range(image.size[0]):
    for y in range(image.size[1]):
        pix = image.getpixel((x,y))
        if pix == 220 or pix == 227:
            image2.putpixel((x,y),0)
#分割字母
inletter = False
foundletter=False
start = 0
end = 0
letters = []#letter中存的是每个字母的x轴范围，tuple
for y in range(image2.size[0]): 
    for x in range(image2.size[1]):
        pix = image2.getpixel((y,x))
        if pix != 255:
            inletter = True
    if foundletter == False and inletter == True:
        foundletter = True
        start = y

    if foundletter == True and inletter == False:
        foundletter = False
        end = y
        letters.append((start,end))

    inletter=False

count = 0
for letter in letters:
    image3 = image2.crop((letter[0],0,letter[1],image2.size[1]))
    guess = []
    for image in imageset:#每一个分割出的字母和训练集中的所有字母的特征向量对比。选出最相似的
        for x,y in image.items():
            if len(y) != 0:
                guess.append( (v.relation(y[0],buildvector(image3)),x) )

    guess.sort(reverse=True)
    print(guess[0])
    count +=1

