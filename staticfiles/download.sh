#!/bin/bash
JQUERY='jquery-3.3.1.slim.min.js'
curl -L "https://code.jquery.com/$JQUERY" -o "./js/$JQUERY"

BS_VERSION='4.1.1'
BS_PREFIX='bootstrap.min'
curl -L "https://stackpath.bootstrapcdn.com/bootstrap/$BS_VERSION/js/$BS_PREFIX.js" -o "./js/$BS_PREFIX.js"
curl -L "https://stackpath.bootstrapcdn.com/bootstrap/$BS_VERSION/css/$BS_PREFIX.css" -o "./css/$BS_PREFIX.css"

POPPER_VERSION='1.14.3'
POPPER='popper.min.js'
curl -L "https://cdnjs.cloudflare.com/ajax/libs/popper.js/$POPPER_VERSION/umd/$POPPER" -o "./js/$POPPER"
