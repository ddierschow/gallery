#!/usr/local/bin/python

# todo:
#  how about copy picture?
#  page titles

# requests:

# Wed also like embed links to other sections on the site in
# that text. i.e. when we refer to body work, wed like the text to
# send you to the body work page. I know how to put those links in
# there with htmlwould it be easier for you if I did that before
# sending you the text?

# Also, the bug with the projects returning to "Not Shown" if you
# don't choose an option from the drop down menu still persists. And
# if you do choose an option- even the same category the project is
# already in- it goes to the end of the list. Now, this isn't as much
# as a problem as it had been when it was doing that to the pictures,
# but in some cases the order of the projects is thoughtfully chosen.
# So if you can take a look at that, it'd be great.

# The photo buttons moved up to the sides of the photos, if possible.

# Link color tweaking. Gray-er if possible.

# The second wish, that I realize may be impossible, is if it may be
# possible to expand out of the category/project/photo formula.
# There's one section where it would be really, really useful to
# have it be category/project/project/photo. We would only need it
# for one section, if that would make it any more feasible. We'd
# like to separate "Parts We Make" into Marks and *then* projects
# and photos. If this can't easily be done, don't worry about it.


# permissions
#   v = view
#   m = modify
#   u = upload
#   a = administrate

#-------------+-------------+------+-----+---------+----------------+-------+
# Field       | Type        | Null | Key | Default | Extra          | Table |
#-------------+-------------+------+-----+---------+----------------+-------+
# id          | int(11)     |      | PRI | NULL    | auto_increment | TCPP  |
# groupid     | int(11)     | YES  |     | NULL    |                | T PP  |
# name        | text        | YES  |     | NULL    |                | TCPP  |
# description | text        | YES  |     | NULL    |                | TCPP  |
# alttext     | text        | YES  |     | NULL    |                | TCPP  |
# credit      | varchar(32) | YES  |     | NULL    |                | T  P  |
# file        | varchar(80) | YES  |     | NULL    |                | T  P  |
# display     | int(6)      | YES  |     | NULL    |                |  CPP  |
# image       | int(11)     | YES  |     | NULL    |                |   P   |
# flags       | int(11)     | YES  |     | 0       |                |  CPP  |
# level       | varchar(12) | YES  |     | NULL    |                | T     |
#-------------+-------------+------+-----+---------+----------------+-------+


import cgitb; cgitb.enable()
import cgi, datetime, os, sys, urllib2
import basics
import db
import styles
basics.artdir = 'art'

upone = {'category' : 'top', 'project' : 'category', 'picture' : 'project'}
dnone = {'category' : 'project', 'project' : 'picture', 'top' : 'category'}
shortform = {'category' : 'cat', 'project' : 'proj', 'picture' : 'pic'}
longform  = {'top' : 'top', 'cat' : 'category', 'proj' : 'project', 'pic' : 'picture'}

flag_shown  =  1
flag_center =  2
flag_after  =  4
flag_unlink =  8
flag_link   = 16
flag_image  = 32


def checked(x):
    if x:
	return 'checked'
    return ''



def System(action):
    cook = basics.GetCookies()
    open('logs/system.log', 'a').write('%s %s %s\n' % (str(datetime.datetime.today()), cook.get('id'), action))
    open('logs/system.log', 'a').write('    %s\n' % os.getcwd())
    os.system(action)



def Log(action):
    cook = basics.GetCookies()
    open('logs/change.log', 'a').write('%s %s %s\n' % (str(datetime.datetime.today()), cook.get('id'), action))



def Styles():
    sset = styles.StyleSet(['.title', '.table', '.cell', '.cell,0,2', '.hcell', 'img', '.img', '.header', '.warning', '.righty', '.lefty'])
    sset['body']['ff'] = 'Johnston, "ITC Johnston", "P22 London Underground", "Gill Sans", "Trebuchet MS", Ariel, Helvetica, sans-serif;'
    sset['body']['bgc'] = '#CCFFCC'
    sset['.title']['c'] = '#003300'
    sset['.header'].update({'ta': 'left', 'f': 'left', 'fw': 'bold'})
    sset['.righty']['f'] = 'right'
    sset['.lefty']['f'] = 'left'
    sset['.warning'].update({'fw': 'bold', 'c': '#CC0000'})
    sset['.table'].update({'bgc': '#9999FF', 'clr': 'both', 'bsp': '0px', 'bw': '2px'})
    sset['.cell']['bgc'] = '#EEEEFF'
    sset['.hcell']['bgc'] = '#EEEEFF'
    sset['.cell_0'].update({'ta': 'center', 'va': 'middle', 'bgc': '#EEEEFF'})
    sset['.cell_2'].update({'ta': 'center', 'va': 'middle', 'bgc': '#EEEEFF'})
    sset['img'].update({'bw': '0', 'va': 'middle'})
    sset['.img'].update({'bw': '0', 'va': 'middle'})
    return sset



