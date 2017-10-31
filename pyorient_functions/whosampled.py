from bs4 import BeautifulSoup
from slugify import slugify
from pprint import pprint
import unicodedata

import requests

def match_class(target):
    def do_match(tag):
        classes = tag.get('class', [])
        return all(c in classes for c in target)
    return do_match

def getTrackSamples(artist, track):

    track_samples = []
    headers = requests.utils.default_headers()
    headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    })

    artist = slugify(artist)
    track = slugify(track)

    r = requests.get('https://www.whosampled.com/{0}/{1}/'.format(artist, track), headers=headers)

    print(r.status_code)

    if r.status_code == 200:

        data = r.text
        #
        # print(data)

        soup = BeautifulSoup(data)

        count = 0
        track_start = -1

        for section in soup.find_all('section'):
            sample_section = False
            section_name = section.find_all(match_class(["section-header-title"]))
            if section_name:
                txt = section_name[0].contents[0]
                if len(txt.split(" ")) > 0:
                    contents = txt.split(" ")
                    if (contents[0] == 'Contains') and (contents[1] == 'samples') and (contents[2] == 'of'):
                        print("Looks like")
                        # print(section)
                        sample_section = True

            if sample_section:
                for link in section.find_all(match_class(["trackDetails"])):
                    track_sample = {}

                    # print(link)

                    track_t = link.find(match_class(["trackName"])).contents[0]

                    track_sample['Artist'] = str(link.find(match_class(["trackArtist"])).find('a').contents[0])
                    track_sample['Track'] = unicodedata.normalize('NFKD', track_t).encode('ascii','ignore')
                    track_sample['track_link'] = link.find(match_class(["trackName"])).get('href')
                    track_sample['artist_link'] = link.find(match_class(["trackArtist"])).find('a').get('href')

                    track_samples.append(track_sample)

    return track_samples


        # for link in soup.find_all(match_class("feeditemcontent cxfeeditemcontent")):
        #     count += 1
        #
        #     link_comps = link_text.split("/")
        #     print(link.get('href'))

# ts = getTrackSamples('Kanye West','Blood on the leaves')
# pprint(ts)