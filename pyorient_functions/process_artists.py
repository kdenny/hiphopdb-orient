from sp_py import get_artist, get_artist_albums, get_album_tracks, get_artist_by_uri

from pyorient_functions import *

from whosampled import getTrackSamples

import csv

artists = []

def process_single_artist(artist_name):
    artist = get_artist(artist_name)

    artist_obj = make_artist(artist)
    artists.append(artist)

    return artist, artist_obj

def process_artists_from_file():

    with open("artists.csv") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            artist_name = row[0]

            artist, artist_obj = process_single_artist(artist_name)

            process_artist_genres(artist)

            process_artist_albums(artist, artist_obj)


def process_artist_albums(artist, artist_obj):

    from pprint import pprint

    artist_albums = get_artist_albums(artist)

    pprint(artist_albums)

    print("Processing albums for {}".format(artist['name']))
    for album in artist_albums:

        album_tracks = get_album_tracks(album, artist['name'])

        print("Got {0} tracks for {1}".format(str(len(album_tracks)), album['title']))

        popular = False
        is_duplicate_album = False
        duplicate_count = 0
        for t in album_tracks:
            # dupe = check_duplicate_track(t)
            # duplicate_count += check_duplicate_track(t)

            if t['popularity'] > 5:
                popular = True


        if duplicate_count >= 6:
            is_duplicate_album = True
            delete_album(album)

        if popular and not is_duplicate_album:
            print("Making " + album['title'] )
            alb_obj = make_album(album)
            make_artist_album_edge(artist_obj, alb_obj)
            print("Making tracks for " + album['title'] )
            for track in album_tracks:

                track_obj = make_song(track)
                make_artist_song_edge(artist_obj, track_obj)
                make_album_song_edge(alb_obj, track_obj)

                # samples = getTrackSamples(artist['name'], track['name'])
                # for sample in samples:
                #     artist, artist_obj = process_single_artist(sample['Artist'])
                #     sample_obj = make_song(track)


                if len(track['features']) > 0:
                    for feat in track['features']:
                        feat_artist = get_artist_by_uri(feat)
                        # if feat_artist not in db:
                        # print(feat_artist)
                        feat_obj = make_artist(feat_artist)
                        if feat_obj:
                            make_song_feature_edge(track_obj, feat_obj)
                            make_album_feature_edge(alb_obj, feat_obj)
                            process_artist_genres(feat_artist)
                            make_feature_pair_edge(artist_obj, track_obj, feat_obj)



clear_relationships()


process_artists_from_file()
#
# query_test()
