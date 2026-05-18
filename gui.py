import tkinter as tk
from tkinter import ttk
from search import search
from theme import *
from state import state

def launch_app():

    root = tk.Tk()

    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both")

    search_tab = ttk.Frame(notebook)
    about_tab = ttk.Frame(notebook)

    notebook.add(search_tab, text="Search")
    notebook.add(about_tab, text="About")

    root.state('zoomed')

    #BACKGROUND
    style = ttk.Style()
    style.theme_use('clam')

    style.configure('TFrame', background=MAIN3)

    style.configure('TNotebook.Tab', background=MAIN3, foreground='white')
    style.map('TNotebook.Tab', background=[('selected', '#1A252F')])

    #TITLE
    title = tk.Label(
        search_tab,
        text="Planet Detector",
        bg=MAIN3,
        fg=TEXT1,
        font=("Courier New", 30, "bold")
    )
    title.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

    paragraph = tk.Label(
        search_tab,
        text="Search for data",
        fg=TEXT2,
        bg=MAIN3,
        font=("Courier New", 15)
    )
    paragraph.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

    #ENTRIES
    tk.Label(search_tab, text="Target", bg=MAIN2, fg=TEXT1,
            font=("Courier New", 10)).place(relx=0.12, rely=0.24, anchor="w")

    target_entry = tk.Entry(search_tab, bg=MAIN1, fg=TEXT1, width=20)
    target_entry.place(relx=0.20, rely=0.24, anchor="w")

    tk.Label(search_tab, text="Radius", bg=MAIN2, fg=TEXT1,
            font=("Courier New", 10)).place(relx=0.12, rely=0.31, anchor="w")

    radius_entry = tk.Entry(search_tab, bg=MAIN1, fg=TEXT1, width=20)
    radius_entry.place(relx=0.20, rely=0.31, anchor="w")

    tk.Label(search_tab, text="Exptime", bg=MAIN2, fg=TEXT1,
            font=("Courier New", 10)).place(relx=0.12, rely=0.38, anchor="w")

    exptime_entry = tk.Entry(search_tab, bg=MAIN1, fg=TEXT1, width=20)
    exptime_entry.place(relx=0.20, rely=0.38, anchor="w")

    tk.Label(search_tab, text="Cadence", bg=MAIN2, fg=TEXT1,
            font=("Courier New", 10)).place(relx=0.12, rely=0.45, anchor="w")

    cadence_entry = tk.Entry(search_tab, bg=MAIN1, fg=TEXT1, width=20)
    cadence_entry.place(relx=0.20, rely=0.45, anchor="w")

    tk.Label(search_tab, text="Mission", bg=MAIN2, fg=TEXT1,
            font=("Courier New", 10)).place(relx=0.42, rely=0.24, anchor="w")

    mission_entry = tk.Entry(search_tab, bg=MAIN1, fg=TEXT1, width=20)
    mission_entry.place(relx=0.51, rely=0.24, anchor="w")

    tk.Label(search_tab, text="Author", bg=MAIN2, fg=TEXT1,
            font=("Courier New", 10)).place(relx=0.42, rely=0.31, anchor="w")

    author_entry = tk.Entry(search_tab, bg=MAIN1, fg=TEXT1, width=20)
    author_entry.place(relx=0.51, rely=0.31, anchor="w")

    tk.Label(search_tab, text="Quarter", bg=MAIN2, fg=TEXT1,
            font=("Courier New", 10)).place(relx=0.42, rely=0.38, anchor="w")

    quarter_entry = tk.Entry(search_tab, bg=MAIN1, fg=TEXT1, width=20)
    quarter_entry.place(relx=0.51, rely=0.38, anchor="w")

    tk.Label(search_tab, text="Month", bg=MAIN2, fg=TEXT1,
            font=("Courier New", 10)).place(relx=0.72, rely=0.24, anchor="w")

    month_entry = tk.Entry(search_tab, bg=MAIN1, fg=TEXT1, width=20)
    month_entry.place(relx=0.80, rely=0.24, anchor="w")

    tk.Label(search_tab, text="Campaign", bg=MAIN2, fg=TEXT1,
            font=("Courier New", 10)).place(relx=0.72, rely=0.31, anchor="w")

    campaign_entry = tk.Entry(search_tab, bg=MAIN1, fg=TEXT1, width=20)
    campaign_entry.place(relx=0.80, rely=0.31, anchor="w")

    tk.Label(search_tab, text="Sector", bg=MAIN2, fg=TEXT1,
            font=("Courier New", 10)).place(relx=0.72, rely=0.38, anchor="w")

    sector_entry = tk.Entry(search_tab, bg=MAIN1, fg=TEXT1, width=20)
    sector_entry.place(relx=0.80, rely=0.38, anchor="w")

    tk.Label(search_tab, text="Limit", bg=MAIN2, fg=TEXT1,
            font=("Courier New", 10)).place(relx=0.72, rely=0.45, anchor="w")

    limit_entry = tk.Entry(search_tab, bg=MAIN1, fg=TEXT1, width=20)
    limit_entry.place(relx=0.80, rely=0.45, anchor="w")
    #TREEVIEW

    columns = ('#', 'Mission', 'Year', 'Author',
               'Exptime', 'Target Name', 'Distance')

    tree = ttk.Treeview(search_tab, columns=columns, show='headings', height=12)

    col_widths = [40, 100, 60, 100, 90, 160, 120]

    for i, col in enumerate(columns):
        tree.heading(col, text=col)
        tree.column(col, width=col_widths[i], stretch=False)

    tree.place(relx=0.5, rely=0.75, anchor=tk.CENTER)

    #SHOW RESULTS

    def show_results():

        # clear old rows
        for row in tree.get_children():
            tree.delete(row)

        # insert new rows
        for i, val in enumerate(state["search_results"].table):

            tree.insert(
                '',
                tk.END,
                values=(
                    i + 1,
                    val["mission"],
                    val["year"],
                    val["author"],
                    val["exptime"],
                    val["target_name"],
                    val["distance"]
                )
            )

    #SEARCH

    def run_search():

        query = {
            "target": target_entry.get() or "Kepler-90",
            "radius": radius_entry.get() or None,
            "exptime": exptime_entry.get() or None,
            "cadence": cadence_entry.get() or None,
            "mission": mission_entry.get() or ('Kepler', 'K2', 'TESS'),
            "author": author_entry.get() or None,
            "quarter": quarter_entry.get() or None,
            "month": month_entry.get() or None,
            "campaign": campaign_entry.get() or None,
            "sector": sector_entry.get() or None,
            "limit": int(limit_entry.get()) if limit_entry.get() else None
        }

        results = search(
            target=query["target"],
            radius=query["radius"],
            exptime=query["exptime"],
            cadence=query["cadence"],
            mission=query["mission"],
            author=query["author"],
            quarter=query["quarter"],
            month=query["month"],
            campaign=query["campaign"],
            sector=query["sector"],
            limit=query["limit"]
        )

        state["search_results"] = results

        show_results()

    #SEARCH BUTTON
    search_btn = tk.Button(
        search_tab,
        text="Search",
        width=25,
        bg=MAIN2,
        fg=TEXT1,
        command=run_search
    )

    search_btn.place(relx=0.475, rely=0.45, anchor=tk.CENTER)

    root.mainloop()