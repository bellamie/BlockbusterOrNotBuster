import sys
import requests
import re
#from bs4 import BeautifulSoup

def scrape(id):
    rawHTML = requests.get("http://www.imdb.com/title/" + id).content
    movie = {}
    #find discription
    m = re.search('<h2>Storyline</h2>(.|\n)*?<p>((.|\n)*?)<em', rawHTML)
    if(not m == None):
        #soup = BeautifulSoup(m.group(2), 'html.parser')
        movie['description'] = m.group(2)
    #find rating
    m = re.search('<strong title="([0-9]\.[0-9]) based on', rawHTML)
    if(not m == None):
        movie['rating'] = float(m.group(1))

    return movie

if __name__ == "__main__":
    outputFile = open('movies.csv','w')

    collected = 0
    failed = 0
    start = 400500
    end =   401000
    for i in range(start,end):
        movie = scrape('tt0' + str(i))
        if('description' in movie.keys() and 'rating' in movie.keys()):
            outputFile.write(str(movie['rating']) + "~" + movie['description'].replace('\n','').replace('\r','') + '\r\n')
            outputFile.flush()
            collected += 1
        else:
            failed += 1
        if(i%100 == 0):
            print("scraped: " + str(i - start) + " collected: " + str(collected) + " rejected: " + str(failed))
    outputFile.close()


