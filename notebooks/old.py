import numpy as np
import matplotlib
matplotlib.use("TkAgg") #separate window
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, messagebox
import lightkurve as lk

state = {
    "file": None,
    "lc": None,
    "bls_short": None,
    "bls_long": None,
    "planet_b": {},
    "planet_c": {},
    "masked_lc": None,
}

#whoa cool colors
BG       = "#0b0f1a"
PANEL    = "#111827"
ACCENT   = "#38bdf8"
ACCENT2  = "#f472b6"
TEXT     = "#e2e8f0"
SUBTEXT  = "#94a3b8"
BORDER   = "#1e293b"
SUCCESS  = "#4ade80"
WARNING  = "#facc15"

def embed_figure(fig, parent): #put the graph into the tkinter thingy
    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()

    widget = canvas.get_tk_widget()
    widget.pack(fill="both", expand=True)

    #attach matplotlib canvas cleanup
    canvas._tkcanvas = widget

    return canvas

#matplotlib making it pretty
def apply_plot_style(ax, title="", xlabel="", ylabel=""):
    ax.set_facecolor("#0d1117")
    ax.figure.patch.set_facecolor("#0d1117")
    ax.tick_params(colors=SUBTEXT, labelsize=8)
    ax.spines[:].set_color(BORDER)
    ax.title.set_color(TEXT)
    ax.xaxis.label.set_color(SUBTEXT)
    ax.yaxis.label.set_color(SUBTEXT)
    if title:   ax.set_title(title, fontsize=10, color=TEXT, pad=8)
    if xlabel:  ax.set_xlabel(xlabel, fontsize=8)
    if ylabel:  ax.set_ylabel(ylabel, fontsize=8)

#load the file you are analyzing
def load_file():
    path = "./mastDownload/Kepler/kplr011446443_sc_Q113313330333033302/kplr011446443-2009131110544_slc.fits"
    
    state["file"] = path
    status_var.set("File loaded. Running analysis…")
    root.update()
    
    run_analysis()

#analysis of the data
def run_analysis():
    try:
        #load the data with lightkurve
        lc_file = lk.read(state["file"])
        lc = lc_file.normalize().remove_nans().remove_outliers()
        lc = lc.flatten(window_length=901)
        state["lc"] = lc

        #bls short period search
        period_short = np.linspace(1, 20, 10000)
        bls_s = lc.to_periodogram(method='bls', period=period_short, frequency_factor=500)
        state["bls_short"] = bls_s

        pb_period = bls_s.period_at_max_power
        pb_t0     = bls_s.transit_time_at_max_power
        pb_dur    = bls_s.duration_at_max_power

        #cadence mask for planet b
        mask = bls_s.get_transit_mask(period=pb_period, transit_time=pb_t0, duration=pb_dur)
        masked_lc = lc[~mask]
        state["masked_lc"] = masked_lc

        #depth estimates
        stats_b = bls_s.compute_stats(pb_period, pb_dur, pb_t0)
        depth_raw = stats_b["depth"]

        if isinstance(depth_raw, tuple) or isinstance(depth_raw, list):
            depth_b = float(depth_raw[0].value if hasattr(depth_raw[0], "value") else depth_raw[0])
        else:
            depth_b = float(depth_raw.value if hasattr(depth_raw, "value") else depth_raw)

        state["planet_b"] = {
            "period":   pb_period,
            "t0":       pb_t0,
            "duration": pb_dur,
            "depth":    depth_b,
            "model":    bls_s.get_transit_model(period=pb_period, transit_time=pb_t0, duration=pb_dur),
            "mask":     mask,
            "snr":      float(bls_s.max_power),
        }

        #long period search
        period_long = np.linspace(1, 300, 10000)
        bls_l = masked_lc.to_periodogram('bls', period=period_long, frequency_factor=500)
        state["bls_long"] = bls_l

        pc_period = bls_l.period_at_max_power
        pc_t0     = bls_l.transit_time_at_max_power
        pc_dur    = bls_l.duration_at_max_power

        stats_c = bls_l.compute_stats(pc_period, pc_dur, pc_t0)
        depth_raw = stats_b["depth"]

        if isinstance(depth_raw, tuple) or isinstance(depth_raw, list):
            depth_c = float(depth_raw[0].value if hasattr(depth_raw[0], "value") else depth_raw[0])
        else:
            depth_c = float(depth_raw.value if hasattr(depth_raw, "value") else depth_raw)

        state["planet_c"] = {
            "period":   pc_period,
            "t0":       pc_t0,
            "duration": pc_dur,
            "depth":    depth_c,
            "model":    bls_l.get_transit_model(period=pc_period, transit_time=pc_t0, duration=pc_dur),
            "snr":      float(bls_l.max_power),
        }

        #detection threshhold
        THRESHOLD = 15.0  # BLS power threshold for a credible detection

        has_b = state["planet_b"]["snr"] > THRESHOLD
        has_c = state["planet_c"]["snr"] > THRESHOLD

        update_results_panel(has_b, has_c)
        enable_buttons()
        status_var.set("Analysis complete!")

    except Exception as e:
        messagebox.showerror("Analysis Error", str(e))
        status_var.set("Analysis failed.")

