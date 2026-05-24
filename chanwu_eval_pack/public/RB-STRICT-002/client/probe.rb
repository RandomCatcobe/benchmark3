require "json"
require "mime/types"

type = MIME::Types.type_for("x.parquet").first
puts JSON.generate({ content_type: type&.content_type })
