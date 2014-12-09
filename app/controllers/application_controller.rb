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
        # generate MongoDB URI
        mongohq_url = ENV['MONGOHQ_URL']
        mongo_host = ENV['CISCOCHEF_DB_1_PORT_27017_TCP_ADDR'] || ENV['MONGO_HOST'] || '127.0.0.1'
        mongo_port = ENV['CISCOCHEF_DB_1_PORT_27017_TCP_PORT'] || ENV['MONGO_PORT'] || '27017'
        uri = mongohq_url || 'mongodb://' + mongo_host + ':' + mongo_port + '/ciscochef'

        # connect to MongoDB
        db = URI.parse(uri)
        db_name = db.path.gsub(/^\//, '')
        dbc = Mongo::Connection.new(db.host, db.port).db(db_name)
        dbc.authenticate(db.user, db.password) unless (db.user.nil? || db.user.nil?)

        # params holds query parameters
        time = params[:time]
        max = params[:max]
        min = params[:min]
        rating = params[:rating]
        category = params[:category]

        query = {}

        # add filter criteria
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
