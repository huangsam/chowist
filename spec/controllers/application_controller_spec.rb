require 'spec_helper'

describe ApplicationController do
  it 'should work for root' do
    visit '/'
    expect(page).to have_content('Pick a restaurant already!')
  end

  it 'should work for map' do
    visit '/map'
    expect(page).to have_css('body')
  end

  it 'should work for places' do
    visit '/api/places'
    expect(page).not_to have_title('Cisco Chef')
  end

  it 'should create a mongodb uri' do
    controller = ApplicationController.new
    uri = controller.create_uri
    expect(uri).to match(%r{mongodb://})
  end

  it 'should create empty query with all nils' do
    controller = ApplicationController.new
    query = controller.create_query(nil, nil, nil, nil, nil)
    expect(query).to eq({})
  end

  it 'should not create empty query with no nils' do
    controller = ApplicationController.new
    query = controller.create_query('60', '3', '8', '3', 'Thai')
    expect(query).not_to eq({})
  end
end
