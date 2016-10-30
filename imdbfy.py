import argparse
import requests
import re
from bs4 import BeautifulSoup as bs

f = open('.history.txt','a')

parser = argparse.ArgumentParser()

parser.add_argument("-a", "--actors", help = "Lead actor and Actress",
                    action = "store_true")
parser.add_argument("-d", "--duration", help = "Duration of the movie",
                    action = "store_true")
parser.add_argument("-D", "--director", help = "Director of the movie",
                    action = "store_true")
parser.add_argument("-H", "--history",
                    help = "History of previous searches by the user",
                    action = "store_true")
parser.add_argument("-o", "--overview",
                    help = "Overview (Actor, Ratings, Director, and Summary)",
                    action = "store_true")
parser.add_argument("-P", "--plot", help = "Plot of the movie",
                    action = "store_true")
parser.add_argument("-r", "--ratings", help = "Rating of the movie (out of 10)",
                    action = "store_true")
parser.add_argument("-w", "--nowincinemas", help = "Movies in theatres this week",
                    action = "store_true")
parser.add_argument("-m", "--movie", help = "The name of the movie", default = "")
args = parser.parse_args()

def getUrl():
    f.writelines(args.movie + '\n')
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
        req_url = 'http://www.imdb.com' + what_we_need
        return req_url

def getPage():
    dic = {}
    movie_url = getUrl()
    if movie_url == None:
        return movie_url
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
        dic['Ratings'] = float(new_soup(itemprop="ratingValue")[0].text)
        text = new_soup(property="og:description")[0]['content']
        dic['Director'] = text.split('.')[0].replace('Directed by ','')
        dic['Actors'] = text.split('.')[1].replace('  With ','')
        sum_plot = new_soup(itemprop="description")
        dic['Summary'] = sum_plot[0].text.lstrip().rstrip()
        dic['Plot'] = sum_plot[1].text.lstrip().rstrip()
        dic['Duration'] = new_soup(itemprop="duration")[0].text.lstrip().rstrip()
        return dic

def main():
    if args.nowincinemas:
        movie_req = requests.get('http://www.imdb.com/movies-in-theaters/')
        movie_soup = bs(movie_req.text,'html.parser')
        a = movie_soup(itemprop='image')
        for x in a:
            print x['title']
        return

    if args.history:
        g = open('.history.txt','r')
        print g.read()
        return

    getUrl()
    details = getPage()
    if details == None:
        print "Sorry! No results found!"
        return

    if args.plot:
        print "Plot:"
        print details['Plot']
        return

    if args.overview:
        print "Title:\t\t", details['Title']
        print "Year:\t\t", details['Year']
        print "Actors:\t\t", details['Actors']
        print "Directors:\t", details['Director']
        print "Ratings:\t", details['Ratings']
        print "Summary:\t", details['Summary']
        return

    if args.ratings:
        print "Ratings: ", details['Ratings']

    if args.actors:
        print "Actors: ", details['Actors']

    if args.duration:
        print "Duration: ", details['Duration']

    if args.director:
        print "Directors: ", details['Director']

if __name__ == "__main__":
    main()
    f.close()
