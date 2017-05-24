from mako.template import Template
import markdown

#MAXDESCRIPTIONLENGTH = 32765
MAXDESCRIPTIONLENGTH = 499999

def make_description(config, comic):
    templatefile = config.get('main', 'template')
    t = Template(file(templatefile).read())
    desc = t.render(comic=comic)
    if config.getboolean('main', 'md_template'):
        desc = markdown.markdown(desc, safe_mode='escape')
    desc = desc.replace('\n', '')
    if len(desc) > MAXDESCRIPTIONLENGTH:
        raise RuntimeError, "Max Description length exceeded for comic", comic.id
    return desc


def make_title(config, comic):
    template = config.get('main', 'title_template')
    t = Template(template)
    title = t.render(comic=comic)
    if len(title) > 80:
        raise RuntimeError, "Title too long %s" % comic.id.string
    return title
