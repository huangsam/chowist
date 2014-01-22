require 'haml'
require 'newrelic_rpm'
require 'sinatra/base'

module Website

  class Public < Sinatra::Base

    configure do
        set :static, true
        set :public_folder, "public"
        set :views, "views"
    end

    not_found { haml :notfound }

    get '/' do
        haml :index
    end

    get '/map' do
        erb :map
    end

  end

end
