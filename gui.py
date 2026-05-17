import tkinter as tk
from tkinter import ttk
from search import search
from theme import *
from state import state

def launch_app():
    root = tk.Tk()

    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both")

    tab1 = ttk.Frame(notebook)
    tab2 = ttk.Frame(notebook)

    notebook.add(tab1, text="Search")
    notebook.add(tab2, text="Results")

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

    def show_results():
        columns = ('#', 'Mission', 'Year', 'Author', 'Exptimes', 'Target Name', 'Distance Arcsec')
        tree = ttk.Treeview(tab1, columns=columns, show='headings')

        for col in columns:
            tree.heading(col, text=col)
        
        for i, val in enumerate(state["search_results"].table):

            tree.insert('', tk.END, values=(i + 1, val["mission"], val["year"], val["author"], val["exptime"], val["target_name"], val["distance"]))

        tree.place(relx=0.5, rely=0.75, anchor=tk.CENTER)



    def run_search():
        results = search('Kepler-90', radius=None, exptime=None, cadence=None, mission=('Kepler', 'K2', 'TESS'),
            author=None, quarter=None, month=None, campaign=None,
            sector=None, limit=None)
        
        state["search_results"] = results

        #Show the results
        show_results()

    #SEARCH BUTTON
    search_btn = tk.Button(tab1,
                    text="Search",
                    width=25,
                    bg=MAIN2,
                    fg=TEXT1,
                    command=run_search)
    search_btn.place(relx=0.475, rely=0.45, anchor=tk.CENTER)


    root.mainloop()