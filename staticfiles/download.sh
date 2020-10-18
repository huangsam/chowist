#!/bin/bash

CLOUDFLARE_BASE="https://cdnjs.cloudflare.com/ajax/libs"

# Download jQuery
JQUERY_VERSION="3.5.1"
JQUERY_JS="jquery.slim.min.js"
curl -L "$CLOUDFLARE_BASE/jquery/$JQUERY_VERSION/$JQUERY_JS" -o "./js/$JQUERY_JS"

# Download Bootstrap CSS and JS
BS_VERSION="4.5.3"
BS_JS="bootstrap.min.js"
BS_CSS="bootstrap.min.css"
curl -L "$CLOUDFLARE_BASE/twitter-bootstrap/$BS_VERSION/js/$BS_JS" -o "./js/$BS_JS"
curl -L "$CLOUDFLARE_BASE/twitter-bootstrap/$BS_VERSION/css/$BS_CSS" -o "./css/$BS_CSS"

# Download Popper.js
POPPER_VERSION="1.16.1"
POPPER_JS="popper.min.js"
curl -L "$CLOUDFLARE_BASE/popper.js/$POPPER_VERSION/umd/$POPPER_JS" -o "./js/$POPPER_JS"