def ProcessForm():
    dbi = db.db(basics.cgibin)
    ordlist = []
    idlist = []
    edittype = basics.form.get('edit', None)
    if edittype == 'cat':
	basics.form.setdefault('name_cat.' + basics.form['cat'], "")
	basics.form.setdefault('desc_cat.' + basics.form['cat'], "")
	basics.form.setdefault('alttext_cat.' + basics.form['cat'], "")
	basics.form.setdefault('centered_cat.' + basics.form['cat'], "")
	basics.form.setdefault('unlinked_cat.' + basics.form['cat'], "")
	basics.form.setdefault('extlinked_cat.' + basics.form['cat'], "")
	basics.form.setdefault('linkimg_cat.' + basics.form['cat'], "")
    elif edittype == 'proj':
	basics.form.setdefault('name_proj.' + basics.form['proj'], "")
	basics.form.setdefault('desc_proj.' + basics.form['proj'], "")
	basics.form.setdefault('alttext_proj.' + basics.form['proj'], "")
	basics.form.setdefault('centered_proj.' + basics.form['proj'], "")
	basics.form.setdefault('unlinked_proj.' + basics.form['proj'], "")
	basics.form.setdefault('extlinked_proj.' + basics.form['proj'], "")
    elif edittype == 'pic':
	basics.form.setdefault('name_pic.' + basics.form['pic'], "")
	basics.form.setdefault('desc_pic.' + basics.form['pic'], "")
	basics.form.setdefault('alttext_pic.' + basics.form['pic'], "")
	basics.form.setdefault('credit_pic.' + basics.form['pic'], "")
	basics.form.setdefault('centered_pic.' + basics.form['pic'], "")
	basics.form.setdefault('unlinked_pic.' + basics.form['pic'], "")
	basics.form.setdefault('extlinked_pic.' + basics.form['pic'], "")
    for fullkey in basics.form.keys():
	key = fullkey
	id = '0'
	if '.' in fullkey:
	    key, id = tuple(fullkey.split('.'))
	formval = basics.form[fullkey]
	intval = None
	if formval.isdigit():
	    intval = int(formval)
	if key == 'create':
	    Create(dbi, id, intval)
	elif key == 'scrape_file':
	    Scrape(dbi)
	elif key == 'upload_file':
	    Upload(dbi)
	elif key == 'move_proj':
	    MoveProj(dbi, id, intval)
	elif key == 'moveup_cat':
	    MoveUp(dbi, 'category', id, formval)
	elif key == 'moveup_proj':
	    MoveUp(dbi, 'project', id, formval)
	elif key == 'moveup_pic':
	    MoveUp(dbi, 'picture', id, formval)
	elif key == 'movedn_cat':
	    MoveDown(dbi, 'category', id, formval)
	elif key == 'movedn_proj':
	    MoveDown(dbi, 'project', id, formval)
	elif key == 'movedn_pic':
	    MoveDown(dbi, 'picture', id, formval)
	elif key == 'disp':
	    idlist.append(id)
	elif key == 'order':
	    ordlist.append([int(id), intval])
	elif key == 'flag_pic':
	    Flagship(dbi, id, formval)
	elif key == 'del_cat':
	    Remove(dbi, 'category', formval)
	elif key == 'del_proj':
	    Remove(dbi, 'project', formval)
	elif key == 'del_pic':
	    Remove(dbi, 'picture', formval)
	elif key == 'remove_cat':
	    RemovePrep(dbi, 'category', id, formval)
	elif key == 'remove_proj':
	    RemovePrep(dbi, 'project', id, formval)
	elif key == 'remove_pic':
	    RemovePrep(dbi, 'picture', id, formval)
	elif key == 'name_cat':
	    Name(dbi, 'category', id, formval)
	elif key == 'name_proj':
	    Name(dbi, 'project', id, formval)
	elif key == 'name_pic':
	    Name(dbi, 'picture', id, formval)
	elif key == 'desc_cat':
	    Description(dbi, 'category', id, formval)
	elif key == 'desc_proj':
	    Description(dbi, 'project', id, formval)
	elif key == 'desc_pic':
	    Description(dbi, 'picture', id, formval)
	elif key == 'alttext_cat':
	    AltText(dbi, 'category', id, formval)
	elif key == 'alttext_proj':
	    AltText(dbi, 'project', id, formval)
	elif key == 'alttext_pic':
	    AltText(dbi, 'picture', id, formval)
	elif key == 'credit_pic':
	    Credit(dbi, 'picture', id, formval)
	elif key == 'linkimg_cat':
	    SetFlag(dbi, 'category', id, flag_image, formval)
	elif key == 'linkimg_proj':
	    SetFlag(dbi, 'project', id, flag_image, formval)
	elif key == 'linkimg_pic':
	    SetFlag(dbi, 'picture', id, flag_image, formval)
	elif key == 'extlinked_cat':
	    SetFlag(dbi, 'category', id, flag_link, formval)
	elif key == 'extlinked_proj':
	    SetFlag(dbi, 'project', id, flag_link, formval)
	elif key == 'extlinked_pic':
	    SetFlag(dbi, 'picture', id, flag_link, formval)
	elif key == 'unlinked_cat':
	    SetFlag(dbi, 'category', id, flag_unlink, formval)
	elif key == 'unlinked_proj':
	    SetFlag(dbi, 'project', id, flag_unlink, formval)
	elif key == 'unlinked_pic':
	    SetFlag(dbi, 'picture', id, flag_unlink, formval)
	elif key == 'centered_cat':
	    SetFlag(dbi, 'category', id, flag_center, formval)
	elif key == 'centered_proj':
	    SetFlag(dbi, 'project', id, flag_center, formval)
	elif key == 'centered_pic':
	    SetFlag(dbi, 'picture', id, flag_center, formval)
	elif key == 'rotate':
	    Rotate(dbi, id, formval)
	elif key== 'trash_delete':
	    TrashDelete(dbi, formval)
	elif key== 'trash_restore':
	    TrashRestore(dbi, formval)
	elif key== 'trash_restore_all':
	    TrashRestoreAll(dbi)
	elif key== 'trash_empty':
	    TrashEmpty(dbi)
	elif key=='regenerate':
	    Regenerate(dbi, id)
    if edittype == 'proj':
	OrderDisplay(dbi, 'picture', int(basics.form['proj']), ordlist)
    if edittype == 'pic':
	MovePic(dbi, basics.form['pic'], basics.form['sel_proj'])
    elif edittype:
	UpdateShown(dbi, edittype, idlist)



def Create(dbi, id, parent):
    if not basics.IsAllowed('m'):
	return
    lvl = longform[id]
    res = dbi.select(lvl, ['max(display)'])[0]['max(display)']
    if lvl == 'category':
	dbi.insert(lvl, {'display' : int(res) + 1, 'flags' : 0})
    else:
	dbi.insert(lvl, {'display' : int(res) + 1, 'flags' : 0, 'groupid' : parent})
    newid = dbi.select(lvl, ['max(id)'])[0]['max(id)']
    basics.form[id] = newid
    Log('create %s %s' % (lvl, newid))


def MovePic(dbi, id, proj):
    if not basics.IsAllowed('m'):
	return
    if proj and int(proj) > 0:
	res = dbi.select('picture', ['groupid'], 'id=%s' % id)[0]
	dbi.update('picture', {'display': 999999, 'groupid': proj}, "id=%s" % id)
	NormalizeDisplay(dbi, 'picture', proj)
	NormalizeDisplay(dbi, 'picture', res['groupid'])
	basics.form['proj'] = proj
	Log('movepic %s' % id)


def MoveProj(dbi, id, val):
    if val < 0 or not basics.IsAllowed('m'):
	return
    res = dbi.select('project', ['groupid'], 'id=%s' % id)[0]
    dbi.update('project', {'display': 999999, 'groupid': val}, "id=%s" % id)
    NormalizeDisplay(dbi, 'project', val)
    NormalizeDisplay(dbi, 'project', res['groupid'])
    basics.form['cat'] = val
    Log('moveproj %s' % id)


def MoveUp(dbi, lvl, id, val):
    if not basics.IsAllowed('m'):
	return
    if lvl != 'category':
	res = dbi.select(lvl, ['groupid', 'display'], "id=%s" % id)
	groupid = res[0]['groupid']
	res = dbi.select(lvl, ['id', 'display'], "groupid=%s" % groupid, order="display")
	for ires in range(1, len(res)):
	    if res[ires]['id'] == int(id):
		res = res[ires - 1: ires + 1]
		break
	basics.form[shortform[upone[lvl]]] = groupid
    else:
	res = dbi.select(lvl, ['id', 'display'], order="display")
	for ires in range(1, len(res)):
	    if res[ires]['id'] == int(id):
		res = res[ires - 1: ires + 1]
		break
    if len(res) == 2:
	dbi.update(lvl, {'display': res[0]['display']}, 'id=%s' % res[1]['id'])
	dbi.update(lvl, {'display': res[1]['display']}, 'id=%s' % res[0]['id'])
	Log('moveup %s %s' % (lvl, id))


