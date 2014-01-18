require 'spec_helper'

describe Website::MySite do
  
  def app
    @app ||= Website::MySite
  end
  
  describe "GET '/'" do
    it "should be successful" do
      get '/'
      last_response.should be_ok
    end
  end

  describe "GET '/map'" do
    it "should be successful" do
      get '/'
      last_response.should be_ok
    end
  end
end
