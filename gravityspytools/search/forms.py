from django import forms
from gwpy.table import EventTable


def get_imageid_json(name=''):
    return EventTable.fetch('gravityspy', 'similarity_index_o3 WHERE \"gravityspy_id\" ~ \'{0}\' LIMIT 20'.format(name), columns=["gravityspy_id"]).to_pandas().rename(columns={'gravityspy_id': 'value'}).to_json(orient='records')


def get_zooid_json(name=''):
    return EventTable.fetch('gravityspy', 'similarity_index_o3 WHERE CAST(links_subjects AS TEXT) ~ \'{0}\' LIMIT 20'.format(name), columns=["links_subjects"]).to_pandas().astype(str).rename(columns={'links_subjects': 'value'}).to_json(orient='records')


def get_gpstimes_json(name=''):
    return EventTable.fetch('gravityspy', 'similarity_index_o3 WHERE CAST(\"event_time\" AS TEXT) ~ \'{0}\' LIMIT 20'.format(name), columns=["event_time"]).to_pandas().astype(str).rename(columns={'event_time': 'value'}).to_json(orient='records')


class SearchForm(forms.Form):

    SINGLEVIEW = 'similarityindex'
    MULTIVIEW = 'similarity_index_o3'

    DATABASE_CHOICES = (
        (MULTIVIEW, 'Multiview Model'),
        (SINGLEVIEW, 'Single View Model'),
    )

    H1 = "\'H1\'"
    H1L1 = "\'H1\', \'L1\'"
    H1L1V1 = "\'H1\', \'L1\', \'V1\'"
    L1 = "\'L1\'"
    L1V1 = "\'L1\', \'V1\'"
    V1 = "\'V1\'"

    IFO_CHOICES = (
        (H1L1, 'H1 L1'),
        (H1, 'H1'),
        (H1L1V1, 'H1 L1 V1'),
        (L1, 'L1'),
        (L1V1, 'L1 V1'),
        (V1, 'V1'),
    )

    ALL = "event_time BETWEEN 1126400000 AND 1584057618"
    O1 = "event_time BETWEEN 1126400000 AND 1137250000"
    ER10 = "event_time BETWEEN 1161907217 AND 1164499217"
    O2a = "event_time BETWEEN 1164499217 AND 1219276818"
    ER13 = "event_time BETWEEN 1228838418 AND 1229176818"
    ER14 = "event_time BETWEEN 1235750418 AND 1238112018"
    O3a = "event_time BETWEEN 1238166018 AND 1254009618"
    O3b = "event_time BETWEEN 1256655642 AND 1272326418"
    O3 = "event_time BETWEEN 1238166018 AND 1272326418"
    ERAS = (
        (ALL, 'ALL'),
        (O1, 'O1'),
        (ER10, 'ER10'),
        (O2a, 'O2a'),
        (ER13, 'ER13'),
        (ER14, 'ER14'),
        (O3a, 'O3a'),
        (O3b, 'O3b'),
        (O3, 'O3'),
    )

    database = forms.ChoiceField(choices=DATABASE_CHOICES,)
    howmany = forms.IntegerField(label='How many similar images would you like to return', max_value=200, min_value=1)
    zooid = forms.CharField(label = 'This is the Zooniverse assigned random ID of the image (an integer value)', max_length=10, required=False)
    imageid = forms.CharField(label='The GravitySpy uniqueid (this is the 10 character hash that uniquely identifies all gravity spy images)', max_length=10, required=False)
    ifo = forms.ChoiceField(choices=IFO_CHOICES,)
    era = forms.ChoiceField(choices=ERAS,)

    def clean(self):
        cleaned_data = super(SearchForm, self).clean()
        zooid = cleaned_data.get('zooid')
        imageid = cleaned_data.get('imageid')
        ifos = str(cleaned_data.get('ifo'))
        database = cleaned_data.get('database')
        era = cleaned_data.get('era')
 
        if zooid and imageid:
            raise forms.ValidationError("Please fill out "
                                        "only one of the zooid "
                                        "or gravityspy id fields"
                                        )

        elif (not zooid) and (not imageid):
            raise forms.ValidationError("Please fill out "
                                        "one but not both of the zooid "
                                        "and gravityspy id fields"
                                        )

        if zooid and not imageid:
            if not EventTable.fetch('gravityspy', 'nonanalysisreadyids WHERE links_subjects = {0}'.format(zooid)).to_pandas().empty:
                raise forms.ValidationError("This zooID is one of a handful of glitches that were mistakenly uploaded, despite being glitches"
                                            "occuring while the detector was not in a state to be taking quality data "
                                            "(i.e. people may have been working on the instrument at the time."
                                        )

            if EventTable.fetch('gravityspy', '{0} WHERE links_subjects = {1}'.format(database, zooid), columns=['links_subjects']).to_pandas().empty:
                    raise forms.ValidationError("zooid does not exist")

            elif EventTable.fetch('gravityspy', '{0} WHERE links_subjects = {1} AND ifo IN ({2})'.format(database, zooid, ifos), columns=['links_subjects']).to_pandas().empty:
                raise forms.ValidationError("This image is not from one of the interferometers you selected"
                                        )

        if imageid and not zooid:
            if not EventTable.fetch('gravityspy', 'nonanalysisreadyids WHERE \"gravityspy_id\" = \'{0}\''.format(imageid)).to_pandas().empty:
                raise forms.ValidationError("This gravityspy_id is one of a handful of glitches that were mistakenly uploaded, despite being glitches"
                                            "occuring while the detector was not in a state to be taking quality data "
                                            "(i.e. people may have been working on the instrument at the time."
                                            )

            if EventTable.fetch('gravityspy', '{0} WHERE \"gravityspy_id\" = \'{1}\''.format(database, imageid), columns=['gravityspy_id']).to_pandas().empty:
                raise forms.ValidationError("uniqueid does not exist")

            elif EventTable.fetch('gravityspy', '{0} WHERE \"gravityspy_id\" = \'{1}\' AND ifo IN ({2})'.format(database, imageid, ifos), columns=['gravityspy_id']).to_pandas().empty:
                raise forms.ValidationError("This image is not from one of the interferometers you selected"
                                            )


    def clean_zooid(self):
        zooid = self.cleaned_data['zooid']
        if not zooid:
            zooid = False

        return zooid

    def clean_imageid(self):
        imageid = self.cleaned_data['imageid']
        if not imageid:
            imageid = False

        return imageid