def MoveDown(dbi, lvl, id, val):
    if not basics.IsAllowed('m'):
	return
    if lvl != 'category':
	res = dbi.select(lvl, ['groupid', 'display'], "id=%s" % id)
	groupid = res[0]['groupid']
	res = dbi.select(lvl, ['id', 'display'], "groupid=%s" % groupid, order="display")
	for ires in range(0, len(res) - 1):
	    if res[ires]['id'] == int(id):
		res = res[ires: ires + 2]
		break
	basics.form[shortform[upone[lvl]]] = groupid
    else:
	res = dbi.select(lvl, ['id', 'display'], order="display")
	for ires in range(1, len(res)):
	    if res[ires]['id'] == int(id):
		res = res[ires: ires + 2]
		break
    if len(res) == 2:
	dbi.update(lvl, {'display': res[0]['display']}, 'id=%s' % res[1]['id'])
	dbi.update(lvl, {'display': res[1]['display']}, 'id=%s' % res[0]['id'])
	Log('movedown %s %s' % (lvl, id))


def Flagship(dbi, id, val):
    if not basics.IsAllowed('m'):
	return
    dbi.update('project', {'image': val}, 'id=%s' % id)
    basics.form['proj'] = id
    Log('flagship %s' % id)


def RemovePrep(dbi, lvl, id, val):
    if not basics.IsAllowed('m'):
	return
    if lvl != 'category':
	basics.form[shortform[upone[lvl]]] = val
    if lvl != 'picture':
	res = dbi.select(dnone[lvl], ['id'], 'groupid=%s' % id)
	if res:
	    print '<span class="warning"> %s isn\'t empty!</span><p>' % lvl
	    return
    res = dbi.select(lvl, ['name'], 'id=%s' % id)[0]
    print '<div style="text-align: center; border-width: 1px; width: 300px;">'
    print '<span class="warning">You are trying to remove a %s!</span><p><b>%s</b><p>' % (lvl, res['name'])
    print '<div class="lefty"><a href="gedit.cgi?del_%s=%s">%s - i\'m sure!</a></div>' % (shortform[lvl], id, basics.FmtButton('yes'))
    print '<div class="righty"><a href="gedit.cgi?%s=%s">%s - get me outta here!</a></div>' % (shortform[upone[lvl]], val, basics.FmtButton('no'))
    print '</div>'
    print basics.FormatTail()
    sys.exit(0)


def Remove(dbi, lvl, id):
    if not basics.IsAllowed('m'):
	return
    res = dbi.select(lvl, where='id=%s' % id)[0]
    if lvl == 'picture':
	print '<!-- mv gallery/orig/%s gallery/trash/' % res['file'], ' -->'
	System('mv "gallery/orig/%s" gallery/trash/' % res['file'])
	print '<!-- rm gallery/[mst]_%s' % res['file'], ' -->'
	System('rm "gallery/[mst]_%s"' % res['file'])
    dbi.remove(lvl, 'id=%s' % id)
    if lvl != 'category':
	basics.form[shortform[upone[lvl]]] = res['groupid']
	NormalizeDisplay(dbi, lvl, res['groupid'])
    dbi.insert('trash', {
	'level' : lvl,
	'groupid': res.get('groupid', ''),
	'name': res.get('name', ''),
	'description': res.get('description', ''),
	'alttext': res.get('alttext', ''),
	'credit': res.get('credit', ''),
	'file': res.get('file', '')})
    Log('remove %s %s' % (lvl, id))


def Name(dbi, lvl, id, val):
    if not basics.IsAllowed('m'):
	return
    #res = dbi.select(lvl, ['groupid'], 'id=%s' % id)[0]
    #basics.form[shortform[upone[lvl]]] = res['groupid']
    basics.form[shortform[lvl]] = id
    dbi.update(lvl, {'name' : val}, 'id=%s' % id)
    Log('name %s %s' % (lvl, id))


def Description(dbi, lvl, id, val):
    if not basics.IsAllowed('m'):
	return
    dbi.update(lvl, {'description' : val}, 'id=%s' % id)
    Log('desc %s %s' % (lvl, id))


def AltText(dbi, lvl, id, val):
    if not basics.IsAllowed('m'):
	return
    dbi.update(lvl, {'alttext' : val}, 'id=%s' % id)
    Log('alttext %s %s' % (lvl, id))


def Credit(dbi, lvl, id, val):
    if not basics.IsAllowed('m'):
	return
    basics.form[shortform[lvl]] = id
    dbi.update(lvl, {'credit' : val}, 'id=%s' % id)
    Log('cred %s %s' % (lvl, id))


def SetFlag(dbi, lvl, id, mask, val):
    res = dbi.select(lvl, ['flags'], 'id=%s' % id)[0]
    if val:
	flags = res['flags'] | mask
    else:
	flags = res['flags'] & ~mask
    dbi.updateflag(lvl, {'flags' : flags}, 'id=%s' % id)


def UpdateShown(dbi, edittype, idlist):
    if not basics.IsAllowed('m'):
	return
    lvl = dnone[longform[edittype]]
    if idlist:
	if lvl == 'category':
	    dbi.updateflag(lvl, {'flags' : 'flags&~' + str(flag_shown)});
	else:
	    res = dbi.select(lvl, ['groupid'], 'id=%s' % idlist[0])[0]
	    dbi.updateflag(lvl, {'flags' : 'flags&~' + str(flag_shown)}, 'groupid=%s' % res['groupid'])
	dbi.updateflag(lvl, {'flags' : 'flags|' + str(flag_shown)}, 'id in (%s)' % ','.join(idlist))


def Rotate(dbi, id, angle):
    if not basics.IsAllowed('m'):
	return
    basics.form['pic'] = id
    fn = dbi.select('picture', ['file'], where='id=%s' % id)[0]['file']
    System('mv "gallery/orig/%s" gallery/trash/' % fn)
    System('cat "gallery/trash/%s" |jpegtopnm|pamflip -rotate%s|pnmtojpeg > "gallery/orig/%s"' % (fn, angle, fn))
    SmallerizePic("gallery/orig/", fn)
    Log('rotate %s' % id)


def Regenerate(dbi, id):
    if not basics.IsAllowed('m'):
	return
    basics.form['pic'] = id
    fn = dbi.select('picture', ['file'], where='id=%s' % id)[0]['file']
    SmallerizePic("gallery/orig/", fn)
    Log('regenerate %s' % id)


def TrashDelete(dbi, id):
    if not basics.IsAllowed('a'):
	return
    res = dbi.select('trash', where='id=%s' % id)[0]
    if res['level'] == 'picture':
	System('rm "gallery/trash/%s"' % res['file'])
    dbi.remove('trash', 'id=%s' % id)
    basics.form['trash'] = 1
    Log('trashdel %s' % id)


