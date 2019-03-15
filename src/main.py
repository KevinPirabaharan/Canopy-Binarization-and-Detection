#Canopy Binarization and Detection
#Kevin Pirabaharan (0946212)
#This program creates binarized gray images from coloured images of canopies
#to detect the best algorithm for detecting canopy cover
#As of now NDI and NDI mod code is not working 

from __future__ import division
from imageIO import *
from imthr_lib import*
from PIL import Image
import time

# CIVE = Colour Index of Vegetation Extraction
# CIVE algorithm uses index of
# Z = 0.441*R - 0.811*G + 0.385*B + 18.78745
def imageCIVE(imageName, saveImage):
    red, green, blue = imread_colour(imageName)

    im = Image.open(imageName)
    height, width = im.size

    imgCIVE = np.zeros((width,height))

    for i in range(0, width-1):
        for j in range(0, height-1):
            imgCIVE[i,j] = round(0.441*red[i,j] - 0.811*green[i,j] + 0.385*blue[i,j] + 18.78745)
            if (imgCIVE[i,j] > 255):
                imgCIVE[i,j] = 255
            elif (imgCIVE[i,j] < 0):
                imgCIVE[i,j] = 0

    thr = otsu(imgCIVE)
    imgCIVEOtsu = im2bw(imgCIVE, thr)

    for i in range(0, width-1):
        for j in range(0, height-1):
            if (imgCIVEOtsu[i,j] == 0):
                imgCIVEOtsu[i,j] = 255
            else:
                imgCIVEOtsu[i,j] = 0

    imwrite_gray(saveImage, imgCIVEOtsu)
    print("Done CIVE")

# ExGSubR = Excessive Green Subtract Red Index
# Uses an index of Z = ExG - ExR, where ExG = 2g - r - b, ExR = 1.4r - b, and
# r = R* / (R* + G* + B*), g = G* / (R* + G* + B*), b = B* / (R* + G* + B*)
# Algorithm also uses an Otsu threshhold
def imageExGSubR(imageName, saveImage):
    red, green, blue = imread_colour(imageName)

    im = Image.open(imageName)
    height, width = im.size
    imgExGSubR = np.zeros((width,height))

    for i in range(0, width-1):
        for j in range(0, height-1):
            rgb = float(red[i,j]) + float(green[i,j]) + float(blue[i,j])

            if (rgb != 0):
                r = float(red[i,j]) / rgb
                g = float(green[i,j]) / rgb
                b = float(blue[i,j]) / rgb
            else:
                r = 0
                g = 0
                b = 0

            imgExG = 2*g - r - b
            imgExR = 1.4 * r - b
            imgSub = (imgExG - imgExR) * 255

            if(str(imgSub).isdigit):
                imgExGSubR[i,j] = round(imgSub)
            else:
                imgExGSubR[i,j] = 0

            if (imgExGSubR[i,j] > 255):
                imgExGSubR[i,j] = 255
            elif (imgExGSubR[i,j] < 0):
                imgExGSubR[i,j] = 0

    thr = otsu(imgExGSubR)
    imgExGSubROtsu = im2bw(imgExGSubR, thr)

    imwrite_gray(saveImage, imgExGSubROtsu)
    print("ExGSubR Done")

# NDI = Normalized Difference Index
# NDI = (green - red) / (green + red), and an Otsu threshold
def imageNDI(imageName, saveImage):
    red, green, blue = imread_colour(imageName)

    im = Image.open(imageName)
    height, width = im.size

    imgNDI = np.zeros((width,height))
    for i in range(0, width-1):
        for j in range(0, height-1):
            greenRed = float(green[i,j]) + float(red[i,j])
            if (greenRed == 0):
                imgNDI[i,j] = 0
            else:
                imgNDI[i,j] = ((float(green[i,j]) - float(red[i,j])) / greenRed)

    for k in range(0, width-1):
        for j in range(0, height-1):
            imgNDI[i,j] = (imgNDI[i,j] + 1.0) * 128
            if(str(imgNDI).isdigit):
                imgNDI[i,j] = round(imgNDI[i,j])
            else:
                imgNDI[i,j] = 0

            if (imgNDI[i,j] > 255):
                imgNDI[i,j] = 255
            elif (imgNDI[i,j] < 0):
                imgNDI[i,j] = 0

    thr = otsu(imgNDI)
    imgNDIOtsu = im2bw(imgNDI, thr)

    imwrite_gray(saveImage, imgNDIOtsu)
    print("NGI Done")

