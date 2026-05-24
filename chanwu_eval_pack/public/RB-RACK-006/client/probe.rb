require "rack"

headers = { "Content-Type" => "text/plain", "X-Test" => "1" }
response = Rack::Response.new([], 200, headers)
p response.headers.keys
