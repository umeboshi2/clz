import os, sys
from optparse import OptionParser
import cStringIO as StringIO
import csv

from clz.config import config
from clz.xmlparse import get_comics
from clz.desc import make_description
from clz.categoryids import make_csv, get_categories
from clz.categoryids import make_superhero_table
from clz.ebinfo import makeEbayInfo, EbayFields

CATEGORYFILE = 'comic-categories.csv'
CAT_PREFIX = 'Collectibles > Comics'

if not os.path.isfile(CATEGORYFILE):
    make_csv(CATEGORYFILE, CAT_PREFIX)
    sys.stderr.write("Created category file for %s.\n" % CAT_PREFIX)


def make_superhero_csv(rows):
    fieldnames = ['CategoryID', 'Age', 'Start', 'End', 'Superhero']
    ofile = StringIO.StringIO()
    writer = csv.DictWriter(ofile, fieldnames)
    writer.writeheader()
    for row in rows:
        d = dict(zip(fieldnames, row))
        writer.writerow(d)
    ofile.seek(0)
    return ofile
    
def make_comic_category_map():
    rows = make_superhero_table(config)
    csvdata = make_superhero_csv(rows)
    #print csvdata.read()
    if opts.output is None:
        sys.stdout.write(csvdata.read())
    else:
        filename = opts.output
        sys.stderr.write("Writing %s\n" % filename)
        write_csvfile(filename, csvdata)
        
        
    
# fields are EbayFields and comics are bs4 elements
def make_ebay_csv(fields, comics, config):
    ropts = config.options('reqfields')
    if 'category' not in ropts:
        ropts.append('category')
    ropts.sort()
    if ropts[0] != 'action':
        raise RuntimeError, "No action found in config!"
    reqfields = ['*%s' % o.capitalize() for o in ropts]
    optfields = config.options('optfields')
    fields = reqfields + optfields + [f for f in fields if f not in reqfields]
    ofile = StringIO.StringIO()
    writer = csv.DictWriter(ofile, fields)
    writer.writeheader()
    for comic in comics:
        ebinfo = makeEbayInfo(config, comic, opts)
        cdata = dict([(k,unicode(v).encode('utf-8')) for k,v in ebinfo.items() if k in fields])
        writer.writerow(cdata)
    ofile.seek(0)
    return ofile


def write_csvfile(filename, strio):
    with file(filename, 'w') as outfile:
        outfile.write(strio.read())

parser = OptionParser()
parser.add_option('-u', '--url-prefix', action='store', dest='urlprefix',
                  default='http://replace.me/with/the/url')
parser.add_option('-o', '--output', action='store', dest='output',
                  default=None)
parser.add_option('-c', '--config', action='store', dest='config',
                  default='config.ini')
parser.add_option('--category', action='store', dest='category',
                  default=None)
#parser.add_option('-a', '--action', action='store', dest='action',
#                  default='VerifyAdd')

opts, args = parser.parse_args(sys.argv[1:])
config.read([opts.config])


def show_csv(text):
    import Tkinter
    root = Tkinter.Tk()
    s = Tkinter.Scrollbar(root)
    t = Tkinter.Text(root, height=34, width=250)
    s.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)
    t.pack(side=Tkinter.LEFT, fill=Tkinter.Y)
    s.config(command=t.yview)
    t.config(yscrollcommand=s.set)
    t.insert(Tkinter.END, text)
    Tkinter.mainloop()
    
def main():
    if not len(args):
        raise RuntimeError, "Need to pass an xml file as an argument."
    xmlfile = args[0]
    sys.stderr.write('Getting comics.\n')
    comics = get_comics(xmlfile)
    sys.stderr.write("Created comic list.\n")
    c = comics[0]

    sys.stderr.write("creating csv data...\n")
    cc = make_ebay_csv(EbayFields, comics, config)

    if opts.output is None:
        #sys.stdout.write(cc.read())
        show_csv(cc.read())
    else:
        filename = opts.output
        sys.stderr.write("Writing %s\n" % filename)
        write_csvfile(filename, cc)
    
if __name__ == "__main__":
    main()
    
