# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Label(models.Model):
    TENEIGHTYLINE = '1080LINE'
    FOURTEENHUNDREDRIPPLE = '1400RIPPLE'
    AIRCOMPRESSOR50HZ = 'AIRCOMPRESSOR50HZ'
    BLIP = 'BLIP'
    CHIRP = 'CHIRP'
    EXTREMELYLOUD = 'EXTREMELYLOUD'
    HELIX = 'HELIX'
    KOIFISH = 'KOIFISH'
    LIGHTMODULATION = 'LIGHTMODULATION'
    LOWFREQUENCYBURST = 'LOWFREQUENCYBURST'
    LOWFREQUENCYLINE = 'LOWFREQUENCYLINE'
    NOGLITCH = 'NOGLITCH'
    NONEOFTHEABOVE = 'NONEOFTHEABOVE'
    PAIREDDOVES = 'PAIREDDOVES'
    POWERLINE60HZ = 'POWERLINE60HZ'
    REPEATINGBLIPS = 'REPEATINGBLIPS'
    SCATTEREDLIGHT = 'SCATTEREDLIGHT'
    SCRATCHY = 'SCRATCHY'
    TOMTE = 'TOMTE'
    VIOLINMODEHARMONIC = 'VIOLINMODEHARMONIC'
    WANDERINGLINE = 'WANDERINGLINE'
    WHISTLE = 'WHISTLE'

    LABEL_CHOICES = (
        (TENEIGHTYLINE, '1080 Line'),
        (FOURTEENHUNDREDRIPPLE, '1400 Ripple'),
        (AIRCOMPRESSOR50HZ, 'Air Compressor 50Hz'),
        (BLIP, 'Blip'),
        (CHIRP, 'Chirp'),
        (EXTREMELYLOUD, 'Extremely Loud'),
        (HELIX, 'Helix'),
        (KOIFISH, 'Koi Fish'),
        (LIGHTMODULATION, 'Light Modulation'),
        (LOWFREQUENCYBURST, 'Low Frequency Burst'),
        (LOWFREQUENCYLINE, 'Low Frequency Line'),
        (NOGLITCH, 'No Glitch'),
        (NONEOFTHEABOVE, 'None of the Above'),
        (PAIREDDOVES, 'Paired Doves'),
        (POWERLINE60HZ, 'Power Line 60Hz'),
        (REPEATINGBLIPS, 'Repeating  Blips'),
        (SCATTEREDLIGHT, 'Scattered Light'),
        (SCRATCHY, 'Scratchy'),
        (TOMTE, 'Tomte'),
        (VIOLINMODEHARMONIC, 'Violin Mode Harmonic'),
        (WANDERINGLINE, 'Wandering Line'),
        (WHISTLE, 'Whistle'),
    )

    AGREE = 'AGREE'
    DISAGREE = 'DISAGREE'

    AGREEMENT_CHOICES = (
        (AGREE, 'Agree'),
        (DISAGREE, 'Disagree'),
    )

    label = models.CharField(max_length=30, choices=LABEL_CHOICES,)
    uniqueID = models.CharField(max_length=10)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING,)
    agreed = models.CharField(max_length=8, choices=AGREEMENT_CHOICES,)
