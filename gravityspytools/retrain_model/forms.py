from django import forms
import panoptes_client

from django.utils.translation import gettext_lazy as _

from django import forms
from .models import NewClass

# Create your models here.
class NewClassForm(forms.ModelForm):
    class Meta:
        model = NewClass
        fields = ['collection_owner', 'collection_name',
                  'new_class_name']

        labels = {
            'collection_owner': _("The zooniverse username "
                                  "of the collection owner"),
            'collection_name': _("The display name of the collection as it is "
                                 "in the url. If the collecion url is "
                                 "https://www.zooniverse.org/collections/sbc538/45hz "
                                 "then 45hz would go here"),
            'new_class_name': _("The official new name of the class"),
        }

    def clean(self):
        cleaned_data = super(NewClassForm, self).clean()
        collection_owner = cleaned_data.get('collection_owner')
        collection_name = cleaned_data.get('collection_name')

        tmp = panoptes_client.Collection.where(slug='{0}/{1}'.format(collection_owner, collection_name))
        try:
            tmp.next()
        except:
            raise forms.ValidationError("Either this collection does not "
                                        "exist, is private, or the form was "
                                        "filled out in correctly."
                                        )
