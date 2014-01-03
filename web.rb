require 'sinatra'
require 'json'

str = File.read('public/restaurants.min.json')
json = JSON.parse(str)

get '/' do
	content_type :json
	json.to_json()
end

get '/:name' do
	content_type :json
	output = ''
	json["places"].map do |key|
		if key["_id"] == params[:name]
			output = key.to_json()
			break
		end
	end
	output
end

__END__
