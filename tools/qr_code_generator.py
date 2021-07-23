# -*- encoding = utf-8 -*-
import qrcode
from tkinter import Tk, Entry, Label, Button, SE, SW
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
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
        num_img = 255 * np.array(save_img).astype('uint8')
        img = cv2.cvtColor(np.asarray(num_img), cv2.COLOR_RGB2BGR)
        resize_img = cv2.resize(img, (300, 300))
        img = Image.fromarray(cv2.cvtColor(resize_img, cv2.COLOR_BGR2RGB))

        img_png = ImageTk.PhotoImage(img)
        label_image = Label(root, image=img_png)
        label_image.grid(row=2, column=0, padx=10, pady=10)

    root.after(500, refreshText)


if __name__ == "__main__":
    root = Tk()
    root.title('二维码生成器')
    root.geometry('360x470')
    root.resizable(0, 0)
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
