require 'spec_helper'

describe ApplicationController do
    it "should work for root" do
        get :index
        expect(page).to render_template("index")
    end

    it "should work for map" do
        get :map
        expect(page).to render_template("map")
    end

    it "should work for places" do
        get :places
        expect(response.status).to eq(200)
    end

end