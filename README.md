ciscochef
=========

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

So far, I have tested on both Ruby 1.9 and 2.0 successfully. Your mileage may vary when using anything less than 1.9.

### System dependencies

[RailsInstaller](http://railsinstaller.com/) is a good place to start if you're missing something.

### Configuration

MongoDB is currently configured in a janky-way. Feel free to improve upon the design. I haven't found many good ways to do imports/exports for `:development`, `:test` and `:production`. Therefore, I'm forced to use the external port for Heroku - YUCK!

### How to run the test suite

`bundle exec rspec spec` should have a complete test suite that runs successfully.

### Deployment instructions

`rails s` should do the trick! If you want to use [foreman](https://github.com/ddollar/foreman), feel free to do `foreman start` instead.