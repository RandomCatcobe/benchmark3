# Evidence For RB-STRICT-001

## Source URLs

- https://github.com/weppos/publicsuffix-ruby/blob/main/CHANGELOG.md

## Source Notes

The public_suffix gem embeds Public Suffix List data; the local probe shows the updated classification for `pages.gay`.

## Local Reproduction

- Old: `public_suffix 5.0.4`
- New: `public_suffix 5.0.5`
- Old stdout: `{"domain":"pages.gay"}`
- New stdout: `{"domain":"foo.pages.gay"}`
- Old/new exit code: 0
- Old/new stderr: empty
- Verification path: `data/verification/ruby_new_probe/ruby-public-suffix-pages-gay-domain`
