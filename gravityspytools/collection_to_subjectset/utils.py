import panoptes_client


def retrieve_subjects_from_collection(username, collection_display_name):
    tmp = panoptes_client.Collection.where(slug='{0}/{1}'.format(username, collection_display_name)).next()
    collection_display_url = str(tmp.raw['default_subject_src'])
    subjects_in_collection = [int(str(isubject)) for isubject in tmp.raw['links']['subjects']]
    return subjects_in_collection, collection_display_url
