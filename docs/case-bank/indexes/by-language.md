# Cases By Language

Generated from `docs/case-bank/cases/**/metadata.json`.

## csharp

| Case ID | Title | Status | Ecosystems | Path |
|---|---|---|---|---|
| `DOTNET-05` | ConfigurationBinder appends dictionary collection values | `verified_keep` | dotnet | `serialization-and-binding/dotnet-configurationbinder-dictionary-append` |
| `DOTNET-08` | FluentValidation default EmailAddress behavior changed | `verified_keep` | dotnet | `validation-and-policy/dotnet-08-fluentvalidation-email` |
| `DOTNET-09` | CsvHelper infers culture delimiter from CultureInfo | `verified_keep` | dotnet | `parsing-and-ingestion/dotnet-csvhelper-culture-delimiter` |

## go

| Case ID | Title | Status | Ecosystems | Path |
|---|---|---|---|---|
| `GO-001` | encoding/json omitzero starts omitting zero fields | `verified_keep` | go | `serialization-and-binding/go-json-omitzero` |
| `GO-002` | Go timer channels changed observable capacity | `verified_keep` | go | `state-and-lifecycle/go-timer-channel-capacity` |
| `GO-003` | ServeMux treats method and brace patterns as structured routes | `verified_keep` | go | `routing-and-identity/go-servemux-method-brace-pattern` |
| `GO-006` | go test -json emits structured build-output events | `verified_keep` | go | `observability-and-logging/go-test-json-build-output-events` |
| `GO-007` | go-yaml v3 stops treating YAML 1.1 booleans as bools | `verified_keep` | go | `parsing-and-ingestion/go-yaml-v2-v3-boolean-strings` |

## java

| Case ID | Title | Status | Ecosystems | Path |
|---|---|---|---|---|
| `JVM-JAVA-01` | Jackson XML empty elements deserialize as empty strings | `verified_keep` | jvm | `parsing-and-ingestion/java-jackson-xml-empty-element` |
| `JVM-JAVA-02` | Gson reads enum constants using toString values | `verified_keep` | jvm | `serialization-and-binding/java-gson-enum-tostring` |
| `JVM-JAVA-03` | Hibernate native count result changes from BigInteger to Long | `verified_keep` | jvm | `serialization-and-binding/java-hibernate-native-count-type` |
| `JVM-JAVA-04` | Spring Boot defaults to PathPatternParser matching | `verified_keep` | jvm | `routing-and-identity/java-spring-boot-path-pattern-default` |
| `JVM-JAVA-07` | Commons CSV enum header lookup changed from toString to name | `verified_keep` | jvm | `parsing-and-ingestion/jvm-commons-csv-enum-header` |

## javascript

| Case ID | Title | Status | Ecosystems | Path |
|---|---|---|---|---|
| `JS-01` | Node.js full ICU changes locale month formatting | `verified_keep` | js | `time-and-localization/js-node-full-icu-locale-month` |
| `JS-02` | npm creates lockfileVersion 2 instead of version 1 | `verified_keep` | js | `serialization-and-binding/js-npm-lockfile-version` |
| `JS-03` | Prettier 3 adds trailing commas by default | `verified_keep` | js | `serialization-and-binding/js-prettier-trailing-comma-default` |
| `JS-04` | Jest snapshot formatting drops Object prefixes | `verified_keep` | js | `serialization-and-binding/js-jest-snapshot-format-default` |
| `JS-05` | Mongoose strictQuery stops stripping unknown filters by default | `verified_keep` | js | `validation-and-policy/js-mongoose-strictquery-default` |
| `JS-06` | Zod optional defaults are applied inside object parsing | `verified_keep` | js | `validation-and-policy/js-zod-optional-defaults` |
| `JS-09` | dotenv starts treating unquoted hash text as comments | `verified_keep` | js | `parsing-and-ingestion/js-dotenv-hash-comments` |
| `JS-10` | Handlebars blocks prototype property access by default | `verified_keep` | js | `validation-and-policy/js-handlebars-prototype-access-default` |

## php

| Case ID | Title | Status | Ecosystems | Path |
|---|---|---|---|---|
| `PHP-07` | Carbon timestamp creation defaults to UTC | `verified_keep` | php | `time-and-localization/php-carbon-timestamp-timezone` |
| `PHP-08` | Carbon diffInSeconds returns signed floating-point values | `verified_keep` | php | `time-and-localization/php-carbon-diffin-float-signed` |
| `PHP-11` | call_user_func_array binds string keys as named arguments | `verified_keep` | php | `serialization-and-binding/php-call-user-func-array-named-args` |
| `PHP-12` | htmlspecialchars default flags escape single quotes | `verified_keep` | php | `serialization-and-binding/php-htmlspecialchars-default-flags` |
| `PHP-13` | ksort SORT_REGULAR orders numeric keys before string keys | `verified_keep` | php | `parsing-and-ingestion/php-ksort-regular-mixed-keys` |

## python

| Case ID | Title | Status | Ecosystems | Path |
|---|---|---|---|---|
| `PY-SD-001` | NumPy 2.0 changes scalar and array dtype promotion | `verified_keep` | python | `runtime-semantics/py-numpy-dtype-promotion` |
| `PY-SD-005` | Polars no longer matches null join keys by default | `verified_keep` | python | `parsing-and-ingestion/py-polars-join-null-key-matching` |
| `PY-SD-007` | Pydantic masks nested subclass fields during serialization | `verified_keep` | python | `serialization-and-binding/py-pydantic-nested-subclass-serialization` |
| `PY-SD-008` | SQLAlchemy stops autocommitting Core statements | `verified_keep` | python | `state-and-lifecycle/py-sqlalchemy-autocommit-removed` |
| `PY-SD-010` | attrs generated equality changed for shared NaN values | `verified_keep` | python | `runtime-semantics/py-attrs-nan-equality` |

## ruby

| Case ID | Title | Status | Ecosystems | Path |
|---|---|---|---|---|
| `RB-RACK-005` | Rack stops treating semicolons as query separators | `verified_keep` | ruby | `parsing-and-ingestion/ruby-rack-semicolon-query` |
| `RB-RACK-006` | Rack Response normalizes response header names to lowercase | `verified_keep` | ruby | `parsing-and-ingestion/ruby-rack-response-header-casing` |
| `RB-RSP-009` | RSpec aggregate_failures returns true on success | `verified_keep` | ruby | `runtime-semantics/ruby-rspec-aggregate-failures-return` |
