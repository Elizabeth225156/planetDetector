from astropy.io import fits
from astropy.table import Table 
import matplotlib.pyplot as plt

def main():
    filename = "./mastDownload/Kepler/kplr011446443_sc_Q113313330333033302/kplr011446443-2009131110544_slc.fits"
    fits.info(filename)

    with fits.open(filename) as hdulist:
        binaryext = hdulist[1].data

    binarytable = Table(binaryext)
    binarytable[1:5] #the table with the data being printed


    with fits.open(filename, mode="readonly") as hdulist:
        # Read in the "BJDREF" which is the time offset of the time array.
        bjdrefi = hdulist[1].header['BJDREFI'] 
        bjdreff = hdulist[1].header['BJDREFF']

        # Read in the columns of data.
        times = hdulist[1].data['time'] 
        sap_fluxes = hdulist[1].data['SAP_FLUX']
        pdcsap_fluxes = hdulist[1].data['PDCSAP_FLUX']

        # Convert the time array to full BJD by adding the offset back in.
    bjds = times + bjdrefi + bjdreff 

    with fits.open(filename) as hdulist: 
        imgdata = hdulist[2].data
        
    print(imgdata)

    plt.figure(figsize=(9,4))

    # Plot the time, uncorrected and corrected fluxes.
    plt.plot(bjds, sap_fluxes, '-k', label='SAP Flux') 
    plt.plot(bjds, pdcsap_fluxes, '-b', label='PDCSAP Flux') 

    plt.title('Kepler Light Curve')
    plt.legend()
    plt.xlabel('Time (days)')
    plt.ylabel('Flux (electrons/second)')

    plt.figure(2)
    plt.title('Kepler Aperture')
    plt.imshow(imgdata, cmap=plt.cm.YlGnBu_r)
    plt.xlabel('Column')
    plt.ylabel('Row')
    plt.colorbar()
    plt.show()

main()