import os

def make_picture_url(filename, urlprefix):
    filename = filename.replace('\\', '/')
    basename = os.path.basename(filename)
    return os.path.join(urlprefix, basename)
    
