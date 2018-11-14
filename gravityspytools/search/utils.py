from gwpy.table import EventTable
from .forms import SearchForm
from sqlalchemy.engine import create_engine
from math import sqrt
from datetime import datetime, timedelta
from login.utils import get_token_refresh
import pandas as pd
import os, string, random
import panoptes_client


def similarity_search(form):

    # process the data in form.cleaned_data as required
    if form.cleaned_data['imageid']:
        uniqueID = str(form.cleaned_data['imageid'])
    else:
        uniqueID = form.cleaned_data['imageid']
    if form.cleaned_data['zooid']:
        zooID = float(str(form.cleaned_data['zooid']))
    else:
        zooID = form.cleaned_data['zooid']
    if not zooID and not uniqueID:
        gpstime = float(str(form.cleaned_data['gpstime']))
    else:
        gpstime = False

    howmany = int(form.cleaned_data['howmany'])
    database = str(form.cleaned_data['database'])
    ifos = str(form.cleaned_data['ifo'])

    engine = create_engine('postgresql://{0}:{1}@gravityspy.ciera.northwestern.edu:5432/gravityspy'.format(os.environ['GRAVITYSPY_DATABASE_USER'], os.environ['GRAVITYSPY_DATABASE_PASSWD']))
    if zooID:
        PostGresEuclideanDistanceQuery = 'WITH searcharray AS (SELECT cube(array["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "60", "61", "62", "63", "64", "65", "66", "67", "68", "69", "70", "71", "72", "73", "74", "75", "76", "77", "78", "79", "80", "81", "82", "83", "84", "85", "86", "87", "88", "89", "90", "91", "92", "93", "94", "95", "96", "97", "98", "99", "100", "101", "102", "103", "104", "105", "106", "107", "108", "109", "110", "111", "112", "113", "114", "115", "116", "117", "118", "119", "120", "121", "122", "123", "124", "125", "126", "127", "128", "129", "130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "140", "141", "142", "143", "144", "145", "146", "147", "148", "149", "150", "151", "152", "153", "154", "155", "156", "157", "158", "159", "160", "161", "162", "163", "164", "165", "166", "167", "168", "169", "170", "171", "172", "173", "174", "175", "176", "177", "178", "179", "180", "181", "182", "183", "184", "185", "186", "187", "188", "189", "190", "191", "192", "193", "194", "195", "196", "197", "198", "199"]) FROM {2} WHERE "links_subjects" = \'{0}\'), t AS (SELECT "uniqueID", links_subjects, cube(array["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "60", "61", "62", "63", "64", "65", "66", "67", "68", "69", "70", "71", "72", "73", "74", "75", "76", "77", "78", "79", "80", "81", "82", "83", "84", "85", "86", "87", "88", "89", "90", "91", "92", "93", "94", "95", "96", "97", "98", "99", "100", "101", "102", "103", "104", "105", "106", "107", "108", "109", "110", "111", "112", "113", "114", "115", "116", "117", "118", "119", "120", "121", "122", "123", "124", "125", "126", "127", "128", "129", "130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "140", "141", "142", "143", "144", "145", "146", "147", "148", "149", "150", "151", "152", "153", "154", "155", "156", "157", "158", "159", "160", "161", "162", "163", "164", "165", "166", "167", "168", "169", "170", "171", "172", "173", "174", "175", "176", "177", "178", "179", "180", "181", "182", "183", "184", "185", "186", "187", "188", "189", "190", "191", "192", "193", "194", "195", "196", "197", "198", "199"]) FROM {2} WHERE ifo IN ({3})) SELECT "uniqueID", "links_subjects" FROM t order by (SELECT * FROM searcharray) <-> cube asc limit {1};'.format(int(zooID), howmany, database, ifos)
    elif uniqueID:
        PostGresEuclideanDistanceQuery = 'WITH searcharray AS (SELECT cube(array["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "60", "61", "62", "63", "64", "65", "66", "67", "68", "69", "70", "71", "72", "73", "74", "75", "76", "77", "78", "79", "80", "81", "82", "83", "84", "85", "86", "87", "88", "89", "90", "91", "92", "93", "94", "95", "96", "97", "98", "99", "100", "101", "102", "103", "104", "105", "106", "107", "108", "109", "110", "111", "112", "113", "114", "115", "116", "117", "118", "119", "120", "121", "122", "123", "124", "125", "126", "127", "128", "129", "130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "140", "141", "142", "143", "144", "145", "146", "147", "148", "149", "150", "151", "152", "153", "154", "155", "156", "157", "158", "159", "160", "161", "162", "163", "164", "165", "166", "167", "168", "169", "170", "171", "172", "173", "174", "175", "176", "177", "178", "179", "180", "181", "182", "183", "184", "185", "186", "187", "188", "189", "190", "191", "192", "193", "194", "195", "196", "197", "198", "199"]) FROM {2} WHERE "uniqueID" = \'{0}\'), t AS (SELECT "uniqueID", links_subjects, cube(array["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "60", "61", "62", "63", "64", "65", "66", "67", "68", "69", "70", "71", "72", "73", "74", "75", "76", "77", "78", "79", "80", "81", "82", "83", "84", "85", "86", "87", "88", "89", "90", "91", "92", "93", "94", "95", "96", "97", "98", "99", "100", "101", "102", "103", "104", "105", "106", "107", "108", "109", "110", "111", "112", "113", "114", "115", "116", "117", "118", "119", "120", "121", "122", "123", "124", "125", "126", "127", "128", "129", "130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "140", "141", "142", "143", "144", "145", "146", "147", "148", "149", "150", "151", "152", "153", "154", "155", "156", "157", "158", "159", "160", "161", "162", "163", "164", "165", "166", "167", "168", "169", "170", "171", "172", "173", "174", "175", "176", "177", "178", "179", "180", "181", "182", "183", "184", "185", "186", "187", "188", "189", "190", "191", "192", "193", "194", "195", "196", "197", "198", "199"]) FROM {2} WHERE ifo IN ({3})) SELECT "uniqueID", "links_subjects" FROM t order by (SELECT * FROM searcharray) <-> cube asc limit {1};'.format(uniqueID, howmany, database, ifos)
    elif gpstime:
        PostGresEuclideanDistanceQuery = 'WITH searcharray AS (SELECT cube(array["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "60", "61", "62", "63", "64", "65", "66", "67", "68", "69", "70", "71", "72", "73", "74", "75", "76", "77", "78", "79", "80", "81", "82", "83", "84", "85", "86", "87", "88", "89", "90", "91", "92", "93", "94", "95", "96", "97", "98", "99", "100", "101", "102", "103", "104", "105", "106", "107", "108", "109", "110", "111", "112", "113", "114", "115", "116", "117", "118", "119", "120", "121", "122", "123", "124", "125", "126", "127", "128", "129", "130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "140", "141", "142", "143", "144", "145", "146", "147", "148", "149", "150", "151", "152", "153", "154", "155", "156", "157", "158", "159", "160", "161", "162", "163", "164", "165", "166", "167", "168", "169", "170", "171", "172", "173", "174", "175", "176", "177", "178", "179", "180", "181", "182", "183", "184", "185", "186", "187", "188", "189", "190", "191", "192", "193", "194", "195", "196", "197", "198", "199"]) FROM {2} WHERE "peakGPS" = \'{0}\'), t AS (SELECT "uniqueID", links_subjects, cube(array["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "60", "61", "62", "63", "64", "65", "66", "67", "68", "69", "70", "71", "72", "73", "74", "75", "76", "77", "78", "79", "80", "81", "82", "83", "84", "85", "86", "87", "88", "89", "90", "91", "92", "93", "94", "95", "96", "97", "98", "99", "100", "101", "102", "103", "104", "105", "106", "107", "108", "109", "110", "111", "112", "113", "114", "115", "116", "117", "118", "119", "120", "121", "122", "123", "124", "125", "126", "127", "128", "129", "130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "140", "141", "142", "143", "144", "145", "146", "147", "148", "149", "150", "151", "152", "153", "154", "155", "156", "157", "158", "159", "160", "161", "162", "163", "164", "165", "166", "167", "168", "169", "170", "171", "172", "173", "174", "175", "176", "177", "178", "179", "180", "181", "182", "183", "184", "185", "186", "187", "188", "189", "190", "191", "192", "193", "194", "195", "196", "197", "198", "199"]) FROM {2} WHERE ifo IN ({3})) SELECT "uniqueID", "links_subjects" FROM t order by (SELECT * FROM searcharray) <-> cube asc limit {1};'.format(repr(gpstime), howmany, database, ifos)

    # Query Similarity Index to give you the most similar IDs
    SI = pd.read_sql(PostGresEuclideanDistanceQuery, engine)

    glitches = EventTable.fetch('gravityspy', 'glitches WHERE "uniqueID" IN (\'{0}\')'.format(str("','".join(list(SI['uniqueID'])))), columns = ['uniqueID', 'imgUrl1', 'imgUrl2', 'imgUrl3', 'imgUrl4', 'ifo', 'links_subjects', 'snr', 'peak_frequency', 'Label', 'peakGPS', 'Filename1', 'Filename2', 'Filename3', 'Filename4', 'peak_time'])

    # Convert from astropy to pandas for easy manipulation
    SI_glitches = glitches.to_pandas()

    SI_glitches.loc[SI_glitches.imgUrl1 == '?', 'imgUrl1'] = SI_glitches.loc[SI_glitches.imgUrl1 == '?', ['ifo', 'Filename1']].apply(makelink, axis=1)
    SI_glitches.loc[SI_glitches.imgUrl2 == '?', 'imgUrl2'] = SI_glitches.loc[SI_glitches.imgUrl2 == '?', ['ifo', 'Filename2']].apply(makelink, axis=1)
    SI_glitches.loc[SI_glitches.imgUrl3 == '?', 'imgUrl3'] = SI_glitches.loc[SI_glitches.imgUrl3 == '?', ['ifo', 'Filename3']].apply(makelink, axis=1)
    SI_glitches.loc[SI_glitches.imgUrl4 == '?', 'imgUrl4'] = SI_glitches.loc[SI_glitches.imgUrl4 == '?', ['ifo', 'Filename4']].apply(makelink, axis=1)

    if zooID:
        SI_glitches['searchedID'] = SI_glitches.loc[SI_glitches.links_subjects == zooID, 'uniqueID'].iloc[0]
    elif gpstime:
        SI_glitches['searchedID'] = SI_glitches.loc[SI_glitches.peakGPS == gpstime, 'uniqueID'].iloc[0]
    else:
        SI_glitches['searchedID'] = uniqueID


    if uniqueID:
        SI_glitches['searchedzooID'] = SI_glitches.loc[SI_glitches.uniqueID == uniqueID, 'links_subjects'].iloc[0]
    elif gpstime:
        SI_glitches['searchedzooID'] = SI_glitches.loc[SI_glitches.peakGPS == gpstime, 'links_subjects'].iloc[0]
    else:
        SI_glitches['searchedzooID'] = zooID

    return SI_glitches

