from matplotlib import use
use('agg')
from matplotlib import pyplot

import timeconvert
import datetime
from gwpy.time import from_gps

def obtain_figure(SI_glitches):
    SI_glitches['date'] = SI_glitches['peak_time'].apply(from_gps)

    newestGPS = SI_glitches['date'].max() 
    oldestGPS = SI_glitches['date'].min()

    bins = (newestGPS - oldestGPS).days/7
    if bins == 0:
        bins = 1

    ax = SI_glitches['date'].hist(bins=bins, xrot=45)
    fig = ax.get_figure()

    ax.set_xlabel("Weeks")
    ax.set_ylabel("Number of Glitches per Week")
    ax.set_title("Distribution of Glitches \n Each Bin Represents One Week")

    pyplot.tight_layout()

    #checking and changing xlocs, xlabels
    return fig
