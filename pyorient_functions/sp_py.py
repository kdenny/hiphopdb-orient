
import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pprint import pprint
import csv

client_credentials_manager = SpotifyClientCredentials(client_id='7568b9fd0cbb44958ba19d038ff51d05', client_secret='453d007f79704d27a4b8befcf6a02602')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)



def get_artist(name):
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        artist = items[0]
        this_data = {
            'name': name,
            'uri': artist['uri'],
            'popularity': artist['popularity']
        }
        genre_join = ''
        for g in artist['genres']:
            genre_join += "{0},".format(g)
        this_data['genres'] = genre_join[:-1]
        return this_data
    else:
        return None

def get_artist_by_uri(artist):
    artist_new = sp.artist(artist['uri'])

    this_data = {
        'name': artist['name'],
        'uri': artist['uri'],
        'popularity': artist_new['popularity']
    }
    genre_join = ''
    for g in artist_new['genres']:
        genre_join += "{0},".format(g)
    this_data['genres'] = genre_join[:-1]

    return this_data


def get_artist_albums(artist):
    artist_albums = []
    results = sp.artist_albums(artist['uri'], album_type='album')
    albums = results['items']
    while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])
    used_albums = []
    for a in albums:
        if ('edited' not in str(a['name'])) and ('Edited' not in str(a['name'])) and ('Exclusive Edition' not in str(a['name'])) \
                and ('UK Version' not in str(a['name'])) and ('Softpak' not in str(a['name'])) and 'US' in a['available_markets']:
            album = {
                'uri': a['uri'],
                'title': str(a['name'])
            }
            if len(a['artists']) > 1:
                album['other_artist'] = a['artists'][1]['name']
            else:
                album['other_artist'] = ''

            if album['title'] not in used_albums:
                artist_albums.append(album)
                used_albums.append(album['title'])

    return artist_albums

def get_album_tracks(album, artist_name):
    album_tracks = []
    results = sp.album_tracks(album['uri'])
    tlist = results['items']

    for tl in tlist:
        track = {
            'name': tl['name'].replace('"',"'").replace("'","''").replace("(Clean)","").replace("(clean)","").replace("(Explicit)","").replace("(explicit)",""),
            'uri': tl['uri'],
            'track_num': tl['track_number'],
            'features': []
        }

        ### Process features here

        if len(tl['artists']) > 1:
            for feat in tl['artists']:
                if feat['name'] != artist_name:
                    feat_obj = {
                        'name': feat['name'],
                        'uri': feat['uri']
                    }
                    track['features'].append(feat_obj)
        extra_data = sp.track(track['uri'])
        track['popularity'] = extra_data['popularity']
        album_tracks.append(track)
        # pprint(extra_data)

    return album_tracks
    # pprint(album_tracks)




artists = []
artist_albums = {}



# test_alb = {
#     'uri': 'spotify:album:31SGkM7Y8ZnXL823nDVHNG'
# }
#
# get_album_tracks(test_alb, 'Kanye West')

