#!/usr/local/bin/python

import cgitb; cgitb.enable()
import cgi, urllib2
import basics
import db
import scc

dbi = None

def PrintPic(proj, pic):
    print '<div class="index">'
    print '<h2>' + proj['name'] + '</h2>'
    print '<div class="gallerypicture">'
    print '<a href="../gallery/orig/%(file)s">%(name)s<br><img src="../gallery/m_%(file)s"><br>%(description)s</a>' % pic
    print '</div>'
    print '</div>'


def PrintProj(proj, pics):
    print '<div class="gallery">'
    print '<h2>' + proj['name'] + '</h2>'
    pics.sort(lambda x,y: cmp(x['display'], y['display']))
    for pic in pics:
	print '<div class="galleryitem"><a href="gallery.cgi?pic=%(id)d">%(name)s<br><img src="../gallery/s_%(file)s"></a></div>' % pic
    print '</div>'


def PrintCat(cat, projs):
    print '<div class="gallery">'
    print '<h2>' + cat['name'] + '</h2>'
    projs.sort(lambda x,y: cmp(x['display'], y['display']))
    for proj in projs:
	proj['img'] = dbi.select("picture", ['id', 'name', 'description', 'file'], "id=%s" % int(proj['image']))[0]['file']
	print '<div class="galleryitem"><a href="gallery.cgi?proj=%(id)d">%(name)s<br><img src="../gallery/s_%(img)s"></a></div>' % proj
    print '</div>'


if __name__ == '__main__':
    basics.ReadForm()
    print basics.FormatHtml()
    print basics.FormatHead(extra=scc.FormatHead())
    print scc.FormatMainMenu()

    dbi = db.db(basics.cgibin)
    cats = dbi.select("category", ['id', 'name', 'description'])

    if basics.form.get('pic'):
	pic = dbi.select("picture", ['id', 'name', 'description', 'file', 'project'], "id=%s" % basics.form['pic'])[0]
	PrintPic(dbi.select("project", ['id', 'name', 'description'], "id=%s" % pic['project'])[0], pic)
    elif basics.form.get('proj'):
	PrintProj(dbi.select("project", ['id', 'name', 'description'], "id=%s" % basics.form['proj'])[0],
		  dbi.select("picture", ['id', 'name', 'description', 'file', 'display'], "project=%s" % basics.form['proj']))
    elif basics.form.get('cat'):
	PrintCat(dbi.select("category", ['id', 'name', 'description'], "id=%s" % basics.form['cat'])[0],
		 dbi.select("project", ['id', 'name', 'description', 'image', 'display'], "category=%s" % basics.form['cat']))
    else:
	print '<meta http-equiv="refresh" content="0;url=..">'

    print basics.FormatTail()
