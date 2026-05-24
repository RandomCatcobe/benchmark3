# Environment For RB-STRICT-001

- Runtime: Ruby 4.0 with Bundler.
- Package versions: `public_suffix 5.0.4` and `5.0.5`.
- Version switching: edit `client/Gemfile` to pin the target gem version, then run `bundle install`.
- Adapter/API surface: library-api.
- Probe shape: run `bundle exec ruby probe.rb` in `client/` and parse one JSON object from stdout.
- Command shape: `bundle config set path vendor/bundle`, `bundle install`, `bundle exec ruby probe.rb`.
