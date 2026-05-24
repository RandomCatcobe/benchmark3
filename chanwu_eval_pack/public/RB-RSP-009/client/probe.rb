require "rspec/expectations"
include RSpec::Matchers

p aggregate_failures { expect(1).to eq(1) }
