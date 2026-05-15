import tkinter as tk
from tkinter import ttk

root = tk.Tk()

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)

notebook.add(tab1, text="Search")
notebook.add(tab2, text="Results")

#COLORS
MAIN1 = "#465C88"
MAIN2 = "#0A1D51"
MAIN3 = "#080616"
ACCENT1 = "#3A9AFF"
ACCENT2 = "#FF52A0"
ACCENT3 = "#FFDE42"
TEXT1 = "#F6F6F6"
TEXT2 = "#A2D5C6"

#HOVER COLORS -- NOT WORKING
def on_enter(e):
    e.widget.config(background=ACCENT1, foreground='white')

def on_leave(e):
    e.widget.config(background='SystemButtonFace')

root.state('zoomed') #Linux may need root.attributes('-zoomed', True)

#BACKGROUND
style = ttk.Style()
style.theme_use('clam')

style.configure('TFrame', background=MAIN3)

style.configure('TNotebook.Tab', background=MAIN3, foreground='white')
style.map('TNotebook.Tab', background=[('selected', '#1A252F')])

#TITLE AND PARAGRAPH
title = tk.Label(tab1,
              text="Planet Detector",
              bg=MAIN3, fg=TEXT1,
              font=("Courier New", 30, "bold"))
title.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
paragraph = tk.Label(tab1,
                  text="Search for data",
                  fg=TEXT2,
                  bg=MAIN3,
                  font=("Courier New", 15))
paragraph.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

#ENTER SEARCH DATA -- COL 1
tk.Label(tab1, text="Target", bg=MAIN2, fg=TEXT1, font=("Courier New", 10)).place(relx=0.18, rely=0.25, anchor=tk.CENTER)
tk.Label(tab1, text="Radius", bg=MAIN2, fg=TEXT1, font=("Courier New", 10)).place(relx=0.18, rely=0.3, anchor=tk.CENTER)
tk.Label(tab1, text="Exptime", bg=MAIN2, fg=TEXT1, font=("Courier New", 10)).place(relx=0.18, rely=0.35, anchor=tk.CENTER)
tk.Label(tab1, text="Cadence", bg=MAIN2, fg=TEXT1, font=("Courier New", 10)).place(relx=0.18, rely=0.4, anchor=tk.CENTER)

entry1 = tk.Entry(tab1, bg=MAIN1, fg=TEXT1).place(relx=0.25, rely=0.25, anchor=tk.CENTER)
entry2 = tk.Entry(tab1, bg=MAIN1, fg=TEXT1).place(relx=0.25, rely=0.3, anchor=tk.CENTER)
entry3 = tk.Entry(tab1, bg=MAIN1, fg=TEXT1).place(relx=0.25, rely=0.35, anchor=tk.CENTER)
entry4 = tk.Entry(tab1, bg=MAIN1, fg=TEXT1).place(relx=0.25, rely=0.4, anchor=tk.CENTER)

#ENTER SEARCH DATA -- COL 2
tk.Label(tab1, text="Mission", bg=MAIN2, fg=TEXT1, font=("Courier New", 10)).place(relx=0.43, rely=0.25, anchor=tk.CENTER)
tk.Label(tab1, text="Author", bg=MAIN2, fg=TEXT1, font=("Courier New", 10)).place(relx=0.43, rely=0.3, anchor=tk.CENTER)
tk.Label(tab1, text="Quarter", bg=MAIN2, fg=TEXT1, font=("Courier New", 10)).place(relx=0.43, rely=0.35, anchor=tk.CENTER)

entry1 = tk.Entry(tab1, bg=MAIN1, fg=TEXT1).place(relx=0.5, rely=0.25, anchor=tk.CENTER)
entry2 = tk.Entry(tab1, bg=MAIN1, fg=TEXT1).place(relx=0.5, rely=0.3, anchor=tk.CENTER)
entry3 = tk.Entry(tab1, bg=MAIN1, fg=TEXT1).place(relx=0.5, rely=0.35, anchor=tk.CENTER)

#ENTER SEARCH DATA -- COL 3
tk.Label(tab1, text="Month", bg=MAIN2, fg=TEXT1, font=("Courier New", 10)).place(relx=0.68, rely=0.25, anchor=tk.CENTER)
tk.Label(tab1, text="Campagin", bg=MAIN2, fg=TEXT1, font=("Courier New", 10)).place(relx=0.68, rely=0.3, anchor=tk.CENTER)
tk.Label(tab1, text="Sector", bg=MAIN2, fg=TEXT1, font=("Courier New", 10)).place(relx=0.68, rely=0.35, anchor=tk.CENTER)
tk.Label(tab1, text="Limit", bg=MAIN2, fg=TEXT1, font=("Courier New", 10)).place(relx=0.68, rely=0.4, anchor=tk.CENTER)

entry1 = tk.Entry(tab1, bg=MAIN1, fg=TEXT1).place(relx=0.75, rely=0.25, anchor=tk.CENTER)
entry2 = tk.Entry(tab1, bg=MAIN1, fg=TEXT1).place(relx=0.75, rely=0.3, anchor=tk.CENTER)
entry3 = tk.Entry(tab1, bg=MAIN1, fg=TEXT1).place(relx=0.75, rely=0.35, anchor=tk.CENTER)
entry4 = tk.Entry(tab1, bg=MAIN1, fg=TEXT1).place(relx=0.75, rely=0.4, anchor=tk.CENTER)

#SEARCH BUTTON
search = tk.Button(tab1,
                text="Search",
                width=25,
                bg=MAIN2,
                fg=TEXT1,
                command=root.destroy)
search.place(relx=0.475, rely=0.45, anchor=tk.CENTER)

#BINDING FOR HOVER
# entry1.bind("<Enter>", on_enter) #It doesn't work right
# entry2.bind("<Leave>", on_leave) #It doesn't work right


root.mainloop()