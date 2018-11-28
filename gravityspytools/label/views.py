# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render, redirect
from login.utils import make_authorization_url
from .forms import LabelForm
from .models import Label
from gwpy.table import EventTable
import os

# Create your views here.
convert_string_labels = {'1080Lines': '1080LINE',
        '1400Ripples': '1400RIPPLE',
        'Air_Compressor': 'AIRCOMPRESSOR50HZ',
        'Blip': 'BLIP',
        'Chirp': 'CHIRP',
        'Extremely_Loud':'EXTREMELYLOUD',
        'Helix': 'HELIX',
        'Koi_Fish': 'KOIFISH',
        'Light_Modulation' : 'LIGHTMODULATION',
        'Low_Frequency_Burst' : 'LOWFREQUENCYBURST',
        'Low_Frequency_Lines' : 'LOWFREQUENCYLINE',
        'No_Glitch' : 'NOGLITCH',
        'None_of_the_Above' : 'NONEOFTHEABOVE',
        'Paired_Doves' : 'PAIREDDOVES',
        'Power_Line' : 'POWERLINE60HZ',
        'Repeating_Blips' : 'REPEATINGBLIPS',
        'Scattered_Light' : 'SCATTEREDLIGHT',
        'Scratchy' : 'SCRATCHY',
        'Tomte' : 'TOMTE',
        'Violin_Mode' : 'VIOLINMODEHARMONIC',
        'Wandering_Line' : 'WANDERINGLINE',
        'Whistle' : 'WHISTLE',
}

def index(request):
    if request.user.is_authenticated:
        if request.user.id == 3:
            other_id = 37
        elif request.user.id == 37:
            other_id = 3
        else:
            other_id = -1

        image_to_be_displayed = EventTable.fetch('gravityspy',
                                                 'retired_images_for_testing WHERE \"uniqueID\" NOT IN (SELECT \"uniqueID\" FROM label_label WHERE user_id IN (40, {0}, {1})) ORDER BY RANDOM() LIMIT 1'.format(other_id, request.user.id),
                                                 columns=['imgUrl1', 'imgUrl2', 'imgUrl3', 'imgUrl4', 'uniqueID', 'Label'], db='gravityspytools', passwd=os.getenv('GRAVITYSPYTOOLS_DATABASE_PASSWD'), user=os.getenv('GRAVITYSPYTOOLS_DATABASE_USER'))
        url1=image_to_be_displayed['imgUrl1']
        url2=image_to_be_displayed['imgUrl2']
        url3=image_to_be_displayed['imgUrl3']
        url4=image_to_be_displayed['imgUrl4']
        uniqueID = list(image_to_be_displayed['uniqueID'])[0]
        retired_label = str(list(image_to_be_displayed['Label'])[0])
        retired_label = convert_string_labels[retired_label]

        # Check if this image has already been seen by this user
        try:
            does_exist = Label.objects.get(uniqueID=uniqueID,
                                           user=request.user)
        except:
            does_exist = False

        # if it has redirect them to the page for a fresh image
        # until it is a new label for this user
        if does_exist:
            return redirect('/label/')
        else:
            if request.method == 'POST':
                form = LabelForm(request.POST)
                if form.is_valid():
                    label = str(form.cleaned_data['label'])
                    agreed = str(form.cleaned_data['agreed'])
                    uniqueID = str(form.cleaned_data['uniqueID'])
                    classification, created = Label.objects.get_or_create(label=label,
                                                                 agreed=agreed,
                                                                 uniqueID = uniqueID,
                                                                 user=request.user)
                    classification.save()
                    return redirect('/label/')
            else:
                form = LabelForm(initial={'label': retired_label, 'agreed' : 'AGREE', 'uniqueID' : uniqueID})

        return render(request, 'home.html', {'form': form,
                                             'url1' : list(url1)[0],
                                             'url2' : list(url2)[0],
                                             'url3' : list(url3)[0],
                                             'url4' : list(url4)[0],
                                            })
    else:
        return redirect(make_authorization_url())
