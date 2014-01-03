require 'sinatra'

get '/' do
	content_type :json
	File.read('public/restaurants.min.json')
end