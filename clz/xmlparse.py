from bs4 import BeautifulSoup

def parse_xmlfile(filename):
    return BeautifulSoup(file(filename), 'lxml')

def getChildElements(element):
    return [t for t in element.children if t.name is not None]

def get_comics(filename):
    s = parse_xmlfile(filename)
    return getChildElements(s.comiclist)
