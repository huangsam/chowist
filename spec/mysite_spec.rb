require 'spec_helper'

describe Website::MySite do
    
    def app
        @app ||= Website::MySite
    end
    
    context "basic http" do
        ["/", "/map"].each do |url|
            it "should be ok" do
                get url
                expect(last_response).to be_ok
            end
        end
        ["/foo", "/bar"].each do |url|
            it "should return 404" do
                get url
                expect(last_response.status) == 404
            end
        end
    end

    describe "get /places" do
        it "should work" do
            get '/places'
            expect(last_response).to be_ok
        end
    end

    context "posting place" do
        it "should fail" do
            post '/place', {:name => "Candy"}.to_json, "content_type" => "application/json"
            expect(last_response.body) == "Object was unsuccessful."
        end
    end
end
