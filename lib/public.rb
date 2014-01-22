require 'haml'
require 'json'
require 'mongo'
require 'newrelic_rpm'
require 'sinatra/base'
require 'uri'

include Mongo

def get_connection
    return @db_connection if @db_connection
    #db = URI.parse(ENV['MONGOHQ_URL'])
    db = URI.parse("mongodb://test:mongohq@paulo.mongohq.com:10016/app19845046")
    db_name = db.path.gsub(/^\//, '')
    @db_connection = Mongo::Connection.new(db.host, db.port).db(db_name)
    @db_connection.authenticate(db.user, db.password) unless (db.user.nil? || db.user.nil?)
    @db_connection
end

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
