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

    not_found { slim :notfound }

    get '/' do
        slim :index
    end

    get '/map' do
        erb :map
    end

  end

end
