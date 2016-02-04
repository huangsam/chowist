ruby "2.2.4"
source 'https://rubygems.org'

gem 'rails', '~>4.2.0'

group :development, :test do
  gem 'coveralls', require: false
  gem 'rspec-rails', '~>3.4.0'
  gem 'rack-test'
  gem 'rubocop', require: false
end

group :test do
  gem 'selenium-webdriver'
  gem 'capybara'
end

# Windows compatibility
gem 'tzinfo-data', platforms: [:mingw, :mswin, :x64_mingw]

gem 'sass-rails', '~>5.0.0'
gem 'uglifier', '~>2.7.0'
gem 'coffee-rails', '~>4.1.0'
gem 'jquery-rails'
gem 'turbolinks'
gem 'jbuilder'

gem 'haml'
gem 'json'
gem 'mongo'

gem 'thin'

group :doc do
  gem 'yard', require: false
end

group :production do
  gem 'rails_12factor', '~>0.0.2'
  gem 'newrelic_rpm'
end
