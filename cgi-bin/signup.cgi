#!/usr/local/bin/python

import cgitb; cgitb.enable()
import os
import basics
import CryptCookie

#os.environ['SERVER_NAME'] = 'www.sportscar-craftsmen.com'

def PrintForm():
    print basics.FormatHead()
    print 'You are registering to receive an account on this system.'
    print '<form method="post">'
    print '<table><tr><td>'
    print 'Name:</td><td>'
    print '<input type="text" name="n"></td></tr>'
    print '<tr><td>'
    print 'Password:</td><td>'
    print '<input type="password" name="p"></td></tr>'
    print '<tr><td>'
    print 'Retry password:</td><td>'
    print '<input type="password" name="p2"></td></tr>'
    print '<tr><td>'
    print 'EMail:</td><td>'
    print '<input type="text" name="e" size=60></td></tr>'
    print '<tr><td></td><td>'
    print '<input type="image" name="submit" src="../gfx/but_register.gif" class="img"></td></tr>'
    print '</table>'
    print '<input type="hidden" name="dest" value="%s">' % basics.form.get('dest', 'test.cgi')
    print '</form>'
    print basics.FormatTail()


def Create():
    os.environ['PYTHON_EGG_CACHE'] = '/var/tmp'
    n = basics.form.get('n')
    p = basics.form.get('p')
    p2 = basics.form.get('p2')
    e = basics.form.get('e')
    if not n or not p or p != p2 or not e:
	print basics.FormatHtml()
	PrintForm()
	return

    id = None
    import db
    db = db.db(basics.cgibin)
    id = db.createuser(n, p, e)
    if id:
	cookie = CryptCookie.MakeCookie({'id' : str(id) + ';' + os.environ['REMOTE_ADDR']}, expires=7 * 24 * 60 * 60)
	print basics.FormatHtml(cookie)
	print '<meta http-equiv="refresh" content="0;url=%s>' % basics.form.get('dest', 'test.cgi')
    else:
	cookie = CryptCookie.CryptCookie()
	cookie['id'] = None
	print basics.FormatHtml()
	PrintForm()
	#print basics.FormatHtml(cookie)


if __name__ == '__main__':
    form = basics.ReadForm()
    if basics.form.get('n'):
	Create()
    else:
	print basics.FormatHtml()
	PrintForm()
