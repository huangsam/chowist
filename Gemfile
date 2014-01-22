source "https://rubygems.org"
gem 'bson_ext', '~>1.9'
gem 'haml'
gem 'slim'
gem 'mongo', '~>1.9'
gem 'sinatra'
gem 'rake'

group :development, :test do
    gem 'coveralls', require: false
    gem 'foreman', '0.61'
    gem 'rack-test', :require => 'rack/test'
    gem 'rspec'
    gem 'rspec-core'
end

group :production do
    gem 'newrelic_rpm'
end