def TrashRestore(dbi, id):
    if not basics.IsAllowed('a'):
	return
    res = dbi.select('trash', where='id=%s' % id)[0]
    if res['level'] == 'picture':
	System('mv "gallery/trash/%s" gallery/orig' % res['file'])
	SmallerizePic('gallery/orig/', res['file'])
    if res['level'] == 'category':
	dbi.insert('picture', {'display' : '999999', 'flags' : 0, 'name' : res['name'], 'description' : res['description'], 'alttext' : res['alttext']})
    elif res['level'] == 'project':
	dbi.insert('picture', {'display' : '999999', 'flags' : 0, 'groupid' : res['groupid'],
		'name' : res['name'], 'description' : res['description'], 'alttext' : res['alttext']})
    elif res['level'] == 'picture':
	dbi.insert('picture', {'display' : '999999', 'flags' : 0, 'groupid' : res['groupid'], 'file' : res['file'],
		'name' : res['name'], 'description' : res['description'], 'credit' : res['credit'], 'alttext' : res['alttext']})
    basics.form[shortform[res['level']]] = id
    Log('trashrest %s' % id)


def TrashRestoreAll(dbi):
    if not basics.IsAllowed('a'):
	return
    res = dbi.select('trash', where="level='picture'")
    for r in res:
	if r['level'] == 'picture':
	    System('mv "gallery/trash/%s" gallery/orig' % r['file'])
	    SmallerizePic('gallery/orig/', r['file'])
	    dbi.insert('picture', {'display' : '999999', 'flags' : 0, 'groupid' : 66, 'file' : r['file'],
		    'name' : r['name'], 'description' : r['description'], 'credit' : r['credit'], 'alttext' : r['alttext']})
	    dbi.remove('trash', where="id='%s'" % r['id'])
    Log('trashrestall')


def TrashEmpty(dbi):
    if not basics.IsAllowed('a'):
	return
    dbi.remove('trash')
    Log('trashempty')



def OrderDisplay(dbi, lvl, groupid, ordlist):
    ordlist.sort(lambda x, y: x[1] - y[1])
    for i in range(0, len(ordlist)):
	ordlist[i][1] = i
    orddict = dict(ordlist)
    print '<!-- order list:', ordlist, '-->'
    if lvl == 'category':
	res = dbi.select(lvl, ['id', 'display'], order='display')
    else:
	res = dbi.select(lvl, ['id', 'display'], 'groupid=%s' % groupid, 'display')
    newdisp = 0
    for ent in res:
	dbi.update(lvl, {'display' : orddict.get(ent['id'], newdisp)}, 'id=%s' % ent['id'])
	newdisp += 1



def NormalizeDisplay(dbi, lvl, groupid):
    if lvl == 'category':
	res = dbi.select(lvl, ['id', 'display'], order='display')
    else:
	res = dbi.select(lvl, ['id', 'display'], 'groupid=%s' % groupid, 'display')
    newdisp = 0
    for ent in res:
	dbi.update(lvl, {'display' : newdisp}, 'id=%s' % ent['id'])
	newdisp += 1



def PictureEditor(pic):
    print '<div class="header">picture editor</div>'
    print '<div class="righty"><a href="logout.cgi">%s</a></div>' % basics.FmtButton('log out')
    print '<form name="pic" action="gedit.cgi"><input type="hidden" name="edit" value="pic">'
    print '<input type="hidden" name="pic" value="%s">' % pic
    dbi = db.db(basics.cgibin)
    pic = dbi.select("picture", ['id', 'name', 'description', 'alttext', 'display', 'credit', 'file', 'flags', 'groupid'], "id=%s" % pic)[0]
    projs = dbi.select("project", ['id', 'name', 'description','alttext',  'display', 'flags', 'groupid'], order="display")
    cats = dbi.select("category", ['id', 'name', 'description','alttext',  'display', 'flags'], order="display")
    for p in projs:
	if p['id'] == pic['groupid']:
	    proj = p
    if basics.IsAllowed('m'):
	print '<script language=javascript>'
	print 'var cat_opt = new Array(%s);' % ','.join(map(lambda x: '"%s"' % x['name'].replace('"', r'\"'), cats))
	print 'var cat_val = new Array(%s);' % ','.join(map(lambda x: '"%s"' % x['id'], cats))
	move_opts = '\n'.join(map(lambda x: '<option value="%(id)s">%(name)s</option>' % x, cats))
	print 'var proj_opt_none = new Array("");'
	print 'var proj_val_none = new Array("");'
	proj_opt = {}
	proj_val = {}
	for p in projs:
	    proj_opt.setdefault(p['groupid'], [])
	    proj_val.setdefault(p['groupid'], [])
	    proj_opt[p['groupid']].append(p['name'])
	    proj_val[p['groupid']].append(p['id'])
	print 'var proj_opt_0 = new Array("--------");'
	print 'var proj_val_0 = new Array("0");'
	for opt in proj_opt:
	    print 'var proj_opt_%s = new Array(%s);' % (opt, ','.join(map(lambda x: '"%s"' % str(x).replace('"', r'\"'), proj_opt[opt])))
	for val in proj_val:
	    print 'var proj_val_%s = new Array(%s);' % (val, ','.join(map(lambda x: '"%s"' % x, proj_val[val])))
	print '''function changeval()
{
 var val1 = document.pic.sel_cat.value;
 var opt2ar = eval("proj_opt_" + val1);
 var val2ar = eval("proj_val_" + val1);
 var sel = document.pic.sel_proj;
 sel.options.length = 0;
 for(var opt=0; opt<opt2ar.length; opt++)
 {
  sel.options[opt] = new Option(opt2ar[opt],val2ar[opt]);
 }
}
</script>
'''
    for cat in cats:
	if cat['id'] == proj['groupid']:
	    break
    print basics.FormatTableStart()
    print basics.FormatRowStart()
    print basics.FormatCell(1, 'Category', hdr=True)
    print basics.FormatCell(1, cat['name'])
    print basics.FormatRowEnd()
    print basics.FormatRowStart()
    print basics.FormatCell(1, 'Project', hdr=True)
    print basics.FormatCell(1, proj['name'])
    print basics.FormatRowEnd()
    print basics.FormatRowStart()
    print basics.FormatCell(1, 'Picture Name', hdr=True)
    print basics.FormatCell(1, '<input type="text" size=80 maxlength=80 name="name_pic.%s" value="%s">' % (pic['id'], basics.Literal(pic['name'])))
    print basics.FormatRowEnd()
    print basics.FormatRowStart()
    print basics.FormatCell(1, 'Description', hdr=True)
    print basics.FormatCell(1, '<textarea cols=80 rows=8 wrap="soft" name="desc_pic.%s">%s</textarea>' % (pic['id'], basics.Literal(pic['description'])))
    print basics.FormatRowEnd()
    print basics.FormatRowStart()
    print basics.FormatCell(1, 'Alt Text', hdr=True)
    print basics.FormatCell(1, '<input type="text" size=80 maxlength=80 name="alttext_pic.%s" value="%s">' % (pic['id'], basics.Literal(pic['alttext'])))
    print basics.FormatRowEnd()
    print basics.FormatRowStart()
    print basics.FormatCell(1, 'Picture not linked', hdr=True)
    print basics.FormatCell(1, '<input type=checkbox name="unlinked_pic.%s" value="1" %s>' % (pic['id'], checked(pic['flags'] & flag_unlink)))
    print basics.FormatRowEnd()
    print basics.FormatRowStart()
    print basics.FormatCell(1, 'Picture after text', hdr=True)
    print basics.FormatCell(1, '<input type=checkbox name="centered_pic.%s" value="1" %s>' % (pic['id'], checked(pic['flags'] & flag_center)))
    print basics.FormatRowEnd()
    #print basics.FormatRowStart()
    #print basics.FormatCell(1, 'External link', hdr=True)
    #print basics.FormatCell(1, '<input type=checkbox name="extlinked_pic.%s" value="1" %s>' % (pic['id'], checked(pic['flags'] & flag_link)))
    #print basics.FormatRowEnd()
    print basics.FormatRowStart()
    print basics.FormatCell(1, 'Credit', hdr=True)
    print basics.FormatCell(1, '<input type="text" size=32 maxlength=32 name="credit_pic.%s" value="%s">' % (pic['id'], basics.Literal(pic['credit'])))
    print basics.FormatRowEnd()
    if basics.IsAllowed('m'):
	print basics.FormatRowStart()
	print basics.FormatCell(1, 'Move to', hdr=True)
	print basics.FormatCell(1, '<select name="sel_cat" onchange=changeval()><option value="-1">--------</option>%s</select><select name="sel_proj"><option value="-1">--------</option></select>' % move_opts)
	print basics.FormatRowEnd()
    print basics.FormatTableEnd()
    print '<div class="lefty">'
    if basics.IsAllowed('m'):
	print '<input type="image" name="submit" src="../art/but_save_changes.gif" class="img"> -'
	print '<a href="gedit.cgi?rotate.%s=270">%s</a> -' % (pic['id'], basics.FmtButton('rotate right'))
	print '<a href="gedit.cgi?rotate.%s=90">%s</a> -' % (pic['id'], basics.FmtButton('rotate left'))
	print '<a href="gedit.cgi?rotate.%s=180">%s</a> -' % (pic['id'], basics.FmtButton('rotate 180'))
	print '<a href="gedit.cgi?regenerate.%s=1">%s</a>' % (pic['id'], basics.FmtButton('regenerate'))
    print '</div>'
    print '<div class="righty"><a href="gedit.cgi?proj=%s">%s</a></div><br clear=all>' % (proj['id'], basics.FmtButton('picture list'))
    print basics.FmtImg('t_' + pic['file'])
    print basics.FmtImg('s_' + pic['file'])
    print basics.FmtImg('m_' + pic['file'])
    print basics.FmtImg('orig/' + pic['file'])



