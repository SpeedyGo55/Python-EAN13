from io import BytesIO
import win32clipboard
import PIL.Image
import os
import sys
from tkinter import *
from tkinter import filedialog
import matplotlib.pyplot as plt
import numpy as np

global setFigure
# noinspection PyRedeclaration
setFigure = False
global label

root = Tk()
root.title("EAN-13 Generator")
root.iconbitmap("icon.ico")

selected = BooleanVar()
info = Label(root, text="Input 12 Digits:")
info.pack()

entry = Entry(root)
entry.pack()

decimal = "0"
leftOdd = [
    np.array([0, 0, 0, 1, 1, 0, 1]),  # 0
    np.array([0, 0, 1, 1, 0, 0, 1]),  # 1
    np.array([0, 0, 1, 0, 0, 1, 1]),  # 2
    np.array([0, 1, 1, 1, 1, 0, 1]),  # 3
    np.array([0, 1, 0, 0, 0, 1, 1]),  # 4
    np.array([0, 1, 1, 0, 0, 0, 1]),  # 5
    np.array([0, 1, 0, 1, 1, 1, 1]),  # 6
    np.array([0, 1, 1, 1, 0, 1, 1]),  # 7
    np.array([0, 1, 1, 0, 1, 1, 1]),  # 8
    np.array([0, 0, 0, 1, 0, 1, 1])  # 9
]
leftEven = [
    np.array([0, 1, 0, 0, 1, 1, 1]),  # 0
    np.array([0, 1, 1, 0, 0, 1, 1]),  # 1
    np.array([0, 0, 1, 1, 0, 1, 1]),  # 2
    np.array([0, 1, 0, 0, 0, 0, 1]),  # 3
    np.array([0, 0, 1, 1, 1, 0, 1]),  # 4
    np.array([0, 1, 1, 1, 0, 0, 1]),  # 5
    np.array([0, 0, 0, 0, 1, 0, 1]),  # 6
    np.array([0, 0, 1, 0, 0, 0, 1]),  # 7
    np.array([0, 0, 0, 1, 0, 0, 1]),  # 8
    np.array([0, 0, 1, 0, 1, 1, 1])  # 9
]
rightEven = [
    np.array([1, 1, 1, 0, 0, 1, 0]),  # 0
    np.array([1, 1, 0, 0, 1, 1, 0]),  # 1
    np.array([1, 1, 0, 1, 1, 0, 0]),  # 2
    np.array([1, 0, 0, 0, 0, 1, 0]),  # 3
    np.array([1, 0, 1, 1, 1, 0, 0]),  # 4
    np.array([1, 0, 0, 1, 1, 1, 0]),  # 5
    np.array([1, 0, 1, 0, 0, 0, 0]),  # 6
    np.array([1, 0, 0, 0, 1, 0, 0]),  # 7
    np.array([1, 0, 0, 1, 0, 0, 0]),  # 8
    np.array([1, 1, 1, 0, 1, 0, 0])  # 9
]
firstNumber = [
    np.array([0, 0, 0, 0, 0, 0]),  # 0
    np.array([0, 0, 1, 0, 1, 1]),  # 1
    np.array([0, 0, 1, 1, 0, 1]),  # 2
    np.array([0, 0, 1, 1, 1, 0]),  # 3
    np.array([0, 1, 0, 0, 1, 1]),  # 4
    np.array([0, 1, 1, 0, 0, 1]),  # 5
    np.array([0, 1, 1, 1, 0, 0]),  # 6
    np.array([0, 1, 0, 1, 0, 1]),  # 7
    np.array([0, 1, 0, 1, 1, 0]),  # 8
    np.array([0, 1, 1, 0, 1, 0])  # 9
]


def generate_checknumber(number):
    checknumber = 0
    if len(number) != 12:
        print("WRONG")
        return "length"
    for i in range(0, 12):
        if i % 2 == 0 or i == 0:
            checknumber += int(number[i])
        else:
            checknumber += int(number[i]) * 3
    print(checknumber)
    checknumber = 10 - (checknumber % 10)

    if checknumber == 10:
        checknumber = 0
    print(checknumber)
    print(number + str(checknumber))
    return number + str(checknumber)


def check_ean13(number):
    checknumber = 0
    information = number[:12]

    if len(information) != 12:
        print("WRONG LENGTH")
        return None
    for i in range(0, 12):
        if i % 2 == 0 or i == 0:
            checknumber += int(number[i])
        else:
            checknumber += int(number[i]) * 3
    print(checknumber)
    checknumber = 10 - (checknumber % 10)
    print(checknumber)
    if checknumber != int(number[12]):
        print("WRONG CHECKNUMBER")
        return None
    else:
        return number


def make_ean13(number):
    global setFigure
    global label
    first_digit = number[:1]
    number = number[1:]
    left = number[:6]
    right = number[6:]
    code = np.array([0, 0, 0, 0, 0, 1, 0, 1])
    for i in range(6):
        if firstNumber[int(first_digit)][i] == 0:
            code = np.concatenate((code, leftOdd[(int(left[i]))]))
        else:
            code = np.concatenate((code, leftEven[(int(left[i]))]))
    code = np.concatenate((code, np.array([0, 1, 0, 1, 0])))
    for i in range(6):
        code = np.concatenate((code, rightEven[(int(right[i]))]))
    code = np.concatenate((code, np.array([1, 0, 1, 0, 0, 0, 0, 0])))
    pixel_per_bar = 5
    dpi = 100

    fig = plt.figure(figsize=(len(code) * pixel_per_bar / dpi, 2), dpi=dpi)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()
    ax.imshow(code.reshape(1, -1), cmap='binary', aspect='auto',
              interpolation='nearest')
    plt.savefig("Figure_1.png")
    img = PhotoImage(file="Figure_1.png")
    setFigure = True
    label = Label(root, image=img)
    label.image = img
    label.pack()


def run(event=0):
    try:
        label.destroy()
    except NameError:
        pass
    print(event)
    if selected.get():
        num = generate_checknumber(entry.get())
        if num == "length":
            entry.delete(0, END)
            return
        make_ean13(num)
    else:
        num = check_ean13(entry.get())
        if num is not None:
            make_ean13(num)
        else:
            entry.delete(0, END)
            return


def copy():
    try:
        filepath = "Figure_1.png"
        image = PIL.Image.open(filepath)
        output = BytesIO()
        image.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()
    except Exception as e:
        print(e)
        pass


def change_info():
    info.config(text="")
    global selected
    if selected.get():
        info.config(text="Input 12 Digits:")
    else:
        info.config(text="Input 13 Digits:")


def save():
    if not setFigure:
        return
    else:
        path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=(("PNG", "*.png"),
                                                                                ("JPEG", "*.jpg"),
                                                                                ("All Files", "*.*")))
        try:
            plt.savefig(path)
        except Exception as e:
            print(e)
            pass


def on_closing():
    root.destroy()
    try:
        os.remove("Figure_1.png")
    except FileNotFoundError:
        pass
    root.quit()
    sys.exit(0)


# noinspection PyTypeChecker
root.bind("<Return>", run)

R1 = Radiobutton(root, text="Generate Checknumber automagically",
                 variable=selected, value=True, command=change_info)

R2 = Radiobutton(root, text="Input Checknumber along encoded Numbers",
                 variable=selected, value=False, command=change_info)

submit = Button(root, text="Submit", command=run)
save = Button(root, text="Save", command=save)
copy = Button(root, text="Copy to Clipboard", command=copy)
R1.pack()
R2.pack()
submit.pack()
save.pack()
copy.pack()
selected.set(True)

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
