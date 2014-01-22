require 'spec_helper'

describe Website::Public do
    
    def app
        @app ||= Website::Public
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

end