def ProjectEditor(proj):
    cols = ['Display', 'Name', 'Description', 'Thumbnail', 'Controls']
    dbi = db.db(basics.cgibin)
    pics = dbi.select("picture", ['id', 'name', 'description', 'alttext', 'display', 'credit', 'file', 'flags'], "groupid=%s" % proj, "display")
    proj = dbi.select("project", ['id', 'name', 'description', 'alttext', 'display', 'flags', 'image', 'groupid'], "id=%s" % proj)[0]
    cats = dbi.select("category", ['id', 'name', 'description', 'alttext', 'display', 'flags'])
    for cat in cats:
	if cat['id'] == proj['groupid']:
	    break
    print '<div class="header">project editor</div>'
    print '<div class="righty">'
    print '<a href="logout.cgi">%s</a>' % basics.FmtButton('log out')
    print '</div>'
    print '<form action="gedit.cgi"><input type="hidden" name="edit" value="proj"><input type="hidden" name="proj" value="%s">' % proj['id']
    print basics.FormatTableStart()
    print basics.FormatRowStart()
    print basics.FormatCell(1, 'Category', hdr=True)
    print basics.FormatCell(1, cat['name'])
    print basics.FormatRowEnd()
    print basics.FormatRowStart()
    print basics.FormatCell(1, 'Project Name', hdr=True)
    print basics.FormatCell(1, '<input type="text" size=80 maxlength=80 name="name_proj.%s" value="%s">' % (proj['id'], basics.Literal(proj['name'])))
    print basics.FormatRowEnd()
    print basics.FormatRowStart()
    print basics.FormatCell(1, 'Description', hdr=True)
    print basics.FormatCell(1, '<textarea cols=80 rows=8 wrap="soft" name="desc_proj.%s">%s</textarea>' % (proj['id'], basics.Literal(proj['description'])))
    print basics.FormatRowEnd()
    print basics.FormatRowStart()
    print basics.FormatCell(1, 'Alt Text', hdr=True)
    print basics.FormatCell(1, '<input type="text" size=80 maxlength=80 name="alttext_proj.%s" value="%s">' % (proj['id'], basics.Literal(proj['alttext'])))
    print basics.FormatRowEnd()
    print basics.FormatRowStart()
    print basics.FormatCell(1, 'Picture not linked', hdr=True)
    print basics.FormatCell(1, '<input type=checkbox name="unlinked_proj.%s" value="1" %s>' % (proj['id'], checked(proj['flags'] & flag_unlink)))
    print basics.FormatRowEnd()
    print basics.FormatRowStart()
    print basics.FormatCell(1, 'Picture before text', hdr=True)
    print basics.FormatCell(1, '<input type=checkbox name="centered_proj.%s" value="1" %s>' % (proj['id'], checked(proj['flags'] & flag_center)))
    print basics.FormatRowEnd()
    #print basics.FormatRowStart()
    #print basics.FormatCell(1, 'External link', hdr=True)
    #print basics.FormatCell(1, '<input type=checkbox name="extlinked_proj.%s" value="1" %s>' % (proj['id'], checked(proj['flags'] & flag_link)))
    #print basics.FormatRowEnd()
    if basics.IsAllowed('m'):
	print basics.FormatRowStart()
	print basics.FormatCell(1, 'Move to', hdr=True)
	cell = '<select name="move_proj.%s"><option value="-1" selected> </option>' % proj['id']
	for c in cats:
	    cell += '<option value="%(id)s">%(name)s</option>' % c
	cell += '</select>'
	print basics.FormatCell(1, cell)
    print basics.FormatRowEnd()
    print basics.FormatTableEnd()
    if basics.IsAllowed('m'):
	print '<div class="lefty"><input type="image" name="submit" src="../art/but_save_changes.gif" class="img"></div>'
    print '<div class="righty"><a href="gedit.cgi?cat=%s">%s</a></div>' % (cat['id'], basics.FmtButton('project list'))
    print basics.FormatTableStart()
    print basics.FormatRowStart()
    icol = 0
    for col in cols:
	print basics.FormatCell(icol, col, hdr=True)
	icol += 1
    print basics.FormatRowEnd()
    for pic in pics:
	print basics.FormatRowStart()
	#print basics.FormatCell(0, '<input type=checkbox name="disp.%s" %s>' % (pic['id'], checked(pic['flags'] & flag_shown)))
	print basics.FormatCell(0, '<input type=checkbox name="disp.%s" %s><input type=text size=5 name="order.%s" value=%d>' % (pic['id'], checked(pic['flags'] & flag_shown), pic['id'], pic['display'] * 10))
	print basics.FormatCell(1, basics.Literal(pic['name']))
	print basics.FormatCell(1, basics.Literal(pic['description']))
	cell = basics.FmtImg('t_' + pic['file'], also={'align':'middle'})
	if pic['id'] == proj['image']:
	    cell += ' ' + basics.FmtArt('flag.gif', desc='(F)', hspace=3, also={'valign' : 'middle'})
	print basics.FormatCell(2, cell)
	cell = ''
	if basics.IsAllowed('m'):
	    cell += '<a href="gedit.cgi?moveup_pic.%s=1">%s</a> - ' % (pic['id'], basics.FmtButton('move up'))
	    cell += '<a href="gedit.cgi?movedn_pic.%s=1">%s</a> - ' % (pic['id'], basics.FmtButton('move down'))
	    cell += '<a href="gedit.cgi?remove_pic.%s=%s">' % (pic['id'], proj['id']) + basics.FmtButton('delete') + '</a> - '
	    cell += '<a href="gedit.cgi?pic=%s">%s</a>' % (pic['id'], basics.FmtButton('edit'))
	else:
	    cell += '<a href="gedit.cgi?pic=%s">%s</a>' % (pic['id'], basics.FmtButton('inspect'))
	if basics.IsAllowed('m'):
	    cell += '<br><a href="gedit.cgi?flag_pic.%s=%s">%s</a>' % (proj['id'], pic['id'], basics.FmtButton('make project picture'))
	print basics.FormatCell(1, cell)
	print basics.FormatRowEnd()
    print basics.FormatTableEnd()
    print '<div class="lefty">'
    if basics.IsAllowed('u'):
	print '<a href="gedit.cgi?upload.pic=%s">%s</a> - ' % (proj['id'], basics.FmtButton('new picture'))
    print '<a href="../gallery.php?proj=%s">%s</a>' % (proj['id'], basics.FmtButton('view'))
    print '</div>'
    print '</form>'



