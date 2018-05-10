from django import forms
import panoptes_client


class SearchForm(forms.Form):
    username = forms.CharField(label='The Zoo username of the collection owner', max_length=100)
    collection_display_name = forms.CharField(label='The display name of the collection as it is in the url. If the collecion url is https://www.zooniverse.org/collections/sbc538/45hz then 45hz would go here')

    def clean(self):
        cleaned_data = super(SearchForm, self).clean()
        username = cleaned_data.get('username')
        collection_display_name = cleaned_data.get('collection_display_name')

        tmp = panoptes_client.Collection.where(slug='{0}/{1}'.format(username, collection_display_name))
        try:
            tmp.next()
        except:
            raise forms.ValidationError("Either this collection does not "
                                        "exist or the form was filled out in correctly."
                                        )
