import os
import cStringIO as StringIO
import csv

import requests

CATEGORYIDS_URL = 'http://pics.ebay.com/aw/pics/pdf/us/file_exchange/CategoryIDs-US.csv'
CategoryIDFields = ['CategoryID', 'Category Path']

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
    
