from bs4 import BeautifulSoup
import requests

def get_cover_url(comic):
    url = comic.url.string
    #print "Retrieve picture url from", url
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')
    links = soup.find_all('link')
    imgsrc = None
    for link in links:
        if 'rel' in link.attrs:
            if link['rel'] == ['image_src']:
                imgsrc = link['href']
                break
    if imgsrc is None:
        raise RuntimeError, "No image found for comic %s" % comic.id
    return imgsrc


