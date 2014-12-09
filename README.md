ciscochef
=========

[![Build Status](https://travis-ci.org/huangsam/ciscochef.png?branch=master)](https://travis-ci.org/huangsam/ciscochef) [![Dependency Status](https://gemnasium.com/huangsam/ciscochef.png)](https://gemnasium.com/huangsam/ciscochef) [![Coverage Status](https://coveralls.io/repos/huangsam/ciscochef/badge.png?branch=master)](https://coveralls.io/r/huangsam/ciscochef?branch=master)

This is a [web application](http://ciscochef.herokuapp.com/) that
shows a dynamically created map of places that Cisco coworkers
have deemed worthy of eating at around the San Jose campus.
It's responsive, meaning that it will look great on computers,
smartphones and tablets. This map will benefit not only employees
at Cisco, but also people around the Bay Area.

[Click here](https://github.com/huangsam/ciscochef/wiki) to check
out the project wiki!

### Ruby version

So far, the app has been tested on Ruby 1.9.3, 2.0.0 and 2.1.0
successfully. Your mileage may vary when using other versions.

### System dependencies

[RailsInstaller](http://railsinstaller.com/) is a good place to start
for Windows users. Mac owners should be fine skipping down to the
Deployment Instructions section.

### Configuration

These are the configuration that are used to connect to the database:

- `MONGOHQ_URL` - MongoHQ add-on from Heroku, standalone variable
- `MONGO_HOST` - Manually injected Mongo IP Address, used with its port counterpart
- `MONGO_PORT` - Manually injected Mongo Port Number
- `CISCOCHEF_DB_1_PORT_27017_TCP_ADDR` - Fig Mongo IP Address, used with its port counterpart
- `CISCOCHEF_DB_1_PORT_27017_TCP_PORT` - FIg Mongo Port Number

A Mongo ORM like `mongoid` has not been deployed yet, so please run
`mongoimport --db ciscochef --collection places --file test.json --jsonArray`
in an existing mongo server process on your computer.

### How to run the test suite

`bundle exec rspec spec` should have a complete test suite that runs
successfully on the environment of your choice, given that you have
finished the data import from above.

### Deployment instructions

#### Local Machine

`bundle install` should get all the necessary dependencies. Do not
include `Gemfile.lock` when you push on Windows - it will cause Travis CI
to fail.

`rails s` should do the trick - defaulting the port over to 3000. If you
need a different port, then do `rails s -p ${PORT}`. Feel free to do
`foreman start` instead, which closely reflects the production
environment on Heroku. Windows users should use foreman v0.61,
since anything above that version is Windows-incompatible.

#### Vagrant Machine

`vagrant up` and `vagrant ssh` should get you into a self-provisioned
machine. Once you are inside, go into the project repository and run
`fig up` or `fig up -d`. Fig will produce a properly working set
of services for running Cisco Chef as a containerized application.
