#!/usr/bin/env python

# -*- coding: utf-8 -*-
# vim:tabstop=4:expandtab:sw=4:softtabstop=4

from __future__ import print_function
from BeautifulSoup import Tag
import argparse
import base64
import gumbo
import jsbeautifier
import mimetypes
import re
import requests
import sys
import urlparse

FF25 = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) '
        'Gecko/20100101 Firefox/25.0')


def is_remote(address):
    return urlparse.urlparse(address)[0] in ('http', 'https')


def get_content(from_):
    if is_remote(from_):
        r = requests.get(from_, headers={'User-Agent': FF25})
        return r.content
    else:
        return open(from_).read()


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
    '''Fetch the contents of an external script and write that to an inline
    script element. If the [-b] flag is passed in, the JS will be beautified
    using jsbeautifier.'''
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
            print('failed to load javascript from %s' % js['src'])
            print(e)


def replaceCss(base_url, soup):
    '''Fetch the contents of an external link and write that to an inline
    style element. For now the CSS is left as is, without uncompressing.'''
    for css in soup.findAll('link', {'rel': 'stylesheet',
                                     'href': re.compile('.+')}):
        try:
            real_css = get_content(resolve_path(base_url, css['href']))
            style_tag = Tag(soup, "style")
            style_tag.insert(0, real_css)
            css.replaceWith(style_tag)

        except Exception, e:
            print('failed to load css from %s' % css['href'])
            print(e)


def main(url):
    '''Parse the HTML source with the Gumbo HTML5 parser and inline the CSS and
    JS assets. Results are printed to STDOUT.'''
    soup = gumbo.soup_parse(get_content(url))

    replaceJavascript(url, soup)
    replaceCss(url, soup)

    print(soup, file=sys.stdout)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--beautify', action='store_true',
                        help='Beautify (unminify) the JS')
    parser.add_argument('in_file', help='HTML file to inline')
    args = parser.parse_args()
    main(args.in_file)
