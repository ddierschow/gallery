#!/usr/local/bin/python

import cgitb; cgitb.enable()
import os
import basics
import CryptCookie


if __name__ == '__main__':
    cookie = CryptCookie.ClearCookie({'id' : ''})
    print basics.FormatHtml(cookie)
    basics.ReadForm({})
    CryptCookie.keypath = basics.cgibin
    print '<meta http-equiv="refresh" content="0;url=%s>' % basics.form.get('dest', '../')
    #print '<meta http-equiv="refresh" content="0;url=%s>' % 'test.cgi'
