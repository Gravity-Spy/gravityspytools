from gwpy.table import EventTable
from search.utils import makelink


def searchDB(form):

    # process the data in form.cleaned_data as required
    # process the data in form.cleaned_data as required
    glitchclass = str(form.cleaned_data['glitchclass'])

    SI_glitches = EventTable.fetch('gravityspy', 'trainingset WHERE \"Label\" = \'{0}\''.format(glitchclass), columns = ['uniqueID', 'Filename1', 'Filename2', 'Filename3', 'Filename4', 'ifo', 'snr', 'peak_frequency', 'Label']).to_pandas()

    SI_glitches['imgUrl1'] = SI_glitches[['ifo', 'Filename1']].apply(makelink, axis=1)
    SI_glitches['imgUrl2'] = SI_glitches[['ifo', 'Filename2']].apply(makelink, axis=1)
    SI_glitches['imgUrl3'] = SI_glitches[['ifo', 'Filename3']].apply(makelink, axis=1)
    SI_glitches['imgUrl4'] = SI_glitches[['ifo', 'Filename4']].apply(makelink, axis=1)

    return SI_glitches
