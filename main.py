from tkinter import *
import tkinter as tk

root = Tk()

root.state('zoomed') #Linux may need root.attributes('-zoomed', True)
bg_image = tk.PhotoImage(file="assets/horsehead.png")

#Set background image
bg_label = tk.Label(root, image=bg_image)
bg_label.place(relwidth=1, relheight=1)

title = Label(root, text="Planet Detector", bg="red", fg="darkblue", font=("Courier New", 25, "bold"))
title.pack()
paragraph = Label(root, text="FDSFDS")
paragraph.pack()

root.mainloop()