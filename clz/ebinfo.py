from .base import make_picture_url
from .desc import make_description

EbayFields = ['Category','Title', 'Subtitle', 'PicURL',
              'Description', 'Quantity', 'Product:Brand',
              'Duration', 'PostalCode',
              'Product:UPC',
              'Product:ISBN',
]

def makeCommonData(config):
    CommonData = dict()
    # we will use PostalCode for location
    rlocation = False
    need_rlocation = True
    for field, value in config.items('reqfields'):
        rfield = '*%s' % field.capitalize()
        CommonData[rfield] = value
        if field.lower() == 'location':
            rlocation = True
            need_rlocation = False
    if not rlocation:
        optfields = [o.lower() for o in config.options('optfields')]
        if 'postalcode' not in optfields:
            raise RuntimeError, "need postal code if not using location"
        code = config.get('optfields', 'postalcode')
        CommonData['PostalCode'] = code
        need_rlocation = False
    if need_rlocation and not rlocation:
        raise RuntimeError, "another problem"
    return CommonData

def makeEbayInfo(config, comic):
    data = makeCommonData(config)
    Title = comic.series.displayname.string
    Subtitle = comic.fulltitle.string
    urlprefix = config.get('main', 'urlprefix')
    PicURL = make_picture_url(comic.coverfront.string, urlprefix)
    Description = make_description(config, comic)
    ndata = dict(Title=Title,
                Subtitle=Subtitle,
                PicURL=PicURL,
                Description=Description,
    )
    ndata['Product:Brand'] = comic.publisher.displayname.string
    if comic.isbn is not None:
        ndata['Product:ISBN'] = comic.isbn.string
    if comic.barcode is not None:
        ndata['Product:UPC'] = comic.barcode.string
    data.update(ndata)
    Quantity = int(comic.quantity.string)
    if Quantity > config.getint('reqfields', 'quantity'):
        data['*Quantity'] = Quantity
    return data