#design stuff
#results panel
def update_results_panel(has_b, has_c):
    for w in results_frame.winfo_children():
        w.destroy()

    def row(label, value, color=TEXT):
        f = tk.Frame(results_frame, bg=PANEL)
        f.pack(fill="x", pady=1)
        tk.Label(f, text=label, bg=PANEL, fg=SUBTEXT,
                 font=("Courier New", 9), width=26, anchor="w").pack(side="left")
        tk.Label(f, text=value, bg=PANEL, fg=color,
                 font=("Courier New", 9, "bold"), anchor="w").pack(side="left")

    def section(title, color=ACCENT):
        tk.Label(results_frame, text=title, bg=PANEL, fg=color,
                 font=("Courier New", 10, "bold")).pack(anchor="w", pady=(10, 2))
        ttk.Separator(results_frame, orient="horizontal").pack(fill="x", pady=2)

    #star header
    fname = state["file"].split("/")[-1] if state["file"] else "Unknown"
    section("STAR", ACCENT)
    row("File", fname)

    lc = state["lc"]
    if lc is not None:
        total_days = float(lc.time.max().value - lc.time.min().value)
        row("Observation span", f"{total_days:.1f} days")
        row("Data points", f"{len(lc.time):,}")

    #planet b
    section("CANDIDATE PLANET b", SUCCESS if has_b else WARNING)
    if has_b:
        pb = state["planet_b"]
        row("Detection",      "Likely detected",  SUCCESS)
        row("Orbital period", f"{pb['period'].value:.4f} days")
        row("Transit epoch",  f"{pb['t0'].value:.4f} BKJD")
        row("Transit dur.",   f"{pb['duration'].value * 24:.2f} hours")
        if pb["depth"] is not None:
            rp_rs = np.sqrt(abs(pb["depth"]))
            row("Transit depth",  f"{abs(pb['depth']):.5f} (rel. flux)")
            row("Rp/Rs estimate", f"≈ {rp_rs:.4f}")
        row("BLS power (SNR)", f"{pb['snr']:.2f}")
    else:
        row("Detection", "Weak / not detected", WARNING)
        row("BLS power", f"{state['planet_b']['snr']:.2f}")

    #planet c
    section("CANDIDATE PLANET c", SUCCESS if has_c else WARNING)
    if has_c:
        pc = state["planet_c"]
        row("Detection",      "Likely detected",  SUCCESS)
        row("Orbital period", f"{pc['period'].value:.4f} days")
        row("Transit epoch",  f"{pc['t0'].value:.4f} BKJD")
        row("Transit dur.",   f"{pc['duration'].value * 24:.2f} hours")
        if pc["depth"] is not None:
            rp_rs = np.sqrt(abs(pc["depth"]))
            row("Transit depth",  f"{abs(pc['depth']):.5f} (rel. flux)")
            row("Rp/Rs estimate", f"≈ {rp_rs:.4f}")
        row("BLS power (SNR)", f"{pc['snr']:.2f}")
    else:
        row("Detection", "Weak / not detected", WARNING)
        row("BLS power", f"{state['planet_c']['snr']:.2f}")

    #are there planets
    section("VERDICT", ACCENT2)
    if has_b and has_c:
        verdict = "Multi-planet system detected"
        vc = SUCCESS
    elif has_b or has_c:
        verdict = "Single planet candidate detected"
        vc = SUCCESS
    else:
        verdict = "No strong planet signal found."
        vc = WARNING
    tk.Label(results_frame, text=verdict, bg=PANEL, fg=vc,
             font=("Courier New", 10, "bold"), wraplength=300, justify="left").pack(anchor="w", pady=4)

    tk.Label(results_frame,
             text="Note: BLS power > 15 is used as the detection threshold.\n"
                  "Rp/Rs is the planet-to-star radius ratio. Values ~0.01–0.15\n"
                  "are typical for Kepler planets.",
             bg=PANEL, fg=SUBTEXT, font=("Courier New", 8),
             justify="left", wraplength=300).pack(anchor="w", pady=(6, 0))

