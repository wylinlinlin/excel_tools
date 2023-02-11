import os
import fitz
import tkinter as tk
from tkinter import filedialog

# 转换前后的目录跟文件夹
covert_path = []
# 图片后缀文件名
pic_name_list = ['.jpg', '.png', '.bmp', '.jpeg', '.JPG', '.PNG', '.JPEG']


def get_file_path():
    """
    获取转换文件夹的跟目录，并保存目标跟目录到数组中
    """
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askdirectory()
    covert_path.append(file_path)
    covert_path.append(file_path + "-转换结果")


def covert_img_to_pdf(file_path):
    """
    打开路径文件夹并转换文件夹下的图片为PDF文件
    """
    docunames = os.listdir(file_path)
    doc = fitz.open()
    save = False
    for docuname in docunames:
        tempPath = file_path + "\\" + docuname
        if os.path.isdir(tempPath):
            covert_img_to_pdf(tempPath)
        else:
            file_suffix = os.path.splitext(docuname)[1]
            if file_suffix in pic_name_list:
                img = fitz.open(tempPath)  # 打开图片
                pdfbytes = img.convert_to_pdf()   # 使用图片创建单页的 PDF
                imgpdf = fitz.open("pdf", pdfbytes)
                doc.insert_pdf(imgpdf)
                save = True
    if save:
        file_name = os.path.basename(file_path) + ".pdf"
        new_file_path = file_path.replace(covert_path[0], covert_path[1])
        if os.path.exists(new_file_path) == False:
            os.makedirs(new_file_path)  # 多层创建目录
        doc.save(new_file_path + "\\" + file_name)


if __name__ == '__main__':
    get_file_path()
    covert_img_to_pdf(covert_path[0])
