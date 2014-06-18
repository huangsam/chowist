require 'spec_helper'

describe ApplicationController do
    it "should work for root" do
        visit '/'
        expect(page).to have_content("Pick a restaurant already!")
    end

    it "should work for map" do
        visit '/map'
        expect(page).to have_css("body")
    end

    it "should work for places" do
        visit '/api/places'
        expect(page).not_to have_title('Cisco Chef')
    end

end