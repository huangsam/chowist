# This class is the controller for the entire Application. It
# uses a primitive form of +authenticate+
class ApplicationController < ActionController::Base
    # Prevent CSRF attacks by raising an exception.
    # For APIs, you may want to use :null_session instead.
    protect_from_forgery with: :exception

    # layouts will not be rendered
    layout false

    # returns the Home Page
    def index
        render haml: "index.html.haml"
    end

    # returns a rendered Google Maps
    def map
        render erb: "map.html.erb"
    end

    # returns a JSON array of places:
    # +time+ - under x parameter,
    # +max+ - at most x parameter,
    # +min+ - at least x parameter,
    # +rating+ - at least x parameter,
    # +category+ - matches x parameter
    def places
        mongohq_url = ENV['MONGOHQ_URL']
        mongo_host = ENV['MONGO_HOST']
        mongo_port = ENV['MONGO_PORT']

        url = nil

        if mongohq_url
            url = mongohq_url
        elsif mongo_host and mongo_port
            url = 'mongodb://' + mongo_host + ':' + mongo_port + '/ciscochef'
        else
            url = 'mongodb://127.0.0.1:27017/ciscochef'
        end

        db = URI.parse(url)
        db_name = db.path.gsub(/^\//, '')
        dbc = Mongo::Connection.new(db.host, db.port).db(db_name)
        dbc.authenticate(db.user, db.password) unless (db.user.nil? || db.user.nil?)

        time = params[:time]
        max = params[:max]
        min = params[:min]
        rating = params[:rating]
        category = params[:category]

        query = {}

        if time then query["minutes"] = { "$lte" => time.to_i } end
        if max then query["maxparty"] = { "$lte" => max.to_i } end
        if min then query["minparty"] = { "$gte" => min.to_i } end
        if rating then query["rating"] = { "$gte" => rating.to_f } end
        if category then query["categories"] = { "$in" => [category] } end

        coll = dbc.collection("places")
        cursor = coll.find(query)
        render json: cursor.to_a
    end
end