# NDI = Normalized Difference Index Modified
# NDI = (green - red - 2*blue) / (green + red + 2*blue), and uses an existing threshold (75)
def imageNDIMod(imageName, saveImage):
    red, green, blue = imread_colour(imageName)

    im = Image.open(imageName)
    height, width = im.size

    imgNDIMod = np.zeros((width,height))
    for i in range(0, width-1):
        for j in range(0, height-1):
            greenRedBlue = float(green[i,j]) + float(red[i,j]) + 2 * float(blue[i,j])
            if (greenRedBlue == 0):
                imgNDIMod[i,j] = 0
            else:
                imgNDIMod[i,j] = ((float(green[i,j]) - float(red[i,j]) - float(blue[i,j])) / greenRedBlue)

    for k in range(0, width-1):
        for j in range(0, height-1):
            imgNDIMod[i,j] = (imgNDIMod[i,j] + 1.0) * 128
            if(str(imgNDIMod).isdigit):
                imgNDIMod[i,j] = round(imgNDIMod[i,j])
            else:
                imgNDIMod[i,j] = 0

            if (imgNDIMod[i,j] > 255):
                imgNDIMod[i,j] = 255
            elif (imgNDIMod[i,j] < 0):
                imgNDIMod[i,j] = 0

    thr = otsu(imgNDIMod)
    imgNDIModOtsu = im2bw(imgNDIMod, 75)
    imwrite_gray(saveImage, imgNDIModOtsu)
    imgNDIModedBackup = im2bw(imgNDIMod, thr)
    backup = saveImage.replace("../images/processed/", "../images/processed/backup_")
    imwrite_gray(backup, imgNDIModedBackup)
    print("NGI Mod Done")

#Testing all algorithms through a suite of images, automated it to send results to folders and textfiles
def testAlgos():
    testfiles_list = ["../images/raw/oarmaturapress.jpg", "../images/raw/PeterKaminski.jpg", "../images/raw/test_image.jpg"]
    text_file = open("../data/runtimessdlg.txt", "w")
    for src_files in testfiles_list:
        print("File: " + src_files)
        #Running CIVE
        print("Starting CIVE")
        if (".p" in src_files):
            dest_files = src_files.replace('.p','_CIVE.p')
            dest_files = dest_files.replace('raw', 'processed')
        elif (".j" in src_files):
            dest_files = src_files.replace('.j','_CIVE.j')
            dest_files = dest_files.replace('raw', 'processed')
        elif (".t" in src_files):
            dest_files = src_files.replace('.t','_CIVE.t')
            dest_files = dest_files.replace('raw', 'processed')
        startTime = time.time()
        imageCIVE(src_files, dest_files)
        endTime = time.time()
        runtTime = (endTime - startTime)
        text_file.write("Time for CIVE agorithm for " + src_files + " is " + str(runtTime) + ".\n\n")

        #Running ExGSubR
        print("Starting ExGSubR")
        if (".p" in src_files):
            dest_files = src_files.replace('.p','_ExGSubR.p')
            dest_files = dest_files.replace('raw', 'processed')
        elif (".j" in src_files):
            dest_files = src_files.replace('.j','_ExGSubRE.j')
            dest_files = dest_files.replace('raw', 'processed')
        elif (".t" in src_files):
            dest_files = src_files.replace('.t','_ExGSubR.t')
            dest_files = dest_files.replace('raw', 'processed')
        startTime = time.time()
        imageExGSubR(src_files, dest_files)
        endTime = time.time()
        runtTime = (endTime - startTime)
        text_file.write("Time for ExGSubR agorithm for " + src_files + " is " + str(runtTime) + ".\n\n")

        #Running NDI
        print("Starting NDI")
        if (".p" in src_files):
            dest_files = src_files.replace('.p','_NDI.p')
            dest_files = dest_files.replace('raw', 'processed')
        elif (".j" in src_files):
            dest_files = src_files.replace('.j','_NDI.j')
            dest_files = dest_files.replace('raw', 'processed')
        elif (".t" in src_files):
            dest_files = src_files.replace('.t','_NDI.t')
            dest_files = dest_files.replace('raw', 'processed')
        startTime = time.time()
        imageNDI(src_files, dest_files)
        endTime = time.time()
        runtTime = (endTime - startTime)
        text_file.write("Time for NDI agorithm for " + src_files + " is " + str(runtTime) + ".\n\n")

        #Running NDIMod
        print("Starting NDIMod")
        if (".p" in src_files):
            dest_files = src_files.replace('.p','_NDIMod.p')
            dest_files = dest_files.replace('raw', 'processed')
        elif (".j" in src_files):
            dest_files = src_files.replace('.j','_NDIMod.j')
            dest_files = dest_files.replace('raw', 'processed')
        elif (".t" in src_files):
            dest_files = src_files.replace('.t','_NDIMod.t')
            dest_files = dest_files.replace('raw', 'processed')
        startTime = time.time()
        imageNDIMod(src_files, dest_files)
        endTime = time.time()
        runtTime = (endTime - startTime)
        text_file.write("Time for NDIMod agorithm for " + src_files + " is " + str(runtTime) + ".\n\n")

    text_file.close()

