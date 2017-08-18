#!/usr/local/bin/python

import cgi, urllib2
import basics
import db


'''
+-------------+-------------+------+-----+---------+----------------+
| Field       | Type        | Null | Key | Default | Extra          |
+-------------+-------------+------+-----+---------+----------------+
| id          | int(11)     |      | PRI | NULL    | auto_increment | TCPP
| groupid     | int(11)     | YES  |     | NULL    |                | T PP
| name        | text        | YES  |     | NULL    |                | TCPP
| description | text        | YES  |     | NULL    |                | TCPP
| credit      | varchar(32) | YES  |     | NULL    |                | T  P
| file        | varchar(80) | YES  |     | NULL    |                | T  P
| display     | int(6)      | YES  |     | NULL    |                |  CPP
| image       | int(11)     | YES  |     | NULL    |                |   P 
| flags       | int(11)     | YES  |     | 0       |                |  CPP
| level       | varchar(12) | YES  |     | NULL    |                | T   
+-------------+-------------+------+-----+---------+----------------+
'''


def LoadCat(category):
    dbi = db.db(basics.cgibin)
    cat = dbi.select("category", ['id', 'name', 'description', 'display', 'flags'], "id=%s" % category)
    cat['projs'] = dbi.select("project", ['id', 'category', 'name', 'description', 'display'], "category=%s" % category)
    return cat


def LoadProj(project):
    pass


def LoadPicture(picture):
    pass


def LoadTree():
    dbi = db.db(basics.cgibin)
    cats = dbi.select("category", ['id', 'name', 'description', 'display', 'flags'])
    projs = dbi.select("project", ['id', 'category', 'name', 'description', 'display', 'flags'])
    pics = dbi.select("picture", ['id', 'project', 'name', 'description', 'credit', 'file', 'display', 'flags'])
    tree = {}
    for cat in cats:
	catid = int(cat['id'])
	tree[catid] = {'name' : cat['name'], 'description' : cat['description'], 'projs' : {}, 'display' : cat['display'], 'flags' : cat['flags']}
	for proj in projs:
	    projid = int(proj['id'])
	    pcatid = int(proj['category'])
	    if not pcatid == catid:
		continue
	    tree[catid]['projs'][projid] = {'name' : proj['name'], 'description' : proj['description'], 'pics' : {}, 'display' : proj['display'], 'flags' : proj['flags']}
	    for pic in pics:
		picid = int(pic['id'])
		pprojid = int(pic['project'])
		if not pprojid == projid:
		    continue
		tree[catid]['projs'][projid]['pics'][picid] = {'name' : pic['name'], 'description' : pic['description'], 'credit' : pic['credit'], 'file' : pic['file'], 'pics' : {}, 'display' : pic['display'], 'flags' : pic['flags']}

    return tree



def DispFull():
    tree = LoadTree()
    print '<form action="gedit.cgi">'
    print basics.FormatTableStart()
    cats = tree.keys()
    cats.sort(lambda x,y: cmp(tree[x]['display'], tree[y]['display']))
    for cat in cats:
	rowstarted = True
	print basics.FormatRowStart()
	print basics.FormatCell(0,
		'<input type=checkbox name="disp.%s" %s>' % (cat, checked(tree[cat]['flags'] & 1)) + tree[cat]['name'] + ' : ' + tree[cat]['description'],
		also={'rowspan':len(tree[cat]['projs'])})
	for proj in tree[cat]['projs']:
	    if not rowstarted:
		print basics.FormatRowStart()
		rowstarted = False
	    project = tree[cat]['projs'][proj]
	    print basics.FormatCellStart(1)
	    print project['name'] + ' : ' + project['description']
	    print basics.FormatCellEnd()
	    print basics.FormatCellStart(2)
	    for pic in project['pics']:
		picture = project['pics'][pic]
		print picture['file'] + '<br>'
	    print basics.FormatCellEnd()
	    print basics.FormatRowEnd()
    print basics.FormatTableEnd()
    print '<input type="submit">'
    print "</form>"

if __name__ == '__main__':
    pass
