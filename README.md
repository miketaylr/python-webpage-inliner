# urlgrep

A webpage inliner in Python

This script works by checking what external CSS and JS resources (css, javascript)
a webpage references, downloads and inlines them, using [Google's Gumbo HTML5 parser](https://github.com/google/gumbo-parser).

The result is printed to STDOUT, at which point it's trivial to pipe into grep (or whatever) for interesting patterns over a page.

It could possibly do more interesting things in the future:

TODO: ability to beautify (i.e., un-minify) CSS. (is this WIP? https://github.com/einars/js-beautify/tree/master/python/cssbeautifier)

## Getting this to work
0) `git clone git@github.com:miketaylr/urlgrep.git && cd urlgrep`

1) Install dependencies

* `pip install BeautifulSoup` (Gumbo has a BeautifulSoup adapter, which is super easy to work with).
* `pip install feedparser`
* `pip install jsbeautifier`
* `git submodule init && git submodule update`

2) Build Gumbo. See their [README](https://github.com/google/gumbo-parser/blob/master/README.md).

I had to install `libtool`, `automake`, and `autoconf` with `brew` to make this work, FWIW/YMMV/YOLO.

3) Install Gumbo Python bindings
`sudo python setup.py install` (from gumbo dir, but you already knew that because you read the [README](https://github.com/google/gumbo-parser/blob/master/README.md).

## Usage

`python inliner.py http://andyshora.com/promises-angularjs-explained-as-cartoon.html`

This will inline the file as is.

`python inliner.py -b example/index.html`

This will beautify the JavaScript, then inline it.