#plot functions
def open_plot_window(title, info_text, plot_fn):
    win = tk.Toplevel(root)
    win.title(title)
    win.configure(bg=BG)
    win.geometry("1400x1000")

    fig_container = {"fig": None, "canvas": None}

    def on_close():
        try:
            if fig_container["canvas"]:
                fig_container["canvas"].get_tk_widget().destroy()
            if fig_container["fig"]:
                plt.close(fig_container["fig"])
        except:
            pass
        win.destroy()

    win.protocol("WM_DELETE_WINDOW", on_close)

    info = tk.Label(
        win,
        text=info_text,
        bg=PANEL,
        fg=SUBTEXT,
        font=("Courier New", 9),
        justify="left",
        wraplength=1200,
        padx=12,
        pady=8
    )
    info.pack(fill="x")

    frame = tk.Frame(win, bg=BG)
    frame.pack(fill="both", expand=True)

    fig, axes = plot_fn()

    fig_container["fig"] = fig
    fig_container["canvas"] = embed_figure(fig, frame)


#plot 1, light curve (flattened)
def show_light_curve():
    info = ("FLATTENED LIGHT CURVE\n"
            "This plot shows the brightness of the star over time after removing slow "
            "instrumental trends (flattening). Each dip in the flux may indicate a planet "
            "passing in front of the star (a 'transit'). The x-axis is time in days "
            "(Barycentric Kepler Julian Date), and the y-axis is relative flux (normalized).")
    def plot_fn():
        fig, ax = plt.subplots(figsize=(16, 7))
        state["lc"].scatter(ax=ax, s=1, color=ACCENT, alpha=0.6, label="Flux")
        apply_plot_style(ax, "Flattened Light Curve", "Time (BKJD)", "Normalized Flux")
        fig.tight_layout()
        return fig, [ax]
    open_plot_window("Light Curve", info, plot_fn)


#plot 2, bls periodogram
def show_bls_short():
    info = ("BLS PERIODOGRAM — SHORT PERIOD SEARCH (1–20 days)\n"
            "The Box Least Squares (BLS) algorithm tests thousands of trial periods to find "
            "a repeating box-shaped dip consistent with a transit. The y-axis shows BLS power "
            "(higher = better fit). The tallest peak indicates the most likely orbital period "
            "for a short-period planet. Harmonics (1/2, 1/3 of the true period) will also "
            "appear as smaller peaks.")
    def plot_fn():
        fig, ax = plt.subplots(figsize=(9, 4))
        bls = state["bls_short"]
        ax.plot(bls.period.value, bls.power.value, color=ACCENT, lw=0.8, alpha=0.9)
        pb = state["planet_b"]
        ax.axvline(pb["period"].value, color=SUCCESS, lw=1.5, linestyle="--",
                   label=f"Best period: {pb['period'].value:.3f} d")
        ax.legend(fontsize=8, facecolor=PANEL, labelcolor=TEXT)
        apply_plot_style(ax, "BLS Periodogram (Short Period Search)", "Period (days)", "BLS Power")
        fig.tight_layout()
        return fig, [ax]
    open_plot_window("BLS Periodogram — Short Period", info, plot_fn)


#plot 3: planet b: phase folded transit
def show_folded_b():
    pb = state["planet_b"]
    info = (f"PHASE-FOLDED TRANSIT — PLANET b  (period ≈ {pb['period'].value:.4f} days)\n"
            "Phase-folding 'stacks' every transit on top of each other by aligning them to "
            "the same orbital phase. If a real planet is present, all the individual transits "
            "line up and the dip becomes clear. The red curve is the BLS best-fit transit model. "
            "The x-axis is time relative to mid-transit (in days).")
    def plot_fn():
        fig, ax = plt.subplots(figsize=(9, 4))
        folded = state["lc"].fold(pb["period"], pb["t0"])
        folded.scatter(ax=ax, s=2, color=ACCENT, alpha=0.5, label="Flux")
        pb["model"].fold(pb["period"], pb["t0"]).plot(ax=ax, c=ACCENT2, lw=2, label="BLS Model")
        ax.set_xlim(-5, 5)
        ax.legend(fontsize=8, facecolor=PANEL, labelcolor=TEXT)
        apply_plot_style(ax, f"Phase-Folded Transit — Planet b  (P = {pb['period'].value:.4f} d)",
                         "Time from Mid-Transit (days)", "Normalized Flux")
        fig.tight_layout()
        return fig, [ax]
    open_plot_window("Phase-Folded Transit — Planet b", info, plot_fn)


