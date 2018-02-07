from gwpy.table import EventTable


def searchDB(form):

    # process the data in form.cleaned_data as required
    if len(str(form.cleaned_data['imageid'])) > 6:
        uniqueID = str(form.cleaned_data['imageid']).split(',')
    else:
        uniqueID = None


    # process the data in form.cleaned_data as required
    if len(str(form.cleaned_data['zooid'])) > 6:
        zooID = str(form.cleaned_data['zooid']).split(',')
    else:
        zooID = None

    if uniqueID:
        SI_glitches = EventTable.fetch('gravityspy', 'glitches WHERE "uniqueID" IN (\'{0}\')'.format(str("','".join(uniqueID))), columns = ['uniqueID', 'imgUrl1', 'imgUrl2', 'imgUrl3', 'imgUrl4', 'ifo', 'links_subjects', 'snr', 'peak_frequency', 'Label']).to_pandas()
    elif zooID:
        SI_glitches = EventTable.fetch('gravityspy', 'glitches WHERE CAST(links_subjects AS TEXT) IN (\'{0}\')'.format(str("','".join(zooID))), columns = ['uniqueID', 'imgUrl1', 'imgUrl2', 'imgUrl3', 'imgUrl4', 'ifo', 'links_subjects', 'snr', 'peak_frequency', 'Label']).to_pandas()
    else:
        SI_glitches = EventTable.fetch('gravityspy', 'glitches', columns = ['uniqueID', 'imgUrl1', 'imgUrl2', 'imgUrl3', 'imgUrl4', 'ifo', 'links_subjects', 'snr', 'peak_frequency', 'Label']).to_pandas()

    return SI_glitches
