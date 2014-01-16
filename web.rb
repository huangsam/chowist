require 'sinatra'
require 'json'
require 'mongo'
require 'uri'
require 'haml'

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

get '/places' do
    content_type :json
    db = get_connection
    coll = db.collection("places")
    coll.find().each do |row|
        puts row
    end
end

get '/places/:id' do
    content_type :json
    str = File.read('public/restaurants.min.json')
    json = JSON.parse(str)
    output = ''
    json["places"].map do |key|
        if key["_id"] == params[:id].to_i
            output = key.to_json()
            break
        end
    end
    output
end

__END__
