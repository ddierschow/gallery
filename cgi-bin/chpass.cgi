#!/usr/local/bin/python

import cgitb; cgitb.enable()
import os
import basics
import CryptCookie

#os.environ['SERVER_NAME'] = 'www.sportscar-craftsmen.com'

def PrintForm():
    print basics.FormatHead()
    print 'You have requested to change your password.'
    print '<form method="post">'
    print '<table><tr><td>'
    print 'Name:</td><td>'
    print '<input type="text" name="n"></td></tr>'
    print '<tr><td>'
    print 'Old password:</td><td>'
    print '<input type="password" name="op"></td></tr>'
    print '<tr><td>'
    print 'New password:</td><td>'
    print '<input type="password" name="p1"></td></tr>'
    print '<tr><td>'
    print 'Retry new password:</td><td>'
    print '<input type="password" name="p2"></td></tr>'
    print '<tr><td>'
    print 'Change email address:</td><td>'
    print '<input type="text" name="em" size=60></td></tr>'
    print '<tr><td></td><td>'
    print '<input type="image" name="submit" src="../gfx/but_save_changes.gif" class="img"></td></tr>'
    print '</table>'
    print '<input type="hidden" name="dest" value="%s">' % basics.form.get('dest', 'test.cgi')
    print '</form>'
    print basics.FormatTail()


def ChangePass():
    if not basics.form.get('p1') or basics.form.get('p1') != basics.form.get('p2'):
	print basics.FormatHtml()
	PrintForm()
	return

    id = None
    import db
    db = db.db(basics.cgibin)
    id = db.login(basics.form['n'], basics.form['op'])[0]
    if id and basics.form.get('p1') == basics.form.get('p2', -1):
	db.changepassword(id, basics.form.get('p1'))
	db.changeemail(id, basics.form.get('em'))
	cookie = CryptCookie.MakeCookie({'id' : str(id) + ';' + os.environ['REMOTE_ADDR']}, expires=7 * 24 * 60 * 60)
	print basics.FormatHtml(cookie)
	print '<meta http-equiv="refresh" content="0;url=%s>' % basics.form.get('dest', 'test.cgi')
    else:
	cookie = CryptCookie.CryptCookie()
	cookie['id'] = None
	print basics.FormatHtml()
	PrintForm()


if __name__ == '__main__':
    form = basics.ReadForm()
    if basics.form.get('n'):
	ChangePass()
    else:
	print basics.FormatHtml()
	PrintForm()
