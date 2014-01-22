require 'spec_helper'

describe Website::Api do
    
    def app
        @app ||= Website::Api
    end
    
    describe "get /api/places" do
        it "should work" do
            get '/places'
            expect(last_response).to be_ok
        end
    end

end
