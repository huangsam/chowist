source "https://rubygems.org"
#ruby '2.0.0'
gem 'bson_ext', '~>1.9'
gem 'haml'
gem 'mongo', '~>1.9'
gem 'sinatra'
gem 'rake'

group :development, :test do
    gem 'foreman', '0.61'
    gem 'rack-test', :require => 'rack/test'
    gem 'rspec'
    gem 'simplecov', '>=0.4.2', :require => false
end

group :production do
    gem 'newrelic_rpm'
end
