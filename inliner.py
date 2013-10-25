#!/usr/bin/env python

# -*- coding: utf-8 -*-
# vim:tabstop=4:expandtab:sw=4:softtabstop=4

import argparse
import base64
import feedparser
import gumbo
import jsbeautifier
import mimetypes
import re
import sys
import urllib2
import urlparse
from BeautifulSoup import Tag


def is_remote(address):
    return urlparse.urlparse(address)[0] in ('http', 'https')


def ignore_url(address):
    url_blacklist = ('getsatisfaction.com',
                     'google-analytics.com')

    for bli in url_blacklist:
        if address.find(bli) != -1:
            return True

    return False


def get_content(from_, expect_binary=False):
    if is_remote(from_):
        if ignore_url(from_):
            return u''

        ct = urllib2.urlopen(from_)
        if not expect_binary:
            s = ct.read()
            encodings = feedparser.convert_to_utf8(ct.headers, s)
            return unicode(s, encodings[1])
        else:
            return ct.read()
    else:
        s = open(from_).read()
        if not expect_binary:
            encodings = feedparser.convert_to_utf8({}, s)
            return unicode(s, encodings[1])
        else:
            return s


def resolve_path(base, target):
    if True:
        return urlparse.urljoin(base, target)

    if is_remote(target):
        return target

    if target.startswith('/'):
        if is_remote(base):
            protocol, rest = base.split('://')
            return '%s://%s%s' % (protocol, rest.split('/')[0], target)
        else:
            return target
    else:
        try:
            base, rest = base.rsplit('/', 1)
            return '%s/%s' % (base, target)
        except ValueError:
            return target


def replaceJavascript(base_url, soup):
    for js in soup.findAll('script', {'src': re.compile('.+')}):
        try:
            real_js = get_content(resolve_path(base_url, js['src']))
            if args.beautify:
                opts = jsbeautifier.default_options()
                opts.indent_size = 2
                opts.indent_with_tabs = False
                real_js = jsbeautifier.beautify(real_js, opts)
            script_tag = Tag(soup, "script")
            script_tag.insert(0, real_js)
            js.replaceWith(script_tag)
        except Exception, e:
            print 'failed to load javascript from %s' % js['src']
            print e

css_url = re.compile(ur'url\((.+)\)')


def replaceCss(base_url, soup):
    for css in soup.findAll('link', {'rel': 'stylesheet',
                                     'href': re.compile('.+')}):
        try:
            real_css = get_content(resolve_path(base_url, css['href']))
            style_tag = Tag(soup, "style")
            style_tag.insert(0, real_css)
            css.replaceWith(style_tag)

        except Exception, e:
            print 'failed to load css from %s' % css['href']
            print e


def main(url, output_filename):
    soup = gumbo.soup_parse(get_content(url))

    replaceJavascript(url, soup)
    replaceCss(url, soup)

    res = open(output_filename, 'wb')
    print >>res, str(soup)
    res.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--beautify', action='store_true',
                        help='Beautify (unminify) the JS')
    parser.add_argument('in_file', help='HTML file to inline')
    parser.add_argument('out_file', help='output as HTML')
    args = parser.parse_args()
    main(args.in_file, args.out_file)
