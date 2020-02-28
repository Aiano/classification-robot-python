from classificationFunc import *
from control import *
import tkinter

if __name__ == '__main__':
    window = tkinter.Tk()
    window.title("Classification Robot")
    window.geometry("500x300")

    la = tkinter.Label(window, text="Please choose mode:")
    la.pack()

    bu1 = tkinter.Button(window, text="classification", command=classification)
    bu1.pack()

    bu2 = tkinter.Button(window, text="control", command=control)
    bu2.pack()

    tkinter.mainloop()
