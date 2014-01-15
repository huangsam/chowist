require 'sinatra'
require 'json'
require 'haml'

get '/' do
	haml :index
end

get '/places' do
	content_type :json
	File.read('public/restaurants.min.json')
end

get '/places/:id' do
	content_type :json
	str = File.read('public/restaurants.min.json')
	json = JSON.parse(str)
	output = ''
	json["places"].map do |key|
		if key["_id"] == params[:id].to_i
			output = key.to_json()
			break
		end
	end
	output
end

__END__
