import os, string, random
from matplotlib import use
use('agg')
from matplotlib import (pyplot as plt, cm)


def id_generator(size=5, chars=string.ascii_uppercase + string.digits +string.ascii_lowercase):
    return ''.join(random.SystemRandom().choice(chars) for _ in range(size))


def make_gravityspy_image(eventTime, ifo, sampleFrequency=16384, blockTime=64):
    from gwpy.timeseries import TimeSeries
    from gwpy.spectrogram import Spectrogram
    from gwpy.segments import Segment

    import pyomega.ML.make_pickle_for_linux as make_pickle
    import pyomega.ML.labelling_test_glitches as label_glitches

    import pandas as pd
    from sqlalchemy.engine import create_engine

    import numpy as np
    import subprocess

    # find closest sample time to event time
    centerTime = np.floor(eventTime) + \
               np.round((eventTime - np.floor(eventTime)) * \
                     sampleFrequency) / sampleFrequency

    # determine segment start and stop times
    eventTime = round(centerTime - blockTime / 2)
    stopTime = eventTime + blockTime

    # Read in the data
    channelName = '{0}:GDS-CALIB_STRAIN'.format(ifo)
    data = TimeSeries.get(channelName, eventTime, stopTime).astype('float64')

    specsgrams = []
    iTimeWindow = 1.0
    outseg = Segment(centerTime - 2, centerTime + 2)
    qScan = data.q_transform(qrange=(4, 64), frange=(10, 2048),
                         gps=centerTime, search=0.5, tres=0.002,
                         fres=0.5, outseg=outseg, whiten=True)
    qScan = qScan.crop(centerTime-iTimeWindow/2, centerTime+iTimeWindow/2)

    image, ID = plot_gravityspy_image(qScan, eventTime, ifo)

    # Get ML semantic index image data
    image_dataDF = pd.DataFrame()
    image_data = make_pickle.main(image, resolution=0.3)
    image_dataDF[image.split('/')[-1]] = [image_data]

    pathToModel = subprocess.check_output(["which", "semantic_idx_model.h5"]).split('semantic_idx_model.h5')[0] 

    # Determine features
    features = label_glitches.get_feature_space(image_data=image_dataDF,
                                          semantic_model_adr='{0}'.format(pathToModel),
                                          image_size=[140, 170],
                                          verbose=False)

    features = pd.DataFrame(features)
    features['uniqueID'] = ID

    engine = create_engine('postgresql://{0}:{1}@gravityspy.ciera.northwestern.edu:5432/gravityspy'.format(os.environ['GRAVITYSPY_DATABASE_USER'], os.environ['GRAVITYSPY_DATABASE_PASSWD']))
    features.to_sql('similarityindex_temporary', engine, index=False, if_exists='append')

    return image, ID


def plot_gravityspy_image(qScan, eventTime, ifo):
    import numpy as np
    from matplotlib.ticker import ScalarFormatter
    from gwpy.plotter.rc import rcParams
    import matplotlib as mpl
    mpl.rcParams.update(mpl.rcParamsDefault)

    from gwpy.plotter import Plot

    # Set some plotting params
    myfontsize = 15
    mylabelfontsize = 20
    myColor = 'k'
    iTimeWindow = 1.0

    if ifo == 'H1':
        title = "Hanford"
    elif ifo == 'L1':
        title = "Livingston"
    elif ifo == 'V1':
        title = "VIRGO"
    else:
        raise ValueError('You have supplied a detector that is unknown at this time')

    if 1161907217 < eventTime < 1164499217:
        title = title + ' - ER10'
    elif eventTime > 1164499217:
        title = title + ' - O2a'
    elif 1126400000 < eventTime < 1137250000:
        title = title + ' - O1'
    else:
        raise ValueError("Time outside science or engineering run\
                   or more likely code not updated to reflect\
                   new science run")

    indFig = Plot(figsize=[8, 6])
    indFig.add_spectrogram(qScan)

    ax = indFig.gca()
    ax.set_position([0.125, 0.1, 0.775, 0.8])
    ax.set_yscale('log', basey=2)
    ax.set_xscale('linear')

    xticks = np.linspace(qScan.xindex.min().value, qScan.xindex.max().value, 5)
    xticklabels = []
    [xticklabels.append(str(i)) for i in np.linspace(-iTimeWindow/2, iTimeWindow/2, 5)]
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels)

    ax.set_xlabel('Time (s)', labelpad=0.1, fontsize=mylabelfontsize, color=myColor)
    ax.set_ylabel('Frequency (Hz)', fontsize=mylabelfontsize, color=myColor)
    ax.set_title(title, fontsize=mylabelfontsize, color=myColor)
    ax.title.set_position([.5, 1.05])
    ax.set_ylim(10, 2048)
    ax.yaxis.set_major_formatter(ScalarFormatter())
    ax.ticklabel_format(axis='y', style='plain')

    plt.tick_params(axis='x', which='major', labelsize=myfontsize)
    plt.tick_params(axis='y', which='major', labelsize=12)

    cbar = indFig.add_colorbar(cmap='viridis', label='Normalized energy',
                        clim=[0,25.5], pad="3%", width="5%")
    cbar.ax.tick_params(labelsize=12)
    cbar.ax.yaxis.label.set_size(myfontsize)

    ID = id_generator(size=10)
    os.makedirs(os.path.join('static', 'scans', ID, ID))
    imagepath = os.path.join('static', 'scans', ID, ID, ifo + '_' + ID +'_spectrogram_' + str(iTimeWindow) +'.png')
    indFig.save(imagepath)

    return imagepath, ID


