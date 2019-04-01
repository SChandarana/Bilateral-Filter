import cv2
import numpy as np
import math
#this function creates a gaussian value for a given sigma and x
def gauss(x,sigma):
    temp =  1 / (sigma * math.sqrt(2 * math.pi))
    return temp * math.exp(-(x**2/(2 * sigma**2)))
#this function gets all the neighbours of a given pixel
def getNeighbourhood(x,y,w,h,diameter):
    neighbourhood = []
    offset = (diameter - 1)/2
    minXOff = int(max(0,x - offset)) #this part will check if the kernel goes off the edge
    maxXOff = int(min(x + offset,w - 1))
    minYOff = int(max(0, y - offset))
    maxYOff = int(min(y + offset, h - 1))
    for i in range(minXOff,maxXOff + 1):
        for j in range(minYOff,maxYOff + 1):
            neighbourhood.append([i,j])
    return neighbourhood

def bilateral(imageFlash,imageNoFlash,sigmaS, sigmaI, diameter): # the main filter
    filtered = imageFlash.copy()
    filtered.fill(0) #creating an empty copy of the image
    height,width,channels = imageFlash.shape #getting the dimensions
    
    for i in range(height): #looping through all the pixels
    
        for j in range(width):
            newPixel = [0 for i in range(channels)] #splitting the pixel into it's colour channels and working separately on each
            normalise = [0 for i in range(channels)]
            weight = [0 for i in range(channels)]
            neighbourhood = getNeighbourhood(j,i,width,height,diameter)
            for [x,y] in neighbourhood: #running each part of the filter on every neighbour of the pixel
                gaussS = gauss(math.sqrt((y-i)**2 + (x-j)**2),sigmaS)
                #sigma space is the same for all colour channels so only needs to happen once 
                for k in range(channels):
                    gaussI = gauss(int(imageFlash[y,x][k]) - int(imageFlash[i,j][k]), sigmaI)#working out intensity
                    weight[k] = gaussI * gaussS 
                    newPixel[k] += imageNoFlash[y,x][k] * weight[k] #works out the value for the new pixel
                    normalise[k] += weight[k] #keeps account of the normalising factor (so the overall pixel value stays the same)
                    
            for k in range(channels):
                
                newPixel[k] = newPixel[k]/normalise[k] #normalises the pixel
                
            filtered[i,j] = newPixel #adds the new pixel to the picture
            
    return filtered
def main():
    image1 = 'test3b.jpg' #loading the images
    image2 = 'test3a.jpg'
    sigmaS = 50 #assigning variables
    sigmaI = 10
    diameter = 9
    imageFlash = cv2.imread(image1,cv2.IMREAD_UNCHANGED) #reading images
    imageNoFlash = cv2.imread(image2,cv2.IMREAD_UNCHANGED)
    filtered = bilateral(imageFlash,imageNoFlash,sigmaS,sigmaI,diameter) #filtering
    highS = bilateral(imageFlash,imageNoFlash,1000,sigmaI,diameter) #testing different parameters
    highI = bilateral(imageFlash,imageNoFlash,20,100,diameter)
    lowerD = bilateral(imageFlash,imageNoFlash,sigmaS,sigmaI,5)
    cv2.imwrite("result.jpg", filtered)#writing the results
    cv2.imwrite("highSJ.jpg",highS)
    cv2.imwrite("highIJ.jpg",highI)
    cv2.imwrite("lowerDJ.jpg",lowerD)
