source "https://rubygems.org"
gem 'bson_ext'
gem 'haml'
gem 'mongo'
gem 'sinatra', '>=1.2.0'
gem 'rake'

group :development, :test do
    gem 'coveralls', require: false
    gem 'foreman', '0.61'
    gem 'rack-test', :require => 'rack/test'
    gem 'rspec'
    gem 'rspec-core'
end

group :production do
    gem 'newrelic_rpm', '>=3.7.1.188'
end
