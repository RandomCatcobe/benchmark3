require "json"
require "public_suffix"

puts JSON.generate({ domain: PublicSuffix.domain("foo.pages.gay") })