def CategoryEditor(cat):
    cols = ['Display', 'Name', 'Description', 'Controls']
    dbi = db.db(basics.cgibin)
    projs = dbi.select("project", ['id', 'name', 'description', 'alttext', 'display', 'flags'], "groupid=%s" % cat, order="display")
    cats = dbi.select("category", ['id', 'name', 'description', 'alttext', 'display', 'flags'])
    cat = filter(lambda x: int(x['id']) == int(cat), cats)[0]
#    for proj in projs:
#	proj['count'] = dbi.select("picture", ["count(id)"], "groupid=%s" % proj['id'])[0]['count(id)']
    #projs.sort(lambda x,y: cmp(x['display'], y['display']))
    print '<div class="header">category editor</div>'
    print '<div class="righty">'
    print '<a href="logout.cgi">%s</a>' % basics.FmtButton('log out')
    print '</div>'
    print '<form action="gedit.cgi"><input type="hidden" name="edit" value="cat"><input type="hidden" name="cat" value="%s">' % cat['id']
    print basics.FormatTableStart()
    print basics.FormatRowStart()
    print basics.FormatCell(1, 'Category Name', hdr=True)
    print basics.FormatCell(1, '<input type="text" size=80 maxlength=80 name="name_cat.%s" value="%s">' % (cat['id'], basics.Literal(cat['name'])))
    print basics.FormatRowEnd()
    print basics.FormatRowStart()
    print basics.FormatCell(1, 'Description', hdr=True)
    print basics.FormatCell(1, '<textarea cols=80 rows=16 wrap="soft" name="desc_cat.%s">%s</textarea>' % (cat['id'], basics.Literal(cat['description'])))
    print basics.FormatRowEnd()
    print basics.FormatRowStart()
    print basics.FormatCell(1, 'Alt Text', hdr=True)
    print basics.FormatCell(1, '<input type="text" size=80 maxlength=80 name="alttext_cat.%s" value="%s">' % (cat['id'], basics.Literal(cat['alttext'])))
    print basics.FormatRowEnd()
    print basics.FormatRowStart()
    print basics.FormatCell(1, 'Picture not linked', hdr=True)
    print basics.FormatCell(1, '<input type=checkbox name="unlinked_cat.%s" value="1" %s>' % (cat['id'], checked(cat['flags'] & flag_unlink)))
    print basics.FormatRowEnd()
    print basics.FormatRowStart()
    print basics.FormatCell(1, 'Picture before text', hdr=True)
    print basics.FormatCell(1, '<input type=checkbox name="centered_cat.%s" value="1" %s>' % (cat['id'], checked(cat['flags'] & flag_center)))
    print basics.FormatRowEnd()
    print basics.FormatRowStart()
    print basics.FormatCell(1, 'External link', hdr=True)
    print basics.FormatCell(1, '<input type=checkbox name="extlinked_cat.%s" value="1" %s>' % (cat['id'], checked(cat['flags'] & flag_link)) + ' (put link target in description)')
    print basics.FormatRowEnd()
    print basics.FormatRowStart()
    print basics.FormatCell(1, 'Link is image', hdr=True)
    print basics.FormatCell(1, '<input type=checkbox name="linkimg_cat.%s" value="1" %s>' % (cat['id'], checked(cat['flags'] & flag_image)))
    print basics.FormatRowEnd()
    print basics.FormatTableEnd()
    if basics.IsAllowed('m'):
	print '<div class="lefty"><input type="image" name="submit" src="../art/but_save_changes.gif" class="img"></div>'
    print '<div class="righty"><a href="gedit.cgi">%s</a></div>' % basics.FmtButton('category list')
    print basics.FormatTableStart()
    print basics.FormatRowStart()
    icol = 0
    for col in cols:
	print basics.FormatCell(icol, col, hdr=True)
	icol += 1
    print basics.FormatRowEnd()
    for proj in projs:
	print basics.FormatRowStart()
	print basics.FormatCell(0, '<input type=checkbox name="disp.%s" %s>' % (proj['id'], checked(proj['flags'] & flag_shown)))
	print basics.FormatCell(1, proj['name'])
	print basics.FormatCell(1, proj['description'])
	cell = ''
	if basics.IsAllowed('m'):
	    cell += '<a href="gedit.cgi?moveup_proj.%s=1">%s</a> - ' % (proj['id'], basics.FmtButton('move up'))
	    cell += '<a href="gedit.cgi?movedn_proj.%s=1">%s</a> - ' % (proj['id'], basics.FmtButton('move down'))
	    cell += '<a href="gedit.cgi?remove_proj.%s=%s">' % (proj['id'], cat['id']) + basics.FmtButton('delete') + '</a> - '
	    cell += '<a href="gedit.cgi?proj=%s">%s</a>' % (proj['id'], basics.FmtButton('edit'))
	else:
	    cell += '<a href="gedit.cgi?proj=%s">%s</a>' % (proj['id'], basics.FmtButton('inspect'))
	print basics.FormatCell(1, cell)
	print basics.FormatRowEnd()
    print basics.FormatTableEnd()
    print '<div class="lefty">'
    if basics.IsAllowed('m'):
	print '<a href="gedit.cgi?create.proj=%s">%s</a> - ' % (cat['id'], basics.FmtButton('create'))
    print '<a href="../gallery.php?cat=%s">%s</a>' % (cat['id'], basics.FmtButton('view'))
    print '</div>'
    print '</form>'



