from tkinter import Tk, ttk, PhotoImage
from PIL import ImageTk, Image
from vcells import VCells

vcells = VCells("image.png", 10, 300)

scale = 2
size = [x * scale for x in vcells.image.size]
launched = False

root = Tk()

img = ImageTk.PhotoImage(vcells.image.image.resize(size))
label = ttk.Label(root, image=img)
label.grid()


def handle_step(ev):
    vcells.step()
    img2 = ImageTk.PhotoImage(vcells.image.image.resize(size))
    label.configure(image=img2)
    label.image = img2


def upd(ev):
    print("po")
    while vcells.step() != 0:
        img2 = ImageTk.PhotoImage(vcells.image.image.resize(size))
        label.configure(image=img2)
        label.image = img2
        root.after_idle(lambda: upd(ev))
        yield


def handle_run(ev):
    upd()


btnframe = ttk.Frame(root)
btn1 = ttk.Button(btnframe, text='step')
btn2 = ttk.Button(btnframe, text='all')
btn1.bind('<1>', handle_step)
btn2.bind('<1>', upd)

btnframe.grid()
btn1.grid()
btn2.grid()

root.mainloop()
