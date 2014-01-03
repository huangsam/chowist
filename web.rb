require 'sinatra'
require 'mongo'
require 'uri'
require 'bson_ext'

def get_connection
    return @db_connection if @db_connection
    db = URI.parse(ENV['MONGOHQ_URL'])
    db_name = db.path.gsub(/^\//, '')
    @db_connection = Mongo::Connection.new(db.host, db.port).db(db_name)
    @db_connection.authenticate(db.user, db.password) unless (db.user.nil? || db.user.nil?)
    @db_connection
end
 
db = get_connection

collections = db.collection_names

last_collection = collections[-1]
coll = db.collection(last_collection)

# just show 5
darray = []
docs = coll.find().limit(5)
docs.each{ |doc| darray += doc.to_json }

get '/' do
	darray
end