def CategoryList():
    print '<div class="header">category list</div>'
    print '<div class="righty">'
    if basics.IsAllowed('a'):
	print '<a href="user.cgi">%s</a> - ' % basics.FmtButton('user list')
    print '<a href="chpass.cgi">%s</a> - ' % basics.FmtButton('change password')
    print '<a href="logout.cgi">%s</a>' % basics.FmtButton('log out')
    print '</div>'
    cols = ['Display', 'Name', 'Description', 'Controls']
    dbi = db.db(basics.cgibin)
    cats = dbi.select("category", ['id', 'name', 'description', 'alttext', 'display', 'flags'], order="display")
    #cats.sort(lambda x,y: cmp(x['display'], y['display']))
    print '<form action="gedit.cgi"><input type="hidden" name="edit" value="top">'
    print basics.FormatTableStart()
    print basics.FormatRowStart()
    icol = 0
    for col in cols:
	print basics.FormatCell(icol, col, hdr=True)
	icol += 1
    print basics.FormatRowEnd()
    for cat in cats:
	print basics.FormatRowStart()
	print basics.FormatCell(0, '<input type=checkbox name="disp.%s" %s>' % (cat['id'], checked(cat['flags'] & flag_shown)))
	print basics.FormatCell(1, cat['name'])
	print basics.FormatCell(1, cat['description'])
	cell = ''
	if basics.IsAllowed('m'):
	    cell += '<a href="gedit.cgi?moveup_cat.%s=1">%s</a> - ' % (cat['id'], basics.FmtButton('move up'))
	    cell += '<a href="gedit.cgi?movedn_cat.%s=1">%s</a> - ' % (cat['id'], basics.FmtButton('move down'))
	    cell += '<a href="gedit.cgi?remove_cat.%s=1">' % cat['id'] + basics.FmtButton('delete') + '</a> - '
	    cell += '<a href="gedit.cgi?cat=%s">%s</a>' % (cat['id'], basics.FmtButton('edit'))
	else:
	    cell += '<a href="gedit.cgi?cat=%s">%s</a>' % (cat['id'], basics.FmtButton('inspect'))
	print basics.FormatCell(1, cell)
	print basics.FormatRowEnd()
    print basics.FormatTableEnd()
    print '<div class="lefty">'
    if basics.IsAllowed('m'):
	print '<a href="gedit.cgi?create.cat=1">%s</a> - ' % basics.FmtButton('create')
	print '<input type="image" name="submit" src="../art/but_save_changes.gif" class="img"> -'
    if basics.IsAllowed('a'):
	print '<a href="gedit.cgi?trash=1">%s</a> -' % (basics.FmtButton('trash'))
    print '<a href="../index1.php">%s</a>' % (basics.FmtButton('view'))
    print "</form>"


'''
+-------------+-------------+------+-----+---------+----------------+
| Field       | Type        | Null | Key | Default | Extra          |
+-------------+-------------+------+-----+---------+----------------+
| id          | int(11)     |      | PRI | NULL    | auto_increment | TCPP
| groupid     | int(11)     | YES  |     | NULL    |                | T PP
| name        | text        | YES  |     | NULL    |                | TCPP
| description | text        | YES  |     | NULL    |                | TCPP
| alttext     | text        | YES  |     | NULL    |                | TCPP
| credit      | varchar(32) | YES  |     | NULL    |                | T  P
| file        | varchar(80) | YES  |     | NULL    |                | T  P
| display     | int(6)      | YES  |     | NULL    |                |  CPP
| image       | int(11)     | YES  |     | NULL    |                |   P 
| flags       | int(11)     | YES  |     | 0       |                |  CPP
| level       | varchar(12) | YES  |     | NULL    |                | T   
+-------------+-------------+------+-----+---------+----------------+
'''


def Trash():
    if not basics.IsAllowed('a'):
	CategoryList()
	return
    cols = ['ID', 'Level', 'Name', 'Description', 'Alt Text', 'Credit', 'GroupID', 'File', 'Controls']
    print '<div class="header">trash compactor</div>'
    print '<div class="righty">'
    print '<a href="logout.cgi">%s</a>' % basics.FmtButton('log out')
    print '</div>'
    dbi = db.db(basics.cgibin)
    trash = dbi.select('trash')
    print basics.FormatTableStart()
    print basics.FormatRowStart()
    icol = 0
    for col in cols:
	print basics.FormatCell(icol, col, hdr=True)
	icol += 1
    print basics.FormatRowEnd()
    for ent in trash:
	print basics.FormatRowStart()
	print basics.FormatCell(1, str(ent['id']))
	print basics.FormatCell(1, ent['level'])
	print basics.FormatCell(1, ent['name'])
	print basics.FormatCell(1, ent['description'])
	print basics.FormatCell(1, ent['alttext'])
	print basics.FormatCell(1, ent['credit'])
	print basics.FormatCell(1, str(ent['groupid']))
	print basics.FormatCell(1, '<a href="../gallery/trash/%s">%s</a>' % (ent['file'], ent['file']))
	cell = ''
	cell += '<a href="gedit.cgi?trash_delete=%s">%s</a> -' % (ent['id'], basics.FmtButton('delete'))
	cell += '<a href="gedit.cgi?trash_restore=%s">%s</a>' % (ent['id'], basics.FmtButton('restore'))
	print basics.FormatCell(1, cell)
	print basics.FormatRowEnd()
    print basics.FormatTableEnd()
    print '<div class="lefty"><a href="gedit.cgi?trash_empty=1">%s</a>' % basics.FmtButton('delete all')
    print '<a href="gedit.cgi?trash_restore_all=1">%s</a></div>' % (basics.FmtButton('restore_all'))
    print '<div class="righty"><a href="gedit.cgi">%s</a></div>' % basics.FmtButton('category list')



