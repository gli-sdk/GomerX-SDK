# -*- encoding = utf-8 -*-
import qrcode
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import tkinter as tk
import os
from PIL import Image, ImageTk
import cv2 as cv
import numpy as np


def inspection():
    string = entry_txt.get()
    img = qrcode.make(string)

    filename = filedialog.asksaveasfilename(
        defaultextension='.png')
    img.save(filename)
    messagebox.showinfo('提示', '%s保存成功' % filename)


def attention():
    messagebox.showinfo(
        '使用说明', '输入文本内容转换为二维码\n按下保存图片保存二维码\n')


def refreshText():
    # 生成二维码
    string = entry_txt.get()

    if string != '':
        global img_png

        save_img = qrcode.make(string)
        img_png = ImageTk.PhotoImage(save_img, size=(30, 30))
        label_image = Label(root, image=img_png)
        label_image.grid(row=2, column=0, padx=10, pady=10)

    root.after(500, refreshText)


if __name__ == "__main__":
    root = Tk()
    e = StringVar()
    root.title('二维码生成器')
    root.geometry('360x470')
    img_png = None
    entry_txt = Entry(root, font=('微软雅黑', 20))
    entry_txt.grid(row=0, column=0, padx=20, pady=30)

    Label_image = Label(root)
    Label_image.grid(row=2, column=0, padx=20, pady=150)

    save_button = Button(root, text='保存图片',
                         font=('微软雅黑', 15),
                         fg='red',
                         command=inspection)
    save_button.grid(row=4, sticky=SE)

    use_guide_button = Button(root,
                              text='使用说明',
                              font=('微软雅黑', 15),
                              command=attention)
    use_guide_button.grid(row=4, sticky=SW)

    root.after(500, refreshText)
    root.mainloop()
