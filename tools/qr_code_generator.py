# -*- encoding = utf-8 -*-
import qrcode
from tkinter import *
from tkinter import messagebox
import tkinter as tk
import os
from PIL import Image, ImageTk


def made(string, filename):
    if not os.path.exists('images'):
        os.mkdir('images')
    os.chdir('images')
    img = qrcode.make(string)
    img.save(filename)
    messagebox.showinfo('提示', '%s保存成功' % filename)
    os.chdir('..')


def inspection():
    string = entry.get()
    file = entry2.get()
    list = file.strip().split('.')
    try:
        if string.strip() != '' and (list[1] == 'jpg' or list[1] == 'png'):
            made(string, file)
        else:
            messagebox.showerror('错误', '输入错误')
    except IndexError:
        messagebox.showerror('错误', '请输入正确的文件名')


def attention():
    messagebox.showinfo(
        '使用说明', '输入二维码内容\n保存的文件名(要加后缀,例如 test.jpg)\n按下生成即可\n')


def refreshText():
    # 生成二维码
    string = entry_txt.get()

    if string != '':
        global img_png
        img = qrcode.make(string)
        img.save('tmp_img.png')
        img_open = Image.open('tmp_img.png')
        img_png = ImageTk.PhotoImage(img_open)
        label_image = Label(root, image=img_png)
        label_image.grid(row=2, column=0, padx=10, pady=100)

    root.after(500, refreshText)


if __name__ == "__main__":
    root = Tk()
    e = StringVar()
    root.title('二维码生成器')
    root.geometry('800x600')
    root.resizable(False, False)  # 规定窗口不可缩放
    img_png = None
    entry_txt = Entry(root, font=('微软雅黑', 20))
    entry_txt.grid(row=0, column=0, padx=50, pady=10)

    entry_image = Entry(root, font=('微软雅黑', 20)).grid(
        row=1, column=0, padx=10, pady=10)

    Label_image = Label(root).grid(row=2, column=0, padx=10, pady=100)

    save_button = Button(root, text='保存图片', font=('微软雅黑', 20),
                         fg='red', command=inspection)
    save_button.grid(row=4, sticky=SE)

    use_guide_button = Button(
        root, text='使用说明', font=('微软雅黑', 20), command=attention)
    use_guide_button.grid(row=4, sticky=SW)

    root.after(500, refreshText)
    root.mainloop()
