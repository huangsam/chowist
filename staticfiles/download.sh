#!/bin/bash

CLOUDFLARE_BASE="https://cdnjs.cloudflare.com/ajax/libs"

# Download Bootstrap CSS and JS
BS_VERSION="5.2.3"
BS_JS="bootstrap.min.js"
BS_JS_MAP="$BS_JS.map"
BS_CSS="bootstrap.min.css"
BS_CSS_MAP="$BS_CSS.map"
curl -L "$CLOUDFLARE_BASE/twitter-bootstrap/$BS_VERSION/js/$BS_JS" -o "./js/$BS_JS"
curl -L "$CLOUDFLARE_BASE/twitter-bootstrap/$BS_VERSION/js/$BS_JS_MAP" -o "./js/$BS_JS_MAP"
curl -L "$CLOUDFLARE_BASE/twitter-bootstrap/$BS_VERSION/css/$BS_CSS" -o "./css/$BS_CSS"
curl -L "$CLOUDFLARE_BASE/twitter-bootstrap/$BS_VERSION/css/$BS_CSS_MAP" -o "./css/$BS_CSS_MAP"