def create_collection(request, SI_glitches):

    # Verify the links_subjects column before adding them to collection
    SI_glitches = SI_glitches.loc[SI_glitches.links_subjects != 1e20]
    SI_glitches.links_subjects = SI_glitches.links_subjects.apply(int)
    subject_id_requested = int(SI_glitches['searchedzooID'].iloc[0])

    # merge relevantDBs into one DB
    collection_url = 'https://www.zooniverse.org/projects/zooniverse/gravity-spy/collections/'

    request = check_token(request)

    with panoptes_client.Panoptes() as client:
        client.bearer_token = request.session['access_token']
        client.bearer_expires = (
            datetime.now()
            + timedelta(seconds=request.session['expires_in'])
        )
        client.logged_in = True
        
        collection = panoptes_client.Collection()
        collection.links.project = '1104'
        random_hash = id_generator()
        collection.display_name = 'Collection Similar to {0} ID {1}'.format(subject_id_requested, random_hash)
        collection.private = False
        urltmp = collection.save()
        collection_url = collection_url + urltmp['collections'][0]['slug']
        collection.add(SI_glitches.links_subjects.tolist())
        collection.set_default_subject(subject_id_requested)

    return collection_url


def id_generator(size=5, chars=string.ascii_uppercase + string.digits +string.ascii_lowercase):
    return ''.join(random.SystemRandom().choice(chars) for _ in range(size))


def makelink(x):
    # This horrendous thing obtains the public html path for image
    interMediatePath = '/'.join([x for x in str(x.iloc[1]).replace('public_html', '').split('/') if x][1:-1])
    imagename = str(x.iloc[1]).split('/')[-1]
    if x.iloc[0] == 'L1':
        return 'https://ldas-jobs.ligo-la.caltech.edu/~{0}/{1}'.format(interMediatePath, imagename)
    elif x.iloc[0] == 'V1':
        return 'https://ldas-jobs.ligo.caltech.edu/~{0}/{1}'.format(interMediatePath, imagename)
    else:
        return 'https://ldas-jobs.ligo-wa.caltech.edu/~{0}/{1}'.format(interMediatePath, imagename)


def check_token(request):
    if (datetime.now()-datetime(1970,1,1)).total_seconds() > (request.session['token_start_time'] +
                         request.session['expires_in']):
        access_token, expires_in, refresh_token, token_start_time = get_token_refresh(request.session['refresh_token'])
        request.session["access_token"] = access_token
        request.session["expires_in"] = expires_in
        request.session["refresh_token"] = refresh_token
        request.session["token_start_time"] = token_start_time
    return request
