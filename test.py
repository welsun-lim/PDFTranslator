# # import pdfplumber
# import pdfminer
# from pdfminer.converter import PDFPageAggregator
# from pdfminer.layout import LAParams, LTTextBoxHorizontal, LTLine, LTTextLineHorizontal, LTRect, LTCurve, LTImage, \
#     LTFigure, LTAnon, LTChar, LTTextBox, LTTextLine
# from pdfminer.pdfinterp import PDFTextExtractionNotAllowed, PDFResourceManager, PDFPageInterpreter
# from pdfminer.pdfparser import PDFParser, PDFDocument
# import pdf_tools
# import fitz
file = "Compact Descriptors for Video Analysis: the Emerging MPEG Standard.pdf"
"""
q=set()

def direct(x):
    # print(type(x))
    return {
        LTLine: print,
        LTTextBoxHorizontal: print,
        LTTextLineHorizontal: print,
        LTFigure: print
    }[type(x)]

with open(file, 'rb') as pd_file:
    # 用文件对象创建一个PDF文档分析器
    parser = PDFParser(pd_file)
    # 创建一个PDF文档
    doc = PDFDocument()
    # 连接分析器，与文档对象
    parser.set_document(doc)
    doc.set_parser(parser)
    # 提供初始化密码，如果没有密码，就创建一个空的字符串
    doc.initialize()
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建PDF资源管理器，来共享资源
        rsrcmgr = PDFResourceManager()
        # 创建一个PDF设备对象
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF解释其对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in doc.get_pages():
            interpreter.process_page(page)
            # 接受该页面的LTPage对象
            layout = device.get_result()
            # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象
            # 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等
            # 想要获取文本就获得对象的text属性，
            for x in layout:
                key = type(x)
                if key is LTLine:
                    pass
                if key is LTTextBoxHorizontal:
                    print(x.paragraphs(2))
                else:
                    print(key)
                    exit()

print(q)
"""




import fitz
import pdfplumber
from openpyxl import Workbook
from PIL import Image
import cv2
import numpy as np
import os

def analysis_table(pdf_file):

    #打開表格
    workbook = Workbook()
    sheet = workbook.active

    #打開pdf
    with pdfplumber.open(pdf_file) as pdf:
        #遍歷每頁pdf
        for page in pdf.pages:
            #提取表格信息
            table=page.extract_table( table_settings = {
            'vertical_strategy':"text",
            "horizontal_strategy":"text"})
            print(table)

            # 格式化表格數據
            for row in table:
                print(row)
                sheet.append(row)

    workbook.save(filename="2.xlsx")

def pixmap2array(pix):
    '''pixmap數據轉數組對象'''
    #獲取顏色空間
    cspace = pix.colorspace
    if cspace is None:
        mode = "L"
    elif cspace.n == 1:
        mode = "L" if pix.alpha == 0 else "LA"
    elif cspace.n == 3:
        mode = "RGB" if pix.alpha == 0 else "RGBA"
    else:
        mode = "CMYK"

    #將byte數據轉化為PIL格式
    img = Image.frombytes(mode, (pix.width, pix.height), pix.samples)
    #將PIL轉化為numpy格式，並將RGB顏色空間轉化為BGR
    img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)

    return img

def ananlysis_PDF(pdf_file):
    '''解析pdf信息'''

    # 判斷pdf是否存在
    if not os.path.exists(pdf_file):
        print("pdf文件不存在")
        return;

    # 打開pdf文件
    doc=fitz.open(pdf_file)

    #遍歷pdf，提取信息
    for page in doc:
        words=page.getTextWords()
        for w in words:
            print(fitz.Rect(w[:4]),w[4])

        img_list=page.getImageList()
        i=0
        for img in img_list:
            print(fitz.Rect(img[:4]))
            pix=fitz.Pixmap(doc,img[0])
            save_name="./圖片/page_{}_{}.png".format(page.number,i)
            pix.writePNG(save_name)
            image=pixmap2array(pix)
            i+=1

ananlysis_PDF(file)