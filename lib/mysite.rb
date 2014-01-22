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

  class Protected < Sinatra::Base

    not_found { haml :notfound }
    error { @error = request.env['sinatra_error'] ; haml :error }
    
    def self.new(*)
        app = Rack::Auth::Digest::MD5.new(super) do |username|
          {'cisco' => 'chef2'}[username]
        end
        app.realm = 'Cisco Chefs Only'
        app.opaque = 'secretkey'
        app
    end

    get '/places' do
        content_type :json
        db = get_connection

        time = params[:time]
        max = params[:max]
        min = params[:min]

        query = {}

        if time then query["minutes"] = { "$lte" => time.to_i } end
        if max then query["maxparty"] = { "$lte" => max.to_i } end
        if min then query["minparty"] = { "$gte" => min.to_i } end

        coll = db.collection("places")
        cursor = coll.find(query)
        JSON.pretty_generate(cursor.to_a)
    end

    post '/place' do
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

  end


end
