#!/usr/bin/env python

# -*- coding: utf-8 -*-
# vim:tabstop=4:expandtab:sw=4:softtabstop=4

import base64
import feedparser
import gumbo
import mimetypes
import re
import sys
import urllib2
import urlparse


def is_remote(address):
    return urlparse.urlparse(address)[0] in ('http', 'https')


def data_encode_image(name, content):
    return u'data:%s;base64,%s' % (mimetypes.guess_type(name)[0],
                                   base64.standard_b64encode(content))


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
            js.replaceWith(u'<script>%s</script>' % real_js)
        except Exception, e:
            print 'failed to load javascript from %s' % js['src']
            print e

css_url = re.compile(ur'url\((.+)\)')


def replaceCss(base_url, soup):
    for css in soup.findAll('link', {'rel': 'stylesheet',
                                     'href': re.compile('.+')}):
        try:
            real_css = get_content(resolve_path(base_url, css['href']))

            def replacer(result):
                try:
                    path = resolve_path(resolve_path(base_url, css['href']),
                                        result.groups()[0])
                    return u'url(%s)' % data_encode_image(path,
                                                          get_content(path,
                                                                      True))
                except Exception, e:
                    print e
                    return u''

            css.replaceWith(u'<style>%s</style>' % real_css)

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
    main(sys.argv[1], sys.argv[2])