def search_si_database(ID, howmany):
    from sqlalchemy.engine import create_engine
    import pandas as pd
    from gwpy.table import EventTable

    engine = create_engine('postgresql://{0}:{1}@gravityspy.ciera.northwestern.edu:5432/gravityspy'.format(os.environ['GRAVITYSPY_DATABASE_USER'], os.environ['GRAVITYSPY_DATABASE_PASSWD']))

    PostGresEuclideanDistanceQuery = 'WITH searcharray AS (SELECT cube(array["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "60", "61", "62", "63", "64", "65", "66", "67", "68", "69", "70", "71", "72", "73", "74", "75", "76", "77", "78", "79", "80", "81", "82", "83", "84", "85", "86", "87", "88", "89", "90", "91", "92", "93", "94", "95", "96", "97", "98", "99", "100", "101", "102", "103", "104", "105", "106", "107", "108", "109", "110", "111", "112", "113", "114", "115", "116", "117", "118", "119", "120", "121", "122", "123", "124", "125", "126", "127", "128", "129", "130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "140", "141", "142", "143", "144", "145", "146", "147", "148", "149", "150", "151", "152", "153", "154", "155", "156", "157", "158", "159", "160", "161", "162", "163", "164", "165", "166", "167", "168", "169", "170", "171", "172", "173", "174", "175", "176", "177", "178", "179", "180", "181", "182", "183", "184", "185", "186", "187", "188", "189", "190", "191", "192", "193", "194", "195", "196", "197", "198", "199"]) FROM similarityindex_temporary WHERE "uniqueID" = \'{0}\'), t AS (SELECT "uniqueID", links_subjects, cube(array["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "60", "61", "62", "63", "64", "65", "66", "67", "68", "69", "70", "71", "72", "73", "74", "75", "76", "77", "78", "79", "80", "81", "82", "83", "84", "85", "86", "87", "88", "89", "90", "91", "92", "93", "94", "95", "96", "97", "98", "99", "100", "101", "102", "103", "104", "105", "106", "107", "108", "109", "110", "111", "112", "113", "114", "115", "116", "117", "118", "119", "120", "121", "122", "123", "124", "125", "126", "127", "128", "129", "130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "140", "141", "142", "143", "144", "145", "146", "147", "148", "149", "150", "151", "152", "153", "154", "155", "156", "157", "158", "159", "160", "161", "162", "163", "164", "165", "166", "167", "168", "169", "170", "171", "172", "173", "174", "175", "176", "177", "178", "179", "180", "181", "182", "183", "184", "185", "186", "187", "188", "189", "190", "191", "192", "193", "194", "195", "196", "197", "198", "199"]) FROM similarityindex) SELECT "uniqueID", "links_subjects" FROM t order by (SELECT * FROM searcharray) <#> cube asc limit {1};'.format(ID, howmany)

    # Query Similarity Index to give you the most similar IDs
    SI = pd.read_sql(PostGresEuclideanDistanceQuery, engine)
    # Quest glitches DB to get all the metadata on the images that were returned by SI
    glitches = EventTable.fetch('gravityspy', 'glitches WHERE "uniqueID" IN (\'{0}\')'.format(str("','".join(list(SI['uniqueID'])))), columns = ['uniqueID', 'imgUrl1', 'imgUrl2', 'imgUrl3', 'imgUrl4', 'ifo', 'links_subjects', 'snr', 'peak_frequency', 'Label'])

    # Convert from astropy to pandas for easy manipulation
    SI_glitches = glitches.to_pandas()

    return SI_glitches
