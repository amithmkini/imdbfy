import argparse
import requests
import re
from bs4 import BeautifulSoup as bs

parser = argparse.ArgumentParser()

parser.add_argument("-a", "--actors", help = "Lead actor and Actress",
                    action = "store_true")
parser.add_argument("-c", "--cast", help = "Shows the entire cast",
                    action = "store_true")
parser.add_argument("-d", "--duration", help = "Director of the movie",
                    action = "store_true")
parser.add_argument("-H", "--history",
                    help = "History of previous searches by the user",
                    action = "store_true")
parser.add_argument("-o", "--overview",
                    help = "Overview (Actor, Actress, Ratings, Director, and Plot)",
                    action = "store_true")
parser.add_argument("-p", "--poster", help = "Download the poster",
                    action = "store_true")
parser.add_argument("-s", "--summary", help = "Summary of the movie",
                    action = "store_true")
parser.add_argument("-r", "--ratings", help = "Rating of the movie (out of 10)",
                    action = "store_true")
parser.add_argument("-w", "--nowincinemas", help = "Movies in theatres this week",
                    action = "store_true")
parser.add_argument("-m", "--movie", help = "The name of the movie", default = "")
args = parser.parse_args()

def getUrl():
    url_first_part = "http://www.imdb.com/find?ref_=nv_sr_fn&q="
    url_last_part = "&s=all"
    url = url_first_part + args.movie + url_last_part
    req = requests.get(url)
    soup = bs(req.text,'html.parser')

    if 'No results found for' in soup.prettify():
        return None
    else:
        tr = soup.tr
        td = tr.contents
        what_we_need = td[3].a['href']
        req_url = 'www.imdb.com' + what_we_need
        return req_url

def getPage():
    lst = []
    movie_url = getUrl()
    if movie_url == None:
        return url
    else:
        new_req = requests.get(movie_url)
        new_soup = bs(new_req.text,'html.parser')
        tit = new_soup.title.text
        titlis = tit.split()
        titlis.remove('IMDb')
        titlis.remove('-')
        yr = re.findall('\(([0-9]+)\)',tit)
        year = yr[0]
        dic['Year'] = int(yr[0])
        titlis.remove('('+yr[0]+')')
        dic['Title'] = str(' '.join(titlis))
        return dic
