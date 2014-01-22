require 'spec_helper'

describe Website::Protected do
    
    def app
        @app ||= Website::Protected
    end
    
    describe "get /api/places" do
        it "should work with valid credentials" do
            digest_authorize 'cisco', 'chef2'
            get '/places'
            expect(last_response).to be_ok
        end

        it "should not work with invalid credentials" do
            digest_authorize 'admin', 'admin'
            get '/places'
            expect(last_response).to_not be_ok
        end
    end

    context "posting place" do
        it "should fail" do
            digest_authorize 'cisco', 'chef2'
            post '/place', {:name => "Candy"}.to_json, "content_type" => "application/json"
            expect(last_response.body) == "Object was unsuccessful."
        end

        it "should fail with invalid credentials" do
            digest_authorize 'admin', 'admin'
            post '/place', {:name => "Candy"}.to_json, "content_type" => "application/json"
            expect(last_response).to_not be_ok
        end
    end
end
