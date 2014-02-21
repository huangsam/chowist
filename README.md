ciscochef
=========

[![Build Status](https://travis-ci.org/huangsam/ciscochef.png?branch=master)](https://travis-ci.org/huangsam/ciscochef) [![Dependency Status](https://gemnasium.com/huangsam/ciscochef.png)](https://gemnasium.com/huangsam/ciscochef) [![Coverage Status](https://coveralls.io/repos/huangsam/ciscochef/badge.png?branch=master)](https://coveralls.io/r/huangsam/ciscochef?branch=master)

<pre>
 __                __        _
/   o  _  _  _    /  |_  _ _|_
\__ | _> (_ (_)   \__| |(/_ | 

http://www.patorjk.com/software/taag
</pre>

This is a [web application](http://ciscochef.herokuapp.com/) that
shows a dynamically created map of places that my Cisco coworkers
and I have deemed worthy of eating at around the San Jose campus.
It's responsive, meaning that it will look great on computers,
smartphones and tablets. This map will benefit not only employees
at Cisco, but also people around the Bay Area.

[Click here](https://github.com/huangsam/ciscochef/wiki) to check out the project wiki!

### Ruby version

So far, I have tested the app on both Ruby 1.9.3, 2.0.0 and 2.1.0
successfully. Your mileage may vary when using otherwise.

### System dependencies

[RailsInstaller](http://railsinstaller.com/) is a good place to start
if you're missing something.

### Configuration

Configuration to deal with Heroku's MongoHQ platform is the following:
`url = ENV['MONGOHQ_URL'] || 'mongodb://127.0.0.1:27017/ciscochef'`

Since I did not deploy a Mongo ORM like `mongoid` yet, the implication
is that you will need to execute
`mongoimport --db ciscochef --collection places --file test.json --jsonArray`
in an existing mongo server process on your computer. To
learn more about MongoDB, [click here](http://docs.mongodb.org/manual/) for
documentation.

### How to run the test suite

`bundle exec rspec spec` should have a complete test suite that runs successfully
on the environment of your choice, given that you have already done the necessary
import of JSON data.

### Deployment instructions

`bundle install` should get all the necessary dependencies. Do not
include `Gemfile.lock` when you push on Windows - it will cause Travis CI
to fail as mentioned
[here](http://stackoverflow.com/questions/3642085/make-bundler-use-different-gems-for-different-platforms).

`rails s` should do the trick - defaulting the port over to 3000. If you
need a different port, then do `rails s -p ${PORT}`. If you want to use
[foreman](https://github.com/ddollar/foreman), feel free to do
`foreman start` instead. This most closely reflects the production
environment on Heroku. One note for Windows users: make sure to use only
foreman version 0.61, since anything above that particular version
is incompatible with Windows.