class LIGOSearchForm(forms.Form):
    howmany = forms.IntegerField(label='How many similar images would you like to return', max_value=200, min_value=1)
    zooid = forms.CharField(label = 'This is the Zooniverse assigned random ID of the image (an integer value)', max_length=10, required=False)
    imageid = forms.CharField(label='The GravitySpy uniqueid (this is the 10 character hash that uniquely identifies all gravity spy images)', max_length=10, required=False)
    gpstime = forms.CharField(label = 'Supply a gps time of an excess noise feature', required=False) 
    SINGLEVIEW = 'similarityindex'
    MULTIVIEW = 'similarity_index_o3'

    DATABASE_CHOICES = (
        (MULTIVIEW, 'Multiview Model'),
        (SINGLEVIEW, 'Single View Model'),
    )

    H1 = "\'H1\'"
    H1L1 = "\'H1\', \'L1\'"
    H1L1V1 = "\'H1\', \'L1\', \'V1\'"
    L1 = "\'L1\'"
    L1V1 = "\'L1\', \'V1\'"
    V1 = "\'V1\'"

    IFO_CHOICES = (
        (H1L1, 'H1 L1'),
        (H1, 'H1'),
        (H1L1V1, 'H1 L1 V1'),
        (L1, 'L1'),
        (L1V1, 'L1 V1'),
        (V1, 'V1'),
    )

    ALL = "event_time BETWEEN 1126400000 AND 1584057618"
    O1 = "event_time BETWEEN 1126400000 AND 1137250000"
    ER10 = "event_time BETWEEN 1161907217 AND 1164499217"
    O2a = "event_time BETWEEN 1164499217 AND 1219276818"
    ER13 = "event_time BETWEEN 1228838418 AND 1229176818"
    ER14 = "event_time BETWEEN 1235750418 AND 1238112018"
    O3a = "event_time BETWEEN 1238166018 AND 1254009618"
    O3b = "event_time BETWEEN 1256655642 AND 1272326418"
    O3 = "event_time BETWEEN 1238166018 AND 1272326418"
    ERAS = (
        (ALL, 'ALL'),
        (O1, 'O1'),
        (ER10, 'ER10'),
        (O2a, 'O2a'),
        (ER13, 'ER13'),
        (ER14, 'ER14'),
        (O3a, 'O3a'),
        (O3b, 'O3b'),
        (O3, 'O3'),
    )

    ifo = forms.ChoiceField(choices=IFO_CHOICES,)
    database = forms.ChoiceField(choices=DATABASE_CHOICES,)
    era = forms.ChoiceField(choices=ERAS,)
    def clean(self):
        cleaned_data = super(LIGOSearchForm, self).clean()
        zooid = cleaned_data.get('zooid')
        imageid = cleaned_data.get('imageid')
        gpstime = cleaned_data.get('gpstime')
        ifos = cleaned_data.get('ifo')
        database = cleaned_data.get('database')

        if (zooid and imageid and gpstime) or (zooid and imageid) or \
               (zooid and gpstime) or (gpstime and imageid):
            raise forms.ValidationError("Please fill out "
                                        "only one of the zooid "
                                        "or gravityspy id fields"
                                        )

        elif (not zooid) and (not imageid) and (not gpstime):
            raise forms.ValidationError("Please fill out "
                                        "one but not both of the zooid "
                                        "and gravityspy id fields"
                                        )

        if zooid and not imageid and not gpstime:
            if EventTable.fetch('gravityspy', '{0} WHERE links_subjects = {1}'.format(database, zooid), columns=['links_subjects']).to_pandas().empty:
                raise forms.ValidationError("zooid does not exist"
                                        )

        if imageid and not zooid and not gpstime:
            if EventTable.fetch('gravityspy', '{0} WHERE \"gravityspy_id\" = \'{1}\''.format(database, imageid), columns=['gravityspy_id']).to_pandas().empty:
                raise forms.ValidationError("uniqueid does not exist"
                                        )

    def clean_zooid(self):
        zooid = self.cleaned_data['zooid']
        if not zooid:
            zooid = False

        return zooid

    def clean_imageid(self):
        imageid = self.cleaned_data['imageid']
        if not imageid:
            imageid = False

        return imageid

    def clean_gpstime(self):
        gpstime = self.cleaned_data['gpstime']
        if not gpstime:
            gpstime = False

        return gpstime
