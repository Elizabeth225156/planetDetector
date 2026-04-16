from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np

dvt_file = "https://archive.stsci.edu/missions/kepler/dv_files/0114/011446443/kplr011446443-20160128150956_dvt.fits"

with fits.open(dvt_file, mode="readonly") as hdulist:
    # Extract stellar parameters from the primary header.  We'll get the effective temperature, surface gravity,
    # and Kepler magnitude.
    star_teff = hdulist[0].header['TEFF']
    star_logg = hdulist[0].header['LOGG']
    star_tmag = hdulist[0].header['KEPMAG']
    
    # Extract some of the fit parameters for the first TCE.  These are stored in the FITS header of the first
    # extension.
    period = hdulist[1].header['TPERIOD']
    duration = hdulist[1].header['TDUR']
    epoch = hdulist[1].header['TEPOCH']
    depth = hdulist[1].header['TDEPTH']
    
    # Extract some of the columns of interest for the TCE signal.  These are stored in the binary FITS table
    # in the first extension.  We'll extract the timestamps in BKJD, phase, initial fluxes, and corresponding
    # model fluxes.
    times = hdulist[1].data['TIME']
    phases = hdulist[1].data['PHASE']
    fluxes_init = hdulist[1].data['LC_INIT']
    model_fluxes_init = hdulist[1].data['MODEL_INIT']

# First sort the phase and flux arrays by phase so we can draw the connecting lines between points.
sort_indexes = np.argsort(phases)

# Start figure and axis.
fig, ax = plt.subplots(figsize=(12,4))

# Plot the detrended fluxes as black circles.  We will plot them in sorted order.
ax.plot(phases[sort_indexes], fluxes_init[sort_indexes], 'ko',
       markersize=2)

# Plot the model fluxes as a red line.  We will plot them in sorted order so the line connects between points cleanly.
ax.plot(phases[sort_indexes], model_fluxes_init[sort_indexes], '-r')

# Let's label the axes and define a title for the figure.
fig.suptitle('KIC 11446443 - Folded Light Curve And Transit Model.')
ax.set_ylabel("Flux (relative)")
ax.set_xlabel("Orbital Phase")

# Let's add some text in the top-right containing some of the fit parameters.
plt.text(0.3, 0.005, "Period = {0:10.6f} days".format(period))
plt.text(0.3, 0.003, "Duration = {0:10.6f} hours".format(duration))
plt.text(0.3, 0.001, "Depth = {0:10.6f} ppm".format(depth))
plt.text(0.95, 0.005, "Star Teff = {0:10.6f} K".format(star_teff))
plt.text(0.95, 0.003, "Star log(g) = {0:10.6f}".format(star_logg))

plt.show()