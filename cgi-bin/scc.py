#!/usr/local/bin/python

import basics
import db


def FormatHead():
    return '''<link rel="icon" href="http://www.sportscar-craftsmen.com/favicon.ico" type="image/x-icon" />
<link rel="shortcut icon" href="http://www.sportscar-craftsmen.com/favicon.ico" type="image/x-icon" />
<link rel="stylesheet" type="text/css" href="/style.css" />
<link rel="stylesheet" type="text/css" href="/glossymenu.css" />'''


def mcmp(a, b):
    return cmp(a['display'], b['display'])


def LoadCats():
    dbi = db.db(basics.cgibin)
    cats = dbi.select("category", ['id', 'name', 'description', 'display'])
    cats.sort(mcmp)
    return filter(lambda x: x['display'] > 0, cats)



def FormatMainMenu():
    ostr = '<ul class="glossymenu" style="float: left">\n'
    for cat in LoadCats():
	ostr += '<li><a href="gallery.cgi?cat=%(id)d">%(name)s</a></li>\n' % cat
    ostr += '<li><a href="http://maps.google.com/maps?f=q&hl=en&geocode=&q=5865+Kendall+Court,+Arvada,+CO+80002&sll=37.0625,-95.677068&sspn=68.73358,95.976563&ie=UTF8&ll=39.80036,-105.066032&spn=0.008342,0.011716&z=16&iwloc=cent">Map</a></li>\n</ul>'
    return ostr



if __name__ == '__main__':
    pass
