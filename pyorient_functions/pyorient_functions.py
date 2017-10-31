import pyorient


client = pyorient.OrientDB("localhost", 2424)
session_id = client.connect( "root", "America3!" )
client.db_open("hiphopdb", "root", "America3!" )


def clear_relationships():

    tf_delete = "DELETE EDGE track_feature BATCH 10000"
    client.command(tf_delete)
    af_delete = "DELETE EDGE album_feature BATCH 10000"
    client.command(af_delete)
    aa_delete = "DELETE EDGE artist_album BATCH 10000"
    client.command(aa_delete)
    ag_delete = "DELETE EDGE artist_genre BATCH 10000"
    client.command(ag_delete)
    at_delete = "DELETE EDGE artist_track BATCH 10000"
    client.command(at_delete)
    fp_delete = "DELETE EDGE feature_pair BATCH 10000"
    client.command(fp_delete)
    fp_delete = "DELETE EDGE album_track BATCH 10000"
    client.command(fp_delete)


def make_artist(artist):
    ## Make the artist node
    ## Use the Spotify URI as the UID

    dupe_query = "SELECT FROM Artist WHERE uri = '{0}'".format(artist['uri'])
    # print(dupe_query)
    duplicate_check = client.query(dupe_query, 1)
    # print(duplicate_check)
    if len(duplicate_check) < 1:
        # artist_obj = client.command('insert into Artist set name = "{0}", uri = "{1}", popularity = {2}'.format(artist['name'], artist['uri'], artist['popularity']))
        artist_rec = { '@Artist': { 'name': artist['name'].encode('utf-8'), 'uri': str(artist['uri']), 'popularity': artist['popularity'] } }
        artist_obj = client.record_create(21, artist_rec)
        return artist_obj
    else:
        return duplicate_check[0]





def make_album(album):
    ## Make the album node
    ## Use the Spotify URI as the UID
    dupe_query = "SELECT FROM Album WHERE uri = '{0}'".format(album['uri'])
    duplicate_check = client.query(dupe_query, 1)
    if len(duplicate_check) < 1:
        alb_rec = { '@Album': { 'title': str(album['title']), 'uri': str(album['uri'])} }
        alb_obj = client.record_create(29, alb_rec)
        print("Created object for " + album['title'])
        return alb_obj
    else:
        print(album['title'] + " is a duplicate")
        return duplicate_check[0]
    # alb_obj = client.command('insert into Album set title = "{0}", uri = "{1}"'.format(album['title'], album['uri']))





def make_artist_album_edge(artist, album):
    import inspect
    ## Make an edge connecting each Album to it's primary Artist

    # print("Artist Album")
    # artist_rid = ''
    # album_rid = ''
    # print([name for name,thing in inspect.getmembers(artist,[])])
    # for property, value in vars(artist).iteritems():
    #     if property == '_OrientRecord__rid':
    #         artist_rid = value
    # for property, value in vars(album).iteritems():
    #     if property == '_OrientRecord__rid':
    #         album_rid = value
    sql_edge = "create edge artist_album from " + artist._OrientRecord__rid + " to " + album._OrientRecord__rid
    res = client.command( sql_edge )
    print("Created artist album edge")


def make_song(track):
    ## Make the album node
    ## Use the Spotify URI as the UID

    dupe_query = "SELECT FROM Track WHERE uri = '{0}'".format(track['uri'])
    duplicate_check = client.query(dupe_query, 1)
    if len(duplicate_check) < 1:

        track_rec = { '@Track': { 'name': track['name'].encode('utf-8'), 'uri': str(track['uri']), 'track_num': track['track_num'], 'popularity': track['popularity']} }
        track_obj = client.record_create(33, track_rec)

        print("Created song {0}".format(track['name']) )

        return track_obj
    else:
        print("Song {0} is a duplicate".format(track['name']) )
        return duplicate_check[0]

