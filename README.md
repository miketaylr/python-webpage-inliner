# urlgrep

A webpage inliner in Python

This script works by checking what external CSS and JS resources (css, javascript)
a webpage references, downloads and inlines them, using [Google's Gumbo HTML5 parser](https://github.com/google/gumbo-parser).

The result is printed to STDOUT, at which point it's trivial to pipe into grep (or whatever) for interesting patterns over a page.

It could possibly do more interesting things in the future:

TODO: ability to beautify (i.e., un-minify) CSS. (is this WIP? https://github.com/einars/js-beautify/tree/master/python/cssbeautifier)

## Getting this to work
0) `git clone git@github.com:miketaylr/urlgrep.git && cd urlgrep`

1) Install dependencies, grab Gumbo submodule
* `pip install -r requirements.txt`
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

## License

<p xmlns:dct="http://purl.org/dc/terms/" xmlns:vcard="http://www.w3.org/2001/vcard-rdf/3.0#">
  <a rel="license"
     href="http://creativecommons.org/publicdomain/zero/1.0/">
    <img src="http://i.creativecommons.org/p/zero/1.0/88x31.png" style="border-style: none;" alt="CC0" />
  </a>
  <br />
  To the extent possible under law,
  <a rel="dct:publisher"
     href="https://github.com/miketaylr/urlgrep">
    <span property="dct:title">Mike Taylor</span></a>
  has waived all copyright and related or neighboring rights to
  <span property="dct:title">urlgrep</span>.
This work is published from:
<span property="vcard:Country" datatype="dct:ISO3166"
      content="US" about="https://github.com/miketaylr/urlgrep">
  United States</span>.
</p>