#plot 4, masked light curve
def show_masked():
    info = ("MASKED LIGHT CURVE\n"
            "To search for a second planet, the cadences (data points) that belong to Planet b's "
            "transits are masked out (shown in red). The remaining blue points are then used for "
            "a second BLS search. This prevents Planet b's strong signal from overwhelming "
            "any fainter signals.")
    def plot_fn():
        fig, ax = plt.subplots(figsize=(9, 4))
        lc = state["lc"]
        mask = state["planet_b"]["mask"]
        lc[~mask].scatter(ax=ax, s=1, color=ACCENT, alpha=0.5, label="Unmasked")
        lc[mask].scatter(ax=ax, s=4, color=ACCENT2, alpha=0.8, label="Masked (Planet b transits)")
        ax.legend(fontsize=8, facecolor=PANEL, labelcolor=TEXT)
        apply_plot_style(ax, "Light Curve with Planet b Transits Masked",
                         "Time (BKJD)", "Normalized Flux")
        fig.tight_layout()
        return fig, [ax]
    open_plot_window("Masked Light Curve", info, plot_fn)


#plot 5, blas periodogram
def show_bls_long():
    info = ("BLS PERIODOGRAM — LONG PERIOD SEARCH (1–300 days)\n"
            "After masking Planet b, we repeat the BLS search over a much wider range of periods "
            "(up to 300 days). Longer-period planets have fewer transits in the data, so the BLS "
            "power is generally lower. A clear peak still indicates a credible transit signal. "
            "Look for the tallest peak to identify Planet c's orbital period.")
    def plot_fn():
        fig, ax = plt.subplots(figsize=(9, 4))
        bls = state["bls_long"]
        ax.plot(bls.period.value, bls.power.value, color=ACCENT, lw=0.8, alpha=0.9)
        pc = state["planet_c"]
        ax.axvline(pc["period"].value, color=ACCENT2, lw=1.5, linestyle="--",
                   label=f"Best period: {pc['period'].value:.3f} d")
        ax.legend(fontsize=8, facecolor=PANEL, labelcolor=TEXT)
        apply_plot_style(ax, "BLS Periodogram (Long Period Search)", "Period (days)", "BLS Power")
        fig.tight_layout()
        return fig, [ax]
    open_plot_window("BLS Periodogram — Long Period", info, plot_fn)


#plot 6: planet c: phase-folded transit
def show_folded_c():
    pc = state["planet_c"]
    info = (f"PHASE-FOLDED TRANSIT — PLANET c  (period ≈ {pc['period'].value:.4f} days)\n"
            "Same as the Planet b phase-fold, but using the masked light curve and Planet c's "
            "period. Because Planet c has a longer period, fewer transits have been observed, "
            "making the signal noisier. The red binned curve averages groups of points to reveal "
            "the transit shape more clearly.")
    def plot_fn():
        fig, ax = plt.subplots(figsize=(9, 4))
        masked = state["masked_lc"]
        folded = masked.fold(pc["period"], pc["t0"])
        folded.scatter(ax=ax, s=2, color=ACCENT, alpha=0.5, label="Flux")
        folded.bin(0.1).plot(ax=ax, c=ACCENT2, lw=2, label="Binned Flux")
        ax.set_xlim(-5, 5)
        ax.legend(fontsize=8, facecolor=PANEL, labelcolor=TEXT)
        apply_plot_style(ax, f"Phase-Folded Transit — Planet c  (P = {pc['period'].value:.4f} d)",
                         "Time from Mid-Transit (days)", "Normalized Flux")
        fig.tight_layout()
        return fig, [ax]
    open_plot_window("Phase-Folded Transit — Planet c", info, plot_fn)


#plot 7, transit model overlay
def show_both_models():
    info = ("TRANSIT MODEL OVERLAY\n"
            "This shows the full light curve with BLS transit models for both planet candidates "
            "overlaid. Blue ticks mark the predicted transit times for Planet b; pink ticks mark "
            "Planet c. Visually confirming that the model dips align with real dips in the data "
            "is a key validation step.")
    def plot_fn():
        fig, ax = plt.subplots(figsize=(9, 4))
        state["lc"].scatter(ax=ax, s=1, color=SUBTEXT, alpha=0.4, label="Flux")
        state["planet_b"]["model"].plot(ax=ax, c=ACCENT, lw=1.5, label="Planet b model")
        state["planet_c"]["model"].plot(ax=ax, c=ACCENT2, lw=1.5, label="Planet c model")
        ax.legend(fontsize=8, facecolor=PANEL, labelcolor=TEXT)
        apply_plot_style(ax, "Transit Model Overlay — Both Planets",
                         "Time (BKJD)", "Normalized Flux")
        fig.tight_layout()
        return fig, [ax]
    open_plot_window("Both Transit Models", info, plot_fn)


