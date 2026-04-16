import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from astropy.table import Table
import matplotlib.pyplot as plt
from astroquery.mast import Catalogs

filename = "./mastDownload/KeplerFFI/kplr2009170043915_84/kplr2009170043915_ffi-cal.fits"

with fits.open(filename) as hdulist:
    imgdata = hdulist[1].data

catalogData = Catalogs.query_region("290.4620065226813  38.32946356799192", radius="0.2 deg", catalog="TIC")
dattab = Table(catalogData)

radec = (catalogData['ra','dec','Bmag'])
mask = radec['Bmag'] < 15.0
mag_radec = radec[mask]
print(mag_radec)

hdu = fits.open(filename)[1]
wcs = WCS(hdu.header)

fig = plt.figure(figsize=(20,10))
ax = plt.subplot(projection=wcs) 
im = ax.imshow(hdu.data, cmap=plt.cm.gray, origin='lower', clim=(0,20000))
fig.colorbar(im)

plt.title('FFI with TIC Catalog Objects')
ax.set_xlabel('RA [deg]')
ax.set_ylabel('Dec [deg]')
ax.grid(color='white', ls='solid')
ax.autoscale(False)

ax.scatter(mag_radec['ra'], mag_radec['dec'],
           facecolors='none', edgecolors='c', linewidths=0.5,
           transform=ax.get_transform('icrs')) # This is needed when projecting onto axes with WCS info


plt.show()