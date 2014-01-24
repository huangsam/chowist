require 'haml'
require 'json'
require 'mongo'
require 'newrelic_rpm'
require 'sinatra/base'
require 'uri'

include Mongo

module Website

  class Api < Sinatra::Base
    helpers do
        def get_connection
            return @db_connection if @db_connection
            #db = URI.parse(ENV['MONGOHQ_URL'])
            db = URI.parse("mongodb://test:mongohq@paulo.mongohq.com:10016/app19845046")
            db_name = db.path.gsub(/^\//, '')
            @db_connection = Mongo::Connection.new(db.host, db.port).db(db_name)
            @db_connection.authenticate(db.user, db.password) unless (db.user.nil? || db.user.nil?)
            @db_connection
        end
    end

    configure do
        set :static, true
        set :public_folder, "public"
        set :views, "views"
    end

    not_found { haml :notfound }

    get '/places' do
        content_type :json
        db = get_connection

        time = params[:time]
        max = params[:max]
        min = params[:min]
        rating = params[:rating]

        query = {}

        if time then query["minutes"] = { "$lte" => time.to_i } end
        if max then query["maxparty"] = { "$lte" => max.to_i } end
        if min then query["minparty"] = { "$gte" => min.to_i } end
        if rating then query["rating"] = { "$gte" => min.to_i } end

        coll = db.collection("places")
        cursor = coll.find(query)
        JSON.pretty_generate(cursor.to_a)
    end

  end

end