def DispUpload():
    if not basics.IsAllowed('u'):
	return
    print '<div class="header">file uploader</div>'
    dbi = db.db(basics.cgibin)
    proj = basics.form['upload.pic']
    proj = dbi.select('project', ['id', 'name', 'groupid'], 'id=%s' % proj)[0]
    cat = dbi.select('category', ['id', 'name'], 'id=%s' % proj['groupid'])[0]
    print '<form action="gedit.cgi" enctype="multipart/form-data" method="post">'
    print basics.FormatTableStart()
    print basics.FormatRowStart()
    print basics.FormatCell(1, 'Category', hdr=True)
    print basics.FormatCell(1, cat['name'])
    print basics.FormatRowEnd()
    print basics.FormatRowStart()
    print basics.FormatCell(1, 'Project', hdr=True)
    print basics.FormatCell(1, proj['name'])
    print basics.FormatRowEnd()
    print basics.FormatRowStart()
    print basics.FormatCell(1, 'Name', hdr=True)
    print basics.FormatCell(1, '<input type="text" size=80 maxlength=80 name="name">')
    print basics.FormatRowEnd()
    print basics.FormatRowStart()
    print basics.FormatCell(1, 'Description', hdr=True)
    print basics.FormatCell(1, '<textarea cols=80 rows=8 wrap="soft" name="desc"></textarea>')
    print basics.FormatRowEnd()
    print basics.FormatRowStart()
    print basics.FormatCell(1, 'Credit', hdr=True)
    print basics.FormatCell(1, '<input type="text" size=32 maxlength=32 name="credit">')
    print basics.FormatRowEnd()
    print basics.FormatRowStart()
    print basics.FormatCell(1, 'File to Upload', hdr=True)
    print basics.FormatCell(1, '<input type="file" name="upload_file" size="40">')
    print basics.FormatRowEnd()
    print basics.FormatRowStart()
    print basics.FormatCell(1, '- or -', hdr=True)
    print basics.FormatCell(1, '&nbsp')
    print basics.FormatRowEnd()
    print basics.FormatRowStart()
    print basics.FormatCell(1, 'File to Scrape', hdr=True)
    print basics.FormatCell(1, '<input type="text" name="scrape_file" size="80" maxlength="255"> (url)')
    print basics.FormatRowEnd()
    print basics.FormatTableEnd()
    print '<input type="image" name="submit" src="../art/but_upload_file.gif" class="img">'
    print '<input type="hidden" name="upload_to" value="%s">' % proj['id']
    print '</form>'



def Upload(dbi):
    if not basics.IsAllowed('u'):
	return
    inname = basics.cgiform['upload_file'].filename
    if not inname:
	return
    if not (inname.lower().endswith('.jpg') or inname.lower().endswith('.jpeg')):
	print '<span class="warning">%s isn\'t a JPG or JPEG file!</span>  Call me if you want to use other file types.<p>' % inname
	return
    infile = basics.cgiform['upload_file'].file
    pth = 'gallery/orig/'
    if os.path.exists(pth + inname):
	iadd = 1
	root, ext = basics.RootExt(inname)
	while os.path.exists(pth + root + str(iadd) + '.' + ext):
	    iadd += 1
	inname = root + str(iadd) + '.' + ext
    open(pth + inname, 'w').write(infile.read())
    res = dbi.select('picture', ['max(display)'])[0]['max(display)']
    dbi.insert('picture', {'display' : int(res) + 1, 'flags' : 0, 'groupid' : basics.form['upload_to'], 'file' : inname, 'name' : basics.form.get('name', ''), 'description' : basics.form.get('desc', ''), 'credit' : basics.form.get('credit', ''), 'alttext' : basics.form.get('alttext', '')})
    basics.form['proj'] = basics.form['upload_to']
    SmallerizePic(pth, inname)
    Log('upload ' + inname)



def Scrape(dbi):
    if not basics.IsAllowed('u'):
	return
    url = basics.form['scrape_file']
    if not url:
	return
    if not (url.lower().endswith('.jpg') or url.lower().endswith('.jpeg')):
	print '<span class="warning">%s isn\'t a JPG or JPEG file!</span>  Call me if you want to use other file types.<p>' % url
	return
    infile = urllib2.urlopen(url).read()
    inname = url[url.rfind('/') + 1:]

    pth = 'gallery/orig/'
    if os.path.exists(pth + inname):
	iadd = 1
	root, ext = basics.RootExt(inname)
	while os.path.exists(pth + root + str(iadd) + '.' + ext):
	    iadd += 1
	inname = root + str(iadd) + '.' + ext
    open(pth + inname, 'w').write(infile)
    res = dbi.select('picture', ['max(display)'])[0]['max(display)']
    dbi.insert('picture', {'display' : int(res) + 1, 'flags' : 0, 'groupid' : basics.form['upload_to'], 'file' : inname, 'name' : basics.form.get('name', ''), 'description' : basics.form.get('desc', ''), 'credit' : basics.form.get('credit', ''), 'alttext' : basics.form.get('alttext', '')})
    basics.form['proj'] = basics.form['upload_to']
    SmallerizePic(pth, inname)
    Log('upload ' + inname)



def SmallerizePic(pth, inname):
    System('cat "' + pth + inname + '"|jpegtopnm|pamscale -ysize 120|pnmtojpeg > "' + pth + '../t_' + inname + '"')
    System('cat "' + pth + inname + '"|jpegtopnm|pamscale -ysize 240|pnmtojpeg > "' + pth + '../s_' + inname + '"')
    System('cat "' + pth + inname + '"|jpegtopnm|pamscale -ysize 480|pnmtojpeg > "' + pth + '../m_' + inname + '"')


if __name__ == '__main__':
    os.environ['PATH'] += ':/usr/local/bin'
    basics.artdir = 'art'
    basics.picdir = 'gallery'
    basics.ReadForm()
    print basics.FormatHtml()
    if not basics.IsAllowed('v'):
	print '<meta http-equiv="refresh" content="0;url=login.cgi?dest=gedit.cgi">'
	sys.exit(0)
    print '<!--', basics.GetCookies(), '-->'
    print '<!--', os.environ.get('HTTP_COOKIE'), '-->'
    print '<!-- Pre', basics.form, '-->'
    basics.pagetitle = basics.title = 'Gallery Editor'
    print basics.FormatHead(stylelist=Styles())

    ProcessForm()
    print '<!-- Post', basics.form, '-->'

    if basics.form.get('upload.pic'):
	DispUpload()
    elif basics.form.get('pic'):
	PictureEditor(int(basics.form['pic']))
    elif basics.form.get('proj'):
	ProjectEditor(int(basics.form['proj']))
    elif basics.form.get('cat'):
	CategoryEditor(int(basics.form['cat']))
    elif basics.form.get('trash'):
	Trash()
    else:
	CategoryList()

    print '<!--', basics.form, '-->'
    print basics.FormatTail()
