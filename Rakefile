require './web'
require 'rspec/core/rake_task'

task :default => :help

desc "Run specs"
task :spec do
  RSpec::Core::RakeTask.new(:spec) do |t|
    t.pattern = './spec/**/*_spec.rb'
  end
end

desc "Show help menu"
task :help do
  puts "Available rake tasks: "
  puts "rake spec - Run specs and calculate coverage"
end
