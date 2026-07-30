# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render, redirect
from login.utils import make_authorization_url
from .forms import LabelForm
from .models import Label
from gwpy.table import EventTable
from gravityspytools.dbconfig import science_db_host
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


        ids_to_check = ['24LqDBvyeO', 'FPfC0aEI1e', 'gOB9rbtdGz', 'E7EXn4czJc',
        'ht2mTlkZbA', 'fbJRmyH6R9', 'ed7Iakupui', 'GhHiiJ5Ts4',
        'B0vUKA6ZeQ', 'ygPlB11Zj9', 'omkUA8LuaB', 'mzOH0qbFv0',
        'C6MzGQCTGv', 'nMrpPnnfDz', 'XbSNSpviLK', 'Oo8H72QWAw',
        '7HW64D4fA7', '9xvHujvVtv', 'MLPAbmQd4x', 'V4uuSLMNOo',
        'ourXao0cRE', '3wcEpz5s0C', 'NugAGDcjCi', 'G8rXEiBhGT',
        'xgHJnnMwoX', 'XEeXwm5DkX', 'FfnzqtTrHQ', 'sL3UYymoI6',
        'ioqiG8f217', 'UsuiDpfAXH', 'GW3rxN3Wb8', 'r3mVlpgilh',
        '0xZ3R4iHPc', 'NiRjmzXhbr', 's9Enq4PCYN', 'GMm0Rk1iVW',
        'vxo991ufFa', 'JapZ7GlLe1', 'IkAGj8CB6U', 'A1JxVTJmgd',
        'BLNonOtnE2', '6z33RNaEAg', 'G0cM33io47', 'dH5O5YrrB7',
        'yVJLl49BV9', 'lK7yubUvcZ', 'HRrbIQ4zK8', 'c75hgE52dR',
        '2WvkbNdhpk', 'MggOwnseWj', '1vTMMSFxni', 'UDjcIJoLzf',
        '1ttJR9A2WM', 'EyX6uZM6Qo', 'qfM1aQI4wF', '9QfgpKMJww',
        '5cz8tfqJFj', 'vTXvsh5iMw', 'v2TyxmZ6Tc', 'pM48vaDPPi',
        'HNelUx7s8s', 'uJmnet4qL7', '1ZpzvuYcuZ', 'ng3QaYWtAE',
        'aPFZEbUQxL', 'IFKaXPz9KE', 'bFc3GaYnLF', '2dgVGAGIBM',
        'V9ULnrrOe0', 'vx2H5S1yPe', 'n5D5IB0AIE', 'Dj2WUMQD0n',
        'ZzwMjC2szP', 'bd1AyXcxPL', 'tF3c5psnwX', 'j8QMJKIp5Y',
        'HvWuVjAxgQ', 'g28kBCEtFw', 'YlOpXuwBac', 'QI5ZjZmOcM',
        'Eu6dUR7vHj', '7KHfdsqACs', 'UfYh9iDYL0', 'uJke7f6hdB',
        '3mMpVNIajM', 'GWa6UKHqXI', 'CMLEdMlqvn', 'kWWLQls3Vo',
        'DFK4ARnzAr', 'qxS6vWLFuJ', 'rGk6fElzFe', '1jPnk2rJFJ',
        'tfVMddnfqh', 'dwuRCA1nP3', 'AwmcLXV9o1', 'swdy32h0Fp',
        'RRVRl1L0XZ', 'ffvlDTS96q', 'vOvcKYVoZN', 'udPZ3rcL3u',
        'FOM8ykByfa', 'VeQyVYHWSr', 'Hq5usVSTog', 'hvlslveJNJ',
        'ebhyoFqOBd', 'mlFMx9H8Hq', 'tYz5Z39j5K', 'hSbzXErok9',
        'dNa6NpcJfi', 'qjKP3znWK8', 'toBQwU4tLg', 'NzcDOrnnaf',
        '79pWzAonJF', 'DqCrQuxvI7', 'Rh8vMU2ICK', 'VXnnqHoQ5z',
        'r6CPO6ZX9E', 'J3ogagVpeA', 'NVAZ6Xc4eQ', 'Z2KeYGi2lv',
        '86aikgRhYV', 'COfd0ThR8f', 'ez2nWsvmMj', 'JR4i2Q80B9',
        'sCRsuBLRtL', 'sZD4G4nuKo', 'IybF84TuLL', 'V3uTK80wHE',
        'ceOrXQaXcz', 'UVMFIuWlx3', 'gwNPToIyLS', 'gMbu9I3LOZ',
        'T2nqDZKEoC', '4flm14uL1F', 'dHoxYXa8f8', 'Mt43SP8jY6',
        'vXHdiiadBz', '3eGIb1nzjm', 'bksaqq2Azr', 'qYfQSvFjYM',
        'FGouCth8bB', 'FjfUUyGfUj', '3w0Z036EcX', '4A5SeLoXsa',
        'fwt6OxZhwr', 'E1V8ZTkhPc', '0lypuQxnSx', '1WKJvEkLhj',
        'FeiDiLXAd2', 'TahbPXaByj', 'rd6lsMnZxT', 'wWidv1zkIK',
        '3mbVTkeY8t', 'mwoBUhJP22', 'Dl65CXx9SR', 'VTDwKXMgGR',
        '2kuScBFIC7', 'JUzzUDi3pK', 'tCrsuYgcKc', 'a322BNbCzT',
        '9HA6RTlKNJ', 'UKeAnNMnx0', 'vM4BRqjYE8', 'S9ZsGR0sFb',
        '2N5BTzRGqb', 'Q46ODy2Qhd', 'GhWulfsVOX', 'JWhLTKRJVI',
        'BrulPefYNb', 'vYCIyySwRI', 'RLhxT0oVKc', 's97SxynaDo',
        'FPBTXoQSIp', 'grZaLQIEC3', 'GpSDGB7sx7', 'haD99uhXYg',
        'MHyFhsQnfq', 'RyLhg0L79E', '0raPaFgdo3', 'ffnkGCZDho',
        'SWWUfHi2gL', 'uqQPjoe73B', 'TE1GgvxCyQ', 'wfu6OKe2TK',
        '8cFUCHVuZM', 'Udz7brC0vH', 'L53RD6zv8s', '5qE5GmMpzQ',
        '0JLX1Qalcr', 'ZvdxdcTuu8', 'FjRUYnhGwf', 'Vg5m0T9Dwd',
        'HGtGOLIe9N', 'MbAym0YWkj', 'IIraTaWAym', '73UcinUrdM',
        'wi2aRsOjcZ', 'Vc6TgSPi7W', 'CS7WK6sZ9G', 'hgQ6KXu0YX',
        'PoZBeeVbLv', '1lrsvAgDb5', '8GbK5LElwl', 'L8gA0UJsyH',
        'lWOI6FP8IN', 'SShWIgGpUP', 'ChQeL6O5fm', 'bn3hBUMpBy',
        'QucYIs0egf', 'gztfhyRYe1', '4EK4zXBMq8', 'mmhr11qJgm',
        'wka7ATVjjv', '85F3NNUetR', 's8qlH0kENz', 'djxvGB8t77',
        '3RkJTmMBKA', 'N2XG4eLTJ2', 'PcNJEKI7iv', 'i9mlPdB6Cs',
        '3mnm83WK90', 'jCH5gA8yzd', 'DpgXKx15xh', 'lXyk5P02hq',
        'Ug53Bkh4uP', 'fFWqp430xE', 'rlvvq8yBm5', '8BFKEpHn75',
        '2v11UIeNMg', 'azG5vMWetW', '6ekuvywynp', 'mdKBcJFU2w',
        '6uGfTqfqJr', 'vOEsWxqHQc', 'eqxGuGFW0H', 'Mets1F9pid',
        'SlcR4Kox89', 'bOySVR9FkK', '2KFwG4JpG8', 'pCr3PRY0FA',
        'bHzbF2kQ1D', 'CKW4Zj6ogx', 'qmFPR1Dtgf', 'ihjdurfJ2N',
        '5aTGtCaoy6', 'jwGx0stCkm', 'teFrW6g6Ny', 'vktNWsr5Hc',
        '4OV0zGlj0k', 'QHJtCbpfY9', '0XcdU6Nuwo', '9HQcpxoigy',
        'boVUFo2Slz', 'aaP75v7SQd', 'gstFESOkaA', '2W4O2ldxD4',
        'KSTSBuAQpg', 'EubpTgLz0f', 'dQmXkypH32', 'nZEREXT9fw',
        'cVNdZTzhZM', 'LAyFhiUGLA', 'OeachqqctF', 'aCfCRfGtFi',
        'kWWYk11iWH', 'RpSgHH75ya', 'yAipnrUEC5', 'oLiWdBcjhF',
        'Lm5EEzFOJg', 'cVtWAPZilr', 'JYJYVpXrcp', 'zXbj1vw8Gz',
        'NQO5X5y00G', 'kGxMDOlJxI', 'Oqw2w0LWlJ', 'HxVS3GgJ1l',
        'iQQa9Ec0w2', '4iXZPuf4aT', '4AukA557A8', 'ydpcb7aoW6',
        'HF9DGKDLNT', 'tAf2sdYEpE', 'FkpSiy3R4L', 'yjn5S3L0fB',
        '40O9AXpxk1', '9ib12ZkTqJ', 'UjRkapuEMI', 'NMZ6f9pjyU',
        '6dGg3KJAMm', 'pEvzvt4QFI', 'shHpmunyzc', 'llq6zGDGts',
        'w3iet9urDv', '0zBs6v1LBa', 'hlYc1VTigx', '25AT71LU66',
        'lb3oKSg38L', '5qE13eMX4c', 'sUZVsbkrHv', 'NI61EdmmG9',
        '1zlViqIfDH', 'cwOnXzZWIq', 'WunYCeoX5P', '9VLUY20XG9',
        'hvNa72SLpc', 'YmKJuMS57p', 'goGMGffpg4', 'jB91DqTvvT',
        'lPUy2rZ4Hq', '6OzsaQzKJe', 'i5HNUM7xv1', '1wWe8Q7LoE',
        'EC0SuSqQJo', 'SIYMlLCzEb', '1602K0Arm1', 'oCVcRbEfIU',
        'eYJMhPZ6ww', '9AaQ0zXLSV', 'nBvu21v0my', 'PLxP8MGSnE',
        'Ohi4wf4ZHk', '5tXNrAgZIi', 'sV50bCrC7q', 'lbXsF2tumy',
        'aX0cFhkwJG', '3sIPavgkYc', 'Tyu5xOcXDL', 'ZFiYJgKzJU',
        'QPSJHooNse', 'TpjEwRJa4J', 'N0MLnm1Uml', 'StVUrKaqdc',
        'UXxnfcjgyp', '2FImcfpre6', '758tpN2KPJ', 'udd7JcQfwr',
        'MJliehv4mj', 'WbAdabwn6p', 'xVwXvMMNxA', 'VsgCdtpXTS',
        'bIrhlu0jYi', '6gEPYMu07m', 'LLCChad1yo', 'HZ7CeBhTSN',
        'Qw5snyksxH', 'oFe7Giw7PU', '9cJ4Emxnfs', '3M8dXrJ67g',
        'Nhf9pRRk5c', 'idfTlZK5d8', 'LJ3F6NZb4J', 'YUBcPu8Awk',
        'PS9DpAwoS7', '1DuTI2DS2L', 'sdXJHTkvuy', 'aRaUJZGdYT',
        'TNCPBWLN4W', 'Dohnpd782Q', '6YX3Jyg0d5', 'FXE0FMdKX6',
        '24vfrTP9O8', 'eG4BfWP3vi', 'uhibaWCUBo', 'Wpds9Z4Rjx',
        'GyuVinuRoA', 'ZrNF9vU4dc', 'wL4q8d3bNW', 'XDfA7tR07d',
        'v0QfaJ232F', 'oTHkfimm5D', 'HRrPEYnf4H', 'wQIORmwR5j',
        'a7KzJQ2ioZ', '233aRpMuKu', 'Z5zWgTtgIG', 'gKqESgTYEu',
        'qlQIXRnhyb', '9raaHNyfVY', 'f3rQJr8JrE', 'IP9gJEP5DJ',
        'uSs2GyAvdQ', 'nRGdshSZLw', 'lcFPn3duuH', 'iHLFyZGfNI',
        'd1HNOIwSuv', 'FhzvNj9HS7', '7u8MefKKbE', 'eWLW5RlmuI',
        'LKfAjsNnq9', 'Pwcg4lBqfe', 'yPFsxWo1jv', 'TTZmIN20mp',
        'lrlm0XOT61', 'uOKbnV9I3D', 'Ctm7QUkZOu', 'RdZ1nZMgMF',
        'dPpeOIn4m4', 'MAaDiuywgi', 'cP3TaakVVe', 'gom4cpinzc',
        'gj4ZFQHXmT', '6mLJy2Sxjy', 'jGPjmToBKg', '0ZRiH8sk3N',
        'we4EzfIlQI', 'PfI1t2F6Te', 'do7j3GpN3n', 'sgdOdnFnoj',
        'y0SHMolbrH', 'Y0dTPgQZq1', 'sUaJ53zKRc', 'eJPlEduIh0',
        'IPTQIDXYsK', 'xOcBSMPjmt', 'uGbSfu8HcP', 'MF5xeyBuol',
        'KxAumSbn2r', 'LQW4aHOPYI', 'XBuPnhh6VA', '8a152s09My',
        'a0VjphzIbu', 'Ut7HTwAuSN', 'xyluP97LJG', 'DqargGU98b',
        'vul2xQHJqW', 'r3MGMjwxsT', 'u6L2cuqJ9L', 'BG9Jpa8Qo3',
        'X1WLFeSI9n', 'tNNweTY7m5', '5rcohOjCMw', 'wBYIgpVKAl',
        'xfNpt7GVmN', 'CFz1J7FAbf', 'lIyWmuHcAD', '04HxFGxsmh',
        'B97vo37WLo', 'crC42tvxi8', '4teMqbpudF', 'ZDuaCHPmhJ',
        'vwJlk28UG0', 'eRAqnsSfJS', 'kL1vNsgi7L', '3gzArMA8Hc',
        'Tgut9O4Anw', 'yzXg9hMTVA', 'O16McFLqVF', 'OTOlc2YO4Y',
        'yy9cyk2kQp', '0xBFj7Carm', 'P2zKXpSi0O', 'KS34YnEy1o',
        'WEXV0REVzX', '91tMwwCo4V', 'g05ekNMp2y', 'G7V3tZpXUo',
        'jq1JJIMTIt', 'foBgXHgxNB', 'GNLqR363Ps', 'Sz7LDjLsrX']


        image_to_be_displayed = EventTable.fetch('gravityspy',
                                                  'extra_image_for_testing WHERE gravityspy_id IN (\'{1}\') AND gravityspy_id NOT IN (SELECT gravityspy_id FROM label_label WHERE user_id = {0}) ORDER BY RANDOM() LIMIT 1'.format(request.user.id, str("','".join(ids_to_check))),
                                                  columns=['url1', 'url2', 'url3', 'url4', 'gravityspy_id', 'ml_label'], db='gravityspytools', passwd=os.getenv('GRAVITYSPYTOOLS_DATABASE_PASSWD'), user=os.getenv('GRAVITYSPYTOOLS_DATABASE_USER'), host=science_db_host())

        url1=image_to_be_displayed['url1']
        url2=image_to_be_displayed['url2']
        url3=image_to_be_displayed['url3']
        url4=image_to_be_displayed['url4']
        gravityspy_id = list(image_to_be_displayed['gravityspy_id'])[0]
        retired_label = str(list(image_to_be_displayed['ml_label'])[0])
        retired_label = convert_string_labels[retired_label]

        # Check if this image has already been seen by this user
        try:
            does_exist = Label.objects.get(gravityspy_id=gravityspy_id,
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
                    gravityspy_id = str(form.cleaned_data['gravityspy_id'])
                    classification, created = Label.objects.get_or_create(label=label,
                                                                 agreed=agreed,
                                                                 gravityspy_id = gravityspy_id,
                                                                 user=request.user)
                    classification.save()
                    return redirect('/label/')
            else:
                form = LabelForm(initial={'label': retired_label, 'agreed' : 'AGREE', 'gravityspy_id' : gravityspy_id})

        return render(request, 'home.html', {'form': form,
                                             'url1' : list(url1)[0],
                                             'url2' : list(url2)[0],
                                             'url3' : list(url3)[0],
                                             'url4' : list(url4)[0],
                                            })
    else:
        return redirect(make_authorization_url())
