import os, sys
from optparse import OptionParser

from clz.config import config
from clz.xmlparse import get_comics
from clz.desc import make_description
from clz.categoryids import make_csv
from clz.ebinfo import makeEbayInfo, EbayFields

CATEGORYFILE = 'comic-categories.csv'
if not os.path.isfile(CATEGORYFILE):
    prefix = 'Collectibles > Comics'
    make_csv(CATEGORYFILE, prefix)
    print "Created category file for", prefix
    
# fields are EbayFields and comics are bs4 elements
import cStringIO as StringIO
import csv
def make_ebay_csv(fields, comics, config):
    reqfields = ['*%s' % o.capitalize() for o in config.options('reqfields')]
    fields = reqfields + [f for f in fields if f not in reqfields]
    ofile = StringIO.StringIO()
    writer = csv.DictWriter(ofile, fields)
    writer.writeheader()
    for comic in comics:
        ebinfo = makeEbayInfo(config, comic)
        cdata = dict([(k,v) for k,v in ebinfo.items() if k in fields])
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

opts, args = parser.parse_args(sys.argv[1:])
if not len(args):
    raise RuntimeError, "Need to pass an xml file as an argument."
config.read([opts.config])

xmlfile = args[0]

def main():
    print "Getting comics"
    comics = get_comics(xmlfile)
    print "Created comic list."
    c = comics[0]

    print "creating csv data"
    cc = make_ebay_csv(EbayFields, comics, config)

    if opts.output is None:
        sys.stdout.write(cc.read())
    else:
        filename = opts.output
        print "Writing", filename
        write_csvfile(filename, cc)
    
if __name__ == "__main__":
    main()
    
