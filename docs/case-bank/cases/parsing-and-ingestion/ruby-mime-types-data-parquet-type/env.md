# Environment For RB-STRICT-002

- Runtime: Ruby 4.0 with Bundler.
- Package versions: `mime-types-data 3.2025.0924` and `3.2026.0317`, with `mime-types 3.6.0` pinned.
- Version switching: edit `client/Gemfile` to pin the target data gem version, then run `bundle install`.
- Adapter/API surface: library-api.
- Probe shape: run `bundle exec ruby probe.rb` in `client/` and parse one JSON object from stdout.
- Command shape: `bundle config set path vendor/bundle`, `bundle install`, `bundle exec ruby probe.rb`.
