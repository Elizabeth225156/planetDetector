import numpy as np
from astropy.io import fits
from astropy.table import Table
import matplotlib.pyplot as plt

def main():
    filename = "./mastDownload/Kepler/kplr008957091_lc_Q000000000011111111/kplr008957091-2012277125453_lpd-targ.fits.gz"
    #fits.info(filename)

    which_one_to_open = input("Enter the number of frame you want to see: ")
    plot_frame(which_one_to_open, filename)

def plot_frame(row, file):

    with fits.open(file) as hdulist:
        binaryext = hdulist[1].data
    
    binarytab = Table(binaryext)
    binarytab[0:4]

    binarytab['FLUX'][0]

    plt.title('Flux Row ' + str(row))
    plt.xlabel('Column')
    plt.ylabel('Row')

    plt.imshow(binarytab['FLUX'][int(row)], cmap=plt.cm.YlGnBu_r)
    plt.colorbar()
    plt.clim(0,300)
    # aperature_thing(file)
    plt.show()

def diff_between_frames():
    # arr = np.subtract(binarytab['FLUX'][28], binarytab['FLUX'][29])
    # print(arr)
    # plt.title('Flux Row 28 minus 29')
    # plt.xlabel('Column')
    # plt.ylabel('Row')

    # plt.imshow(arr, cmap=plt.cm.YlGnBu_r)
    # plt.colorbar()
    # plt.clim(-4, 12)
    pass

def aperature_thing(file):
    with fits.open(file) as hdulist: 
        imgdata = hdulist[2].data
    print(imgdata)
    plt.figure()
    plt.title('TPF APERTURE')
    plt.xlabel('Column')
    plt.ylabel('Row')
    plt.imshow(imgdata, cmap=plt.cm.YlGnBu_r)
    plt.show()
    
main()