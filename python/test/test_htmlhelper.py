# -*- coding: utf-8 -*-

###
### $Release: $
### $Copyright: copyright(c) 2007-2011 kuwata-lab.com all rights reserved. $
###

from oktest import ok, not_ok, run
import sys, os, re

from testcase_helper import *
import tenjin
from tenjin.helpers import escape, to_str, EscapedStr, EscapedUnicode, mark_as_escaped


class HtmlHelperTest(object):

    def test_tagattr(self):
        tagattr = tenjin.helpers.html.tagattr
        ok (tagattr('size', 20))           == ' size="20"'
        ok (tagattr('size', 0))            == ' size="0"'
        ok (tagattr('size', ''))           == ''
        ok (tagattr('size', 20, 'large'))  == ' size="large"'
        ok (tagattr('size',  0, 'zero'))   == ' size="zero"'
        ok (tagattr('size', '', 'empty'))  == ''
        ok (tagattr('title', '<>&"'))      == ' title="&lt;&gt;&amp;&quot;"'
        ok (tagattr('title', '<>&"', escape=False)) == ' title="<>&""'
        #
        ok (tagattr('size', 20)).is_a(EscapedStr)
        ok (tagattr('size', '')).is_a(EscapedStr)

    def test_tagattrs(self):
        tagattrs = tenjin.helpers.html.tagattrs
        ok (tagattrs(src="img.png", size=20)) == ' src="img.png" size="20"'
        ok (tagattrs(src='', size=0))         == ' size="0"'
        ok (tagattrs(klass='error'))          == ' class="error"'    # klass='error' => class="error"
        ok (tagattrs(checked='Y'))            == ' checked="checked"'
        ok (tagattrs(selected=1))             == ' selected="selected"'
        ok (tagattrs(disabled=True))          == ' disabled="disabled"'
        ok (tagattrs(checked='', selected=0, disabled=None)) == ''
        #
        ok (tagattrs(size=20)).is_a(EscapedStr)
        ok (tagattrs(size=None)).is_a(EscapedStr)
        #
        ok (tagattrs(name="<foo>"))    == ' name="&lt;foo&gt;"'
        ok (tagattrs(name=u"<foo>"))   == ' name="&lt;foo&gt;"'
        ok (tagattrs(name=mark_as_escaped("<foo>")))  == ' name="<foo>"'
        ok (tagattrs(name=mark_as_escaped(u"<foo>"))) == ' name="<foo>"'

    def test_checked(self):
        checked = tenjin.helpers.html.checked
        ok (checked(1==1)) == ' checked="checked"'
        ok (checked(1==0)) == ''
        #
        ok (checked(1==1)).is_a(EscapedStr)
        ok (checked(1==0)).is_a(EscapedStr)

    def test_selected(self):
        selected = tenjin.helpers.html.selected
        ok (selected(1==1)) == ' selected="selected"'
        ok (selected(1==0)) == ''
        #
        ok (selected(1==1)).is_a(EscapedStr)
        ok (selected(1==0)).is_a(EscapedStr)

    def test_disabled(self):
        disabled = tenjin.helpers.html.disabled
        ok (disabled(1==1)) == ' disabled="disabled"'
        ok (disabled(1==0)) == ''
        #
        ok (disabled(1==1)).is_a(EscapedStr)
        ok (disabled(1==0)).is_a(EscapedStr)

    def test_nl2br(self):
        nl2br = tenjin.helpers.html.nl2br
        s = """foo\nbar\nbaz\n"""
        ok (nl2br(s)) == "foo<br />\nbar<br />\nbaz<br />\n"
        #
        ok (nl2br(s)).is_a(EscapedStr)

    def test_text2html(self):
        text2html = tenjin.helpers.html.text2html
        s = """FOO\n    BAR\nBA     Z\n"""
        expected = "FOO<br />\n &nbsp; &nbsp;BAR<br />\nBA &nbsp; &nbsp; Z<br />\n"
        ok (text2html(s)) == expected
        expected = "FOO<br />\n    BAR<br />\nBA     Z<br />\n"
        ok (text2html(s, False)) == expected
        #
        ok (text2html(s)).is_a(EscapedStr)

    def test_nv(self):
        nv = tenjin.helpers.html.nv
        ok (nv('rank', 'A'))       == 'name="rank" value="A"'
        ok (nv('rank', 'A', '.'))  == 'name="rank" value="A" id="rank.A"'
        ok (nv('rank', 'A', klass='error')) == 'name="rank" value="A" class="error"'
        ok (nv('rank', 'A', checked=True))  == 'name="rank" value="A" checked="checked"'
        ok (nv('rank', 'A', disabled=10))   == 'name="rank" value="A" disabled="disabled"'
        ok (nv('rank', 'A', style="color:red")) == 'name="rank" value="A" style="color:red"'
        #
        ok (nv('rank', 'A')).is_a(EscapedStr)
        #
        ok (nv(u"名前", u"なまえ")) == u'name="名前" value="なまえ"'
        ok (nv(u"名前", u"なまえ")).is_a(EscapedUnicode)

    def test_new_cycle(self):
        cycle = tenjin.helpers.html.new_cycle('odd', 'even')
        ok (cycle())  == 'odd'
        ok (cycle())  == 'even'
        ok (cycle())  == 'odd'
        ok (cycle())  == 'even'
        #
        cycle = tenjin.helpers.html.new_cycle('A', 'B', 'C')
        ok (cycle()) == 'A'
        ok (cycle()) == 'B'
        ok (cycle()) == 'C'
        ok (cycle()) == 'A'
        ok (cycle()) == 'B'
        ok (cycle()) == 'C'
        #
        #ok (cycle()).is_a(EscapedStr)
        #ok (cycle()).is_a(EscapedStr)


if __name__ == '__main__':
    run()
