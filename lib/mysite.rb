require 'haml'
require 'json'
require 'mongo'
require 'newrelic_rpm'
require 'sinatra/base'
require 'uri'

include Mongo

def get_connection
    return @db_connection if @db_connection
    db = URI.parse(ENV['MONGOHQ_URL'])
    db_name = db.path.gsub(/^\//, '')
    @db_connection = Mongo::Connection.new(db.host, db.port).db(db_name)
    @db_connection.authenticate(db.user, db.password) unless (db.user.nil? || db.user.nil?)
    @db_connection
end

module Website
  class MySite < Sinatra::Base

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

    get '/notfound' do
        haml :notfound
    end

    get '/places' do
        content_type :json
        db = get_connection
        coll = db.collection("places")
        cursor = coll.find()
        JSON.pretty_generate(cursor.to_a)
    end

    post '/places' do
        doc = JSON.parse(request.body.read)
        db = get_connection
        coll = db.collection("places")
        if ["name", "address", "lat", "long"].all? {|s| doc.key? s}
            coll.insert(doc)
            "Object was successfully created."
        else
            "Object was unsuccessful."
        end
    end

    get '/places/:time' do
        content_type :json
        db = get_connection
        coll = db.collection("places")
        cursor = coll.find("minutes" => {"$lte" => params[:time].to_i})
        JSON.pretty_generate(cursor.to_a)
    end

  end
end
