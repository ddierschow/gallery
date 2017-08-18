#!/usr/local/bin/python

import cgitb; cgitb.enable()
import os
import basics
import db
import styles

# todo
#  password clearing - how?
#  acct verification

cols = [('id', 'Id'), ('name', 'User Name'), ('privs', 'Priveleges'), ('state', 'State'), ('email', 'Email Address')]


def Styles():
    sset = styles.StyleSet(['.title', '.table', '.cell', '.hcell', 'img', '.img', '.header', '.warning', '.righty', '.lefty'])
    sset['body']['bgc'] = '#FFCCCC'
    sset['.title']['c'] = '#003300'
    sset['.header'].update({'ta': 'left', 'f': 'left', 'fw': 'bold'})
    sset['.righty']['f'] = 'right'
    sset['.lefty']['f'] = 'left'
    sset['.warning'].update({'fw': 'bold', 'c': '#CC0000'})
    sset['.table'].update({'bgc': '#9999FF', 'clr': 'both', 'bsp': '0px', 'bw': '2px'})
    sset['.hcell']['bgc'] = '#EEEEFF'
    sset['.cell'].update({'ta': 'left', 'va': 'middle', 'bgc': '#EEEEFF'})
    sset['img'].update({'bw': '0', 'va': 'middle'})
    sset['.img'].update({'bw': '0', 'va': 'middle'})
    return sset


def PrintUsers(dbi):
    users = dbi.select('user', ['name', 'id', 'privs', 'state', 'email'])
    print basics.FormatTableStart(also={'border':1})

    print basics.FormatRowStart()
    for col in cols:
	print basics.FormatCell(0, col[1], hdr=True)
    print basics.FormatRowEnd()

    for user in users:
	print basics.FormatRowStart()
	for col in cols:
	    if col[0] == 'name':
		print basics.FormatCell(0, '<a href="user.cgi?id=%s">%s</a>' % (user['id'], user[col[0]]))
	    else:
		print basics.FormatCell(0, user[col[0]])
	print basics.FormatRowEnd()

    print basics.FormatTableEnd()


def PrintForm(dbi, id):
    user = dbi.select('user', ['name', 'id', 'privs', 'state', 'email'], 'id=%s' % id)[0]
    print '<form>'
    print basics.FormatTableStart(also={'border':1})

    for col in cols:
	print basics.FormatRowStart()
	print basics.FormatCell(0, col[1], hdr=True)
	if col[0] == 'id':
	    cell = '<input type="hidden" name="id" value="%s">%s' % (user[col[0]], user[col[0]])
	elif col[0] == 'email':
	    cell = '<input type="text" name="%s" value="%s" size=60>' % (col[0], user[col[0]])
	else:
	    cell = '<input type="text" name="%s" value="%s">' % (col[0], user[col[0]])
	print basics.FormatCell(0, cell)
	print basics.FormatRowEnd()

    print basics.FormatRowStart()
    print basics.FormatCell(0, 'Password', hdr=True)
    cell = '<input type="checkbox" name="%s">' % col[0]
    print basics.FormatCell(0, cell)
    print basics.FormatRowEnd()

    print basics.FormatTableEnd()
    print '<input type="image" name="submit" src="../%s/but_save_changes.gif" class="img"> -' % basics.artdir
    print '<a href="user.cgi?delete=1&id=%s">%s</a>' % (id, basics.FmtButton('delete'))
    print '</form>'


def DeleteUser(dbi, form):
    dbi.remove('user', 'id=%s' % form['id'])


def UpdateUser(dbi, form):
    dbi.update('user', {'email' : form.get('email', ''), 'state' : form.get('state', ''), 'name' : form.get('name', ''), 'privs' : form.get('privs', '')}, "id=%s" % form.get('id', ''))


if __name__ == '__main__':
    basics.artdir = 'gfx'
    print basics.FormatHtml()
    basics.Restrict('a')
    basics.ReadForm()
    print basics.FormatHead(stylelist=Styles())
    dbi = db.db(basics.cgibin)
    if 'name' in basics.form:
	UpdateUser(dbi, basics.form)
	PrintUsers(dbi)
    elif 'delete' in basics.form:
	DeleteUser(dbi, basics.form)
	PrintUsers(dbi)
    elif 'id' in basics.form:
	PrintForm(dbi, basics.form['id'])
    else:
	PrintUsers(dbi)
    print basics.FormatTail()
