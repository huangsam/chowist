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
    return @data if @data
    db = get_connection
    coll = db.collection("places")
    cursor = coll.find()
    @data = JSON.pretty_generate(cursor.to_a)
    @data
end

post '/places' do
    doc = JSON.parse(request.body.read)
    db = get_connection
    coll = db.collection("places")
    coll.insert(doc)
    "The object you added was successfully created."
end

get '/places/:time' do
    content_type :json
    db = get_connection
    coll = db.collection("places")
    cursor = coll.find("minutes" => {"$lte" => params[:time].to_i})
    JSON.pretty_generate(cursor.to_a)
end

__END__
