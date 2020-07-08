#!/bin/bash

# Download jQuery
JQUERY_VERSION='3.5.1'
JQUERY="jquery-$JQUERY_VERSION.slim.min.js"
curl -L "https://code.jquery.com/$JQUERY" -o './jquery.slim.min.js'

# Download Bootstrap CSS and JS
BS_VERSION='4.5.0'
BS_PREFIX='bootstrap.min'
curl -L "https://stackpath.bootstrapcdn.com/bootstrap/$BS_VERSION/js/$BS_PREFIX.js" -o "./js/$BS_PREFIX.js"
curl -L "https://stackpath.bootstrapcdn.com/bootstrap/$BS_VERSION/css/$BS_PREFIX.css" -o "./css/$BS_PREFIX.css"

# Download Popper.js
POPPER_VERSION='1.16.0'
POPPER='popper.min.js'
curl -L "https://cdnjs.cloudflare.com/ajax/libs/popper.js/$POPPER_VERSION/umd/$POPPER" -o "./js/$POPPER"
