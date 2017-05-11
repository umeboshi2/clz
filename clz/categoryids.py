import os
import cStringIO as StringIO
import csv

import requests

CATEGORYIDS_URL = 'http://pics.ebay.com/aw/pics/pdf/us/file_exchange/CategoryIDs-US.csv'
CategoryIDFields = ['CategoryID', 'Category Path']
CAT_PREFIX = 'Collectibles > Comics'

def download_url(url):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    f = StringIO.StringIO()
    for chunk in r.iter_content(chunk_size=1024): 
        if chunk: # filter out keep-alive new chunks
            f.write(chunk)
            #f.flush() commented by recommendation from J.F.Sebastian
    f.seek(0)
    return f

def get_main_file():
    filename = os.path.basename(CATEGORYIDS_URL)
    if os.path.isfile(filename):
        return file(filename)
    else:
        print "Downloading", CATEGORYIDS_URL
        strio = download_url(CATEGORYIDS_URL)
        with file(filename, 'w') as outfile:
            strio.seek(0)
            outfile.write(strio.read())
        return file(filename)
    

def get_categories(prefix):
    mfile = get_main_file()
    reader = csv.reader(mfile)
    catlist = list()
    for cid, cpath in reader:
        if cpath.startswith(prefix):
            catlist.append((cid, cpath))
    return catlist

    
def make_csv(filename, prefix):
    catlist = get_categories(prefix)
    fieldnames = CategoryIDFields
    with file(filename, 'w') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for cid, cpath in catlist:
            writer.writerow(dict(zip(fieldnames, [cid, cpath])))
    




# superhero stuff
def get_superhero_categories(config):
    catlist = get_categories(CAT_PREFIX)
    cdata = {}
    table = []
    ages = config.options('comic_ages')
    # no individual platinum/golden age superheroes
    oldages = ['platinum', 'golden']
    ages = [a for a in ages if a not in oldages]
    superheroes = dict()
    for cid, cpath in catlist:
        clist = [x.strip() for x in cpath.split(' > ')]
        clist = clist[2:]
        cdata[cid] = clist
        age = clist[0].split()[0].lower()
        if age in ages:
            #print "AGE", age, clist
            hero = clist[1]
            if hero == 'Superhero':
                #print "%s age superhero %s" % (age, clist[2])
                table.append((cid, age, clist[2]))
        elif age in oldages:
            if age == 'platinum':
                table.append((cid, age, clist[0]))
            elif age == 'golden' and clist[1] == 'Superhero':
                table.append((cid, age, clist[1]))
    return table

def make_superhero_table(config):
    table = get_superhero_categories(config)
    rows = []
    for cid, age, hero in table:
        years = config.get('comic_ages', age)
        start, end = [int(x.strip()) for x in years.split(',')]
        rows.append((cid, age, start, end, hero))
    return rows
    
        
        
            
