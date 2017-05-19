from bs4 import BeautifulSoup
import requests
import transaction
from sqlalchemy.orm.exc import NoResultFound

from .database import ComicCoverImage

def get_cover_url(url):
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
        raise RuntimeError, "No image found for comic %s" % url
    return imgsrc


class CoverUrlManager(object):
    def __init__(self, session):
        self.session = session
        
    def set_session(self, session):
        self.session = session
        
    def select_cover_image_by_url(self, url):
        q = self.session.query(ComicCoverImage)
        q = q.filter_by(url=url)
        return q.one()

    def insert_cover_image(self, url):
        print "insert_cover_image", url
        imgsrc = get_cover_url(url)
        with transaction.manager:
            ci = ComicCoverImage()
            ci.url = unicode(url)
            ci.imgsrc = unicode(imgsrc)
            self.session.add(ci)
        self.session.commit()
        return self.session.merge(ci)
    

    def get_cover_image(self, comic):
        url = comic.url.string
        try:
            ci = self.select_cover_image_by_url(url)
        except NoResultFound:
            ci = self.insert_cover_image(url)
        return ci
    

