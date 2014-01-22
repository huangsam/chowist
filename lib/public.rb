require 'haml'
require 'json'
require 'mongo'
require 'newrelic_rpm'
require 'sinatra/base'
require 'uri'

module Website

  class Public < Sinatra::Base

    configure do
        set :static, true
        set :public_folder, "public"
        set :views, "views"
    end

    not_found { haml :notfound }
    error { @error = request.env['sinatra_error'] ; haml :error }

    get '/' do
        haml :index
    end

    get '/map' do
        erb :map
    end

  end

end
