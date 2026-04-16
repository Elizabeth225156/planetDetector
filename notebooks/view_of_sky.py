# Imports for working with data
import numpy as np
from astropy.coordinates import SkyCoord, ICRS
from astropy import units
from astroquery.mast import Observations

# Imports for plotting images
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, LinearSegmentedColormap
from matplotlib.image import imread
from matplotlib import patheffects

# Update Plotting Parameters
params = {
    "axes.labelsize": 12,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "text.usetex": False,
    "lines.linewidth": 1,
    "axes.titlesize": 18,
    "font.family": "serif",
    "font.size": 12,
}
plt.rcParams.update(params)

# Load in the file
mast_data = np.load("mast_obscounts.npz")

ra_coords = mast_data["ra"]
dec_coords = mast_data["dec"]
observation_counts = mast_data["data"]

# Initiate plot - 16:9 aspect ratio for wallpaper
plt.figure(figsize=(16, 9))

ax = plt.subplot()

# Make the background of the plot black
plt.style.use("dark_background")
plt.axvspan(0, 360, color="k", zorder=-1)

# Define a custom color map
# This will create a gradient from black to blue to white!
# colormap = LinearSegmentedColormap.from_list(
#     "", ["black", "midnightblue", "#1a619f", "deepskyblue", "white"]
# )
colormap = "viridis"


# Plot the data
im = ax.imshow(
    observation_counts.T,
    cmap=colormap,  # Set colormap
    norm=LogNorm(10, 1e3),  # Define limits of colormap
    extent=[0, 360, -90, 90],  # Set the limits of the data
    origin="lower",
)

# Set axes limits
plt.xlim(0, 360)
plt.ylim(-90, 90)

# turn off axes
plt.axis("off")
# Force aspect ratio 16:9
ax.set_aspect("auto")

# # Save file
# plt.savefig("mast_wallpaper.png", bbox_inches="tight", dpi=300)

# plt.savefig("mast_visualization.png", bbox_inches="tight")
plt.show()