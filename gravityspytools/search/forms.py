from django import forms
from gwpy.table import EventTable


def get_imageid_json(name=''):
    return EventTable.fetch('gravityspy', 'similarityindex WHERE \"uniqueID\" ~ \'{0}\' LIMIT 100'.format(name), columns=["uniqueID"]).to_pandas().rename(columns={'uniqueID': 'value'}).to_json(orient='records')


def get_zooid_json(name=''):
    return EventTable.fetch('gravityspy', 'similarityindex WHERE CAST(links_subjects AS TEXT) ~ \'{0}\' LIMIT 100'.format(name), columns=["links_subjects"]).to_pandas().astype(str).rename(columns={'links_subjects': 'value'}).to_json(orient='records')


class SearchForm(forms.Form):
    howmany = forms.IntegerField(label='How many similar images would you like to return', max_value=200, min_value=1)
    zooid = forms.CharField(label = 'This is the Zooniverse assigned random ID of the image (an integer value)', max_length=10, required=False)
    imageid = forms.CharField(label='The GravitySpy uniqueid (this is the 10 character hash that uniquely identifies all gravity spy images)', max_length=10, required=False)
    def clean(self):
        cleaned_data = super(SearchForm, self).clean()
        zooid = cleaned_data.get('zooid')
        imageid = cleaned_data.get('imageid')

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
            if EventTable.fetch('gravityspy', 'similarityindex WHERE links_subjects = {0}'.format(zooid), columns=['links_subjects']).to_pandas().empty:
                print "I amde it"
                raise forms.ValidationError("zooid does not exist"
                                        )

        if imageid and not zooid:
            if EventTable.fetch('gravityspy', 'similarityindex WHERE \"uniqueID\" = \'{0}\''.format(imageid), columns=['uniqueID']).to_pandas().empty:
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
