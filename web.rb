require 'haml'
require 'json'
require 'mongo'
require 'sinatra'
require 'newrelic_rpm'
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

get '/' do
    haml :index
end

get '/map' do
    erb :map
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
    if doc.yelp =~ URI:regexp and doc.lat and doc.long
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

__END__
