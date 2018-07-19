# -*- coding: utf-8 -*-
#from __future__ import unicode_literals

from django.shortcuts import render, redirect

from login.utils import make_authorization_url
from collection_to_subjectset.forms import SearchForm
from collection_to_subjectset.utils import retrieve_subjects_from_collection
from gwpy.table import EventTable

import matplotlib.pyplot as plt
import datetime
import timeconvert

# Create your views here.

def index(request):
    if request.user.is_authenticated():
        form = SearchForm()
        return render(request, 'collectioninfo.html', {'form': form})
    else:
        return redirect(make_authorization_url())


def collectioninfo(request):
    # if this is a POST request we need to process the form data
    if request.method == 'GET':

        # create a form instance and populate it with data from the request:
        form = SearchForm(request.GET)
        # check whether it's valid:
        if form.is_valid():
            username = str(form.cleaned_data['username'])
            collection_display_name = str(form.cleaned_data['collection_display_name'])

            subjects_in_collection = retrieve_subjects_from_collection(username, collection_display_name)
            subjects_in_collection = [str(isubject) for isubject in subjects_in_collection]
            SI_glitches = EventTable.fetch('gravityspy', 'glitches WHERE CAST(links_subjects AS FLOAT) IN ({0})'.format(str(",".join(subjects_in_collection)))).to_pandas() 
            
                GlitchValues = SI_glitches.values
                GlitchGPS = (GlitchValues[:,4]).tolist()
                newestGPS = (max(GlitchGPS))
                oldestGPS = (min(GlitchGPS))
                print (newestGPS)
                print (oldestGPS)

                #converting newest and oldest to dates
                newest = timeconvert.gps2ppl(newestGPS)
                oldest = timeconvert.gps2ppl(oldestGPS)
                print (newest)
                print (oldest)

                #number of weeks
                def nofweeks(d1,d2):
                    d1 = datetime.datetime.strptime(d1, "%Y-%m-%d %H:%M")
                    d2 = datetime.datetime.strptime(d2, "%Y-%m-%d %H:%M")
                    hop = ((abs((d2 - d1).days))/7)
                    if hop > 1:
                        return hop
                    elif hop <= 1:
                        return 1
                print (nofweeks(newest, oldest))

                #checking and changing xlocs, xlabels
                plt.hist(GlitchGPS, bins = (nofweeks(newest, oldest)))
                xlocs, xlabels = plt.xticks()
                print (xlocs)
    
                GPSlabels = list()
                for x in range(len(xlocs)):
                    GPSlabels.append(timeconvert.gps2ppl(xlocs[x]))
                plt.xticks(xlocs, GPSlabels, rotation = 45)
                plt.title("Distribution of Glitches \n Each Bin Represents One Week")
                plt.xlabel("Time")
                plt.ylabel("Number of Glitches per Week")
                plt.tight_layout()
                plt.hist(GlitchGPS, bins = (nofweeks(newest, oldest)))
                xlocs, xlabels = plt.xticks()
                print (xlocs)

                plt.savefig("final.png")
            
            return render(request, 'searchresults.html', {'results': SI_glitches.to_dict(orient='records')})
