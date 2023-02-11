from PIL import Image
import os


def jpg2pdf(jpgFile):
    path,fileName = jpgFile.rsplit('\\',1)
    preName,postName = fileName.rsplit('.',1)


    img = Image.open(jpgFile)
    return img.save(path+"\\"+preName+'.pdf', "PDF", resolution=100.0, save_all=True)


def jpg2pdfByPath(pathName):
    files = os.listdir(pathName)
    for f in files:
        if f.lower().find(".jpg")>0 :

            jpg2pdf(pathName+'\\'+f)

jpg2pdfByPath(r'C:\\Users\\hanstan\\Desktop\\PD\\submit\\a1')
