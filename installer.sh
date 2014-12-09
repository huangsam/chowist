#!/bin/bash

# Enable sudo-less Docker
sudo gpasswd -a vagrant docker
sudo service docker restart

# Install pip and Docker packages
curl -sSL https://bootstrap.pypa.io/get-pip.py | sudo python
pip install docker-py fig

# Install ciscochef dependencies
sudo apt-get install -y nodejs ruby1.9.1-dev g++
sudo gem install bundle
cd ciscochef && bundle install
