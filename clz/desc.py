from mako.template import Template

MAXDESCRIPTIONLENGTH = 32765

def make_description(config, comic):
    templatefile = config.get('main', 'template')
    t = Template(templatefile)
    desc = t.render(comic=comic)
    desc = desc.replace('\n', '')
    if len(desc) > MAXDESCRIPTIONLENGTH:
        raise RuntimeError, "Max Description length exceeded for comic", comic.id
    return desc

