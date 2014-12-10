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
    render haml: 'index.html.haml'
  end

  # returns a rendered Google Maps
  def map
    render erb: 'map.html.erb'
  end

  # returns a JSON array of places:
  # +time+ - under x parameter,
  # +max+ - at most x parameter,
  # +min+ - at least x parameter,
  # +rating+ - at least x parameter,
  # +category+ - matches x parameter
  def places
    # connect to database
    uri = create_uri
    db = URI.parse(uri)
    db_name = db.path.gsub(/^\//, '')
    dbc = Mongo::Connection.new(db.host, db.port).db(db_name)
    dbc.authenticate(db.user, db.password) unless db.user.nil? || db.user.nil?

    db_query = create_query(params[:time], params[:min], params[:max],
                            params[:rating], params[:category])

    # query database and render results
    coll = dbc.collection('places')
    cursor = coll.find(db_query)
    render json: cursor.to_a
  end

  # creates database URI
  def create_uri
    mongohq_url = ENV['MONGOHQ_URL']
    mongo_host = ENV['CISCOCHEF_DB_1_PORT_27017_TCP_ADDR'] || '127.0.0.1'
    mongo_port = ENV['CISCOCHEF_DB_1_PORT_27017_TCP_PORT'] || '27017'
    mongohq_url || "mongodb://#{mongo_host}:#{mongo_port}/ciscochef"
  end

  # creates database query
  def create_query(time, min, max, rating, category)
    query = {}
    query['minutes'] = { '$lte' => time.to_i } unless time.nil?
    query['maxparty'] = { '$lte' => max.to_i } unless max.nil?
    query['minparty'] = { '$gte' => min.to_i } unless min.nil?
    query['rating'] = { '$gte' => rating.to_f } unless rating.nil?
    query['categories'] = { '$in' => [category] } unless category.nil?
  end
end