def compare():
    groundTruth = "../images/groundTruth/eg1stanfordBinaryMASK.tif"
    orig = imread_gray(groundTruth)
    origSize = Image.open(groundTruth)
    origHeight, origWidth = origSize.size

    test_list = ["../images/processed/eg1stanford_CIVE.tif", "../images/processed/eg1stanford_ExGSubR.tif", "../images/processed/eg1stanford_NDI.tif", "../images/processed/backup_eg1stanford_NDIMod.tif"]
    results_file = open("../data/comparisonResults.txt", "w")
    for file in test_list:
        comp = imread_gray(file)
        compSize = Image.open(file)
        compHeight, compWidth = compSize.size
        blackMatch = 0
        blackNotMatch = 0
        totalBlack = 0
        whiteMatch = 0
        whiteNotMatch = 0
        totalWhite = 0
        totalMatch = 0
        totalNotMatch = 0
        print("Comparing " + file + " vs. groundTruth")
        if (compHeight == origHeight) or (compWidth == origWidth):
            for i in range(0, origWidth-1):
                for j in range(0, origHeight-1):
                    if (orig[i,j] == comp[i,j]):
                        totalMatch = totalMatch + 1
                        if (orig[i,j] == 0):
                            blackMatch = blackMatch + 1
                        elif (orig[i,j] == 255):
                            whiteMatch = whiteMatch + 1
                    else:
                        totatNotMatch = totalNotMatch + 1
                        if (orig[i,j] == 0):
                            blackNotMatch = blackNotMatch + 1
                        elif (orig[i,j] == 255):
                            whiteNotMatch = whiteNotMatch + 1

            totalMatch = (totalMatch / orig.size) * 100
            totalNotMatch = 100 - totalMatch
            totalBlack = blackMatch + blackNotMatch
            blackNotMatch = (blackNotMatch / totalBlack) * 100
            totalWhite = whiteMatch + whiteNotMatch
            whiteNotMatch = (whiteNotMatch / totalWhite) * 100

        results_file.write("For file " + file + " vs groundTruth: " + "\nTotal Match: " + str(totalMatch) + "%\nTotal Unmatch: " + str(totalNotMatch) + "%\nBlacks Wrong: " + str(blackNotMatch) + "%\nWhites Wrong: " + str(whiteNotMatch) + "%\n \n \n")
    results_file.close()
    print("Comparison complete")


progExit = False
dname = fname.replace('.t','_NDI.t')
dname = dname.replace('raw', 'processed')
while (progExit == False):
    inp = raw_input("Execute Algorithm (1)CIVE, (2)ExGSubR, (3)NDI, (4)NDIMod, (t)est files, (c)ompare to groundtruth or (q)uit? ")
    if (inp.isdigit):
        print("Please drop image in the image/raw/ folder!")
        f = raw_input("Please drop image in the image/raw/ folder and enter filename")
        fname = "../image/raw/" + f
        if (inp == '1'):
            print("imageCIVE")
            imageCIVE(fname, dname)
        elif (inp == '2'):
            print("ExGSubR")
            imageExGSubR(fname, dname)
        elif (inp == '3'):
            print("NDI")
            imageNDI(fname, dname)
        elif (inp == '4'):
            print("NDIMod")
            imageNDIMod(fname, dname)
    elif (inp == 't') or (inp == 'T'):
        print("Testing Algorithms")
        testAlgos()
    elif (inp == 'c') or (inp == 'C'):
        print("Comparing with ground truth:")
        compare()
    elif (inp == "q") or (inp == "Q"):
        progExit = True
    else:
        print("Please check your input")