#button stuff
plot_buttons = []

def enable_buttons():
    for btn in plot_buttons:
        btn.config(state="normal")

#main window
root = tk.Tk()
root.title("Planet Detector")
root.configure(bg=BG)
root.geometry("1600x1100")
root.minsize(900, 600)

#top header
header = tk.Frame(root, bg=PANEL, pady=12)
header.pack(fill="x")

tk.Label(header, text="Planet Detector",
         bg=PANEL, fg=ACCENT, font=("Courier New", 16, "bold")).pack(side="left", padx=20)
tk.Label(header, text="Transit Detection Tool",
         bg=PANEL, fg=SUBTEXT, font=("Courier New", 10)).pack(side="left", padx=4)

#main layout
body = tk.Frame(root, bg=BG)
body.pack(fill="both", expand=True, padx=12, pady=12)

sidebar = tk.Frame(body, bg=PANEL, width=380, padx=14, pady=14)
sidebar.pack(side="left", fill="y", padx=(0, 10))
sidebar.pack_propagate(False)

right = tk.Frame(body, bg=PANEL, padx=14, pady=14)
right.pack(side="left", fill="both", expand=True)

#file loader
tk.Label(sidebar, text="FILE", bg=PANEL, fg=ACCENT,
         font=("Courier New", 9, "bold")).pack(anchor="w")
ttk.Separator(sidebar, orient="horizontal").pack(fill="x", pady=4)

load_btn = tk.Button(sidebar, text="Load FITS File",
                     bg=ACCENT, fg=BG, font=("Courier New", 10, "bold"),
                     relief="flat", cursor="hand2", pady=6, command=load_file)
load_btn.pack(fill="x", pady=(0, 6))

file_label = tk.Label(sidebar, text="No file loaded", bg=PANEL, fg=SUBTEXT,
                      font=("Courier New", 8), wraplength=220, justify="left")
file_label.pack(anchor="w", pady=(0, 10))

#graph buttons
tk.Label(sidebar, text="GRAPHS", bg=PANEL, fg=ACCENT,
         font=("Courier New", 9, "bold")).pack(anchor="w", pady=(10, 0))
ttk.Separator(sidebar, orient="horizontal").pack(fill="x", pady=4)

graph_defs = [
    ("1 · Light Curve",               show_light_curve),
    ("2 · BLS Periodogram (short)",   show_bls_short),
    ("3 · Planet b — Phase Fold",     show_folded_b),
    ("4 · Masked Light Curve",        show_masked),
    ("5 · BLS Periodogram (long)",    show_bls_long),
    ("6 · Planet c — Phase Fold",     show_folded_c),
    ("7 · Both Transit Models",       show_both_models),
]

for label, cmd in graph_defs:
    btn = tk.Button(sidebar, text=label, bg=BORDER, fg=TEXT,
                    font=("Courier New", 9), relief="flat",
                    cursor="hand2", pady=5, anchor="w", padx=8,
                    activebackground=ACCENT, activeforeground=BG,
                    state="disabled", command=cmd)
    btn.pack(fill="x", pady=2)
    plot_buttons.append(btn)

#status bar
status_var = tk.StringVar(value="Load a FITS file to begin.")
tk.Label(sidebar, textvariable=status_var, bg=PANEL, fg=SUBTEXT,
         font=("Courier New", 8), wraplength=300, justify="left").pack(anchor="w", pady=(14, 0))

#results
tk.Label(right, text="ANALYSIS RESULTS", bg=PANEL, fg=ACCENT,
         font=("Courier New", 10, "bold")).pack(anchor="w")
ttk.Separator(right, orient="horizontal").pack(fill="x", pady=4)

#scrollbar
results_container = tk.Frame(right, bg=PANEL)
results_container.pack(fill="both", expand=True)

canvas = tk.Canvas(results_container, bg=PANEL, highlightthickness=0)
scrollbar = tk.Scrollbar(results_container, orient="vertical", command=canvas.yview)

scrollable_frame = tk.Frame(canvas, bg=PANEL)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

results_frame = scrollable_frame

#placeholder text
tk.Label(results_frame,
         text="Loading data...",
         bg=PANEL, fg=SUBTEXT,
         font=("Courier New", 9), justify="left").pack(anchor="w", pady=20)

load_file()
root.mainloop()