def process_artist_genres(artist):
    genre_list = artist['genres'].split(",")

    genre_objects = []

    for genre in genre_list:

        dupe_query = "SELECT FROM Genre WHERE name = '{0}'".format(genre)
        # print(dupe_query)
        duplicate_check = client.query(dupe_query, 1)
        # print(duplicate_check)
        if len(duplicate_check) < 1:
            # artist_obj = client.command('insert into Artist set name = "{0}", uri = "{1}", popularity = {2}'.format(artist['name'], artist['uri'], artist['popularity']))
            genre_rec = { '@Genre': { 'name': genre } }
            genre_obj = client.record_create(25, genre_rec)
        else:
            genre_obj = duplicate_check[0]
        # print(genre_obj)
        artist_query = "SELECT FROM Artist WHERE uri = '{0}'".format(artist['uri'])
        artist_obj = client.query(artist_query, 1)[0]
        sql_edge = "create edge artist_genre from " + artist_obj._OrientRecord__rid + " to " + genre_obj._OrientRecord__rid
        res = client.command( sql_edge )


    return genre_objects

def make_artist_song_edge(artist, track):
    ## Make an edge connecting each Album to it's primary Artist
    # print("Artist Song")

    dupe_query = "SELECT FROM artist_track WHERE Artist = '{0}' AND Track = '{1}'".format(artist._OrientRecord__rid, track._OrientRecord__rid)
    check_dupe = client.query(dupe_query, 1)
    if not check_dupe:
        sql_edge = "create edge artist_track from " + artist._OrientRecord__rid + " to " + track._OrientRecord__rid
        res = client.command( sql_edge )

        # print("Created edge from artist: {0} to track: {1}".format(artist.OrientRecord__rid, track.OrientRecord__rid) )

def make_album_song_edge(album, track):
    ## Make an edge connecting each Album to it's tracks
    # print("Album Song")
    sql_edge = "create edge album_track from " + album._OrientRecord__rid + " to " + track._OrientRecord__rid
    res = client.command( sql_edge )

    # print("Created edge from album: {0} to song: {1}".format(album.OrientRecord__rid, track.OrientRecord__rid) )

def make_song_feature_edge(track, feature):
    ## Make an edge connecting each track to a featured artist

    sql_edge = "create edge track_feature from " + track._OrientRecord__rid + " to " + feature._OrientRecord__rid
    res = client.command( sql_edge )

    # print("Created edge from track: {0} to feature: {1}".format(track.OrientRecord__rid, feature.OrientRecord__rid) )

def make_feature_pair_edge(artist, track, feature):
    ## Make an edge connecting each album artist to artists featured on their tracks
    # print("A")
    sql_edge = "create edge feature_pair from " + artist._OrientRecord__rid + " to " + feature._OrientRecord__rid
    res = client.command( sql_edge )

    # print("Created feature pair from artist: {0} to feature: {1}".format(artist.OrientRecord__rid, feature.OrientRecord__rid) )

def make_album_feature_edge(album, feature):
    ## Make an edge connecting each album artist to artists featured on their tracks
    sql_edge = "create edge album_feature from " + album._OrientRecord__rid + " to " + feature._OrientRecord__rid
    res = client.command( sql_edge )

    # print("Created edge from album: {0} to feature: {1}".format(album.OrientRecord__rid, feature.OrientRecord__rid) )


def delete_album(album):

    sql_edge = "delete vertex Album where uri = '" + album['uri'] + "'"
    res = client.command( sql_edge )

    print("Deleted album: {0} ".format(album['title']) )


def check_duplicate_track(track):
    dupe_query = 'SELECT FROM Track WHERE name = "' + track['name'].replace("'","''").replace("(Clean)","").replace("(clean)","").replace("(Explicit)","").replace("(explicit)","") + '"'
    duplicate_check = client.query(dupe_query, 1)
    print(duplicate_check)
    if len(duplicate_check) < 1:
        return 0
    else:
        print("Track {0} is a duplicate".format(track['name']))
        return 1

def query_test():
    tf_query = "SELECT expand(outE('album_feature')) FROM Album WHERE title = 'Yeezus'"
    track_features = client.query(tf_query, 5000)
    for f in track_features:
        print(f)
        item = f._OrientRecord__o_storage
        print(item['in'])
        for property, value in vars(f).iteritems():
            print(property, value)

    # artist_query =
    # artist_obj = client.query(artist_query, 1)[0]
    # print(artist_obj)
    # tf_query = "SELECT * FROM track_feature WHERE "