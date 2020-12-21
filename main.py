from tkinter import *

launcher = Tk()
launcher.title("Perfect Launcher")
launcher.geometry("800x500")
launcher.configure(background="#008")

txt1 = Label(launcher, text = "Perfect Launcher", background = "#00f", foreground="#fff")
txt1.place(x = 10, y = 10, width = 100, height = 20)



launcher.mainloop()