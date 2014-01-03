require 'sinatra'

get '/' do
	"Hi!"
end

get '/:name' do
	name = params[:name]
	"Hi there #{name}!"
end

get '/discount' do
	markdown :intro
end