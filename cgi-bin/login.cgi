#!/usr/local/bin/python

import cgitb; cgitb.enable()
import os
import basics
import CryptCookie

#os.environ['SERVER_NAME'] = 'www.sportscar-craftsmen.com'

def PrintForm():
    print basics.FormatHead()
    print 'Please log in.'
    print '<form method="post">'
    print '<table><tr><td>'
    print 'Name:</td><td>'
    print '<input type="text" name="n"></td></tr>'
    print '<tr><td>'
    print 'Password:</td><td>'
    print '<input type="password" name="p"></td></tr>'
    print '<tr><td></td><td>'
    print '<input type="image" name="submit" src="../%s/but_log_in.gif" class="img"></td></tr>' % basics.artdir
    print '</table>'
    #print '<input type="hidden" name="dest" value="%s">' % basics.form.get('dest', 'test.cgi')
    print '</form>'
    print '<p><a href="signup.cgi?dest=%s">%s</a>' % (basics.form.get('dest', 'test.cgi'), basics.FmtButton('register'))
    print basics.FormatTail()


def Login():
    id = None
    import db
    db = db.db(basics.cgibin)
    id, privs = db.login(basics.form['n'], basics.form['p'])
    if id:
	cookie = CryptCookie.MakeCookie({'id' : str(id) + ';' + os.environ['REMOTE_ADDR'] + ';' + privs}, expires=7 * 24 * 60 * 60)
	print basics.FormatHtml(cookie)
	print '<meta http-equiv="refresh" content="1;url=%s">' % basics.form.get('dest', 'test.cgi')
	#print cookie
    else:
	#cookie = CryptCookie.MakeCookie({'id' : None}, -1)
	print basics.FormatHtml()
	PrintForm()


if __name__ == '__main__':
    form = basics.ReadForm()
    if basics.form.get('n'):
	Login()
    else:
	print basics.FormatHtml()
	PrintForm()
