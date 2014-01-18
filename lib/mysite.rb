require 'sinatra/base'

module Website
  class MySite < Sinatra::Base

    configure do
      # set app specific settings
      # for example different view folders
      set :public, "public"
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
