# 30+50 Package Migration Ledger

Date: 2026-05-22

Scope: every row from the 2026-05-21 `sequential_30` and `reverse_50` verification runs. Successful silent-drift rows, rejected/no-diff rows, blocked rows, source-check-blocked rows, and duplicate/skipped rows are all represented in the case bank.

No case outside those two runs was newly migrated in this step. Existing non-30+50 packages were left in place.

## Counts

- Run rows covered: 80
- Newly created package folders in this step: 54
- Rows already covered before this step: 26
- Total case-bank packages after migration: 88

Status distribution inside the 30+50 migration scope:

- blocked_dependency: 27
- blocked_runtime: 14
- needs_source: 8
- rejected_no_diff: 5
- verified_keep: 26

Status distribution across the full case bank after migration:

- blocked_dependency: 27
- blocked_runtime: 14
- needs_source: 8
- rejected_no_diff: 5
- verified_keep: 34

## Newly Created In This Step

- DOTNET-01
- DOTNET-02
- DOTNET-03
- DOTNET-04
- DOTNET-06
- DOTNET-07
- DOTNET-10
- GO-004
- GO-005
- GO-008
- GO-009
- GO-010
- JS-07
- JS-08
- JVM-JAVA-09
- JVM-JAVA-10
- NEW-20260520-001
- NEW-20260520-002
- NEW-20260520-003
- NEW-20260520-004
- NEW-20260520-005
- NEW-20260520-006
- NEW-20260520-007
- NEW-20260520-008
- NEW-20260520-009
- NEW-20260520-010
- PHP-01
- PHP-02
- PHP-03
- PHP-04
- PHP-05
- PHP-06
- PHP-09
- PHP-10
- PY-SD-002
- PY-SD-003
- PY-SD-004
- PY-SD-006
- PY-SD-009
- RB-AS-001
- RB-AS-002
- RB-AS-003
- RB-AS-004
- RB-FAR-007
- RB-NOK-010
- RB-SKQ-008
- SEED-20260520-001
- SEED-20260520-002
- SEED-20260520-003
- SEED-20260520-004
- SEED-20260520-005
- SEED-20260520-006
- SEED-20260520-007
- SEED-20260520-008

## Already Covered Before This Step

- DOTNET-05
- DOTNET-09
- GO-001
- GO-003
- GO-006
- GO-007
- JS-01
- JS-02
- JS-03
- JS-04
- JS-05
- JS-10
- JVM-JAVA-01
- JVM-JAVA-02
- JVM-JAVA-03
- JVM-JAVA-04
- PHP-07
- PHP-08
- PY-SD-001
- PY-SD-005
- PY-SD-007
- PY-SD-008
- PY-SD-010
- RB-RACK-005
- RB-RACK-006
- RB-RSP-009

## Row Mapping

| Case ID | Scope | Original Status | First Blocked Step | Case-Bank Status | Migration Kind | Case Path |
|---|---|---|---|---|---|---|
| DOTNET-01 | sequential_30 | blocked | dependency_acquired | blocked_dependency | new failure/ledger package | `serialization-and-binding/dotnet-01-system-text-json-jsonserializer-serialize-object-value-options-with-cust` |
| DOTNET-02 | sequential_30 | blocked | dependency_acquired | blocked_dependency | new failure/ledger package | `serialization-and-binding/dotnet-02-system-text-json-jsonserializer-deserialize-jsondocument-null` |
| DOTNET-03 | sequential_30 | blocked | dependency_acquired | blocked_dependency | new failure/ledger package | `time-and-localization/dotnet-03-net-runtime-globalization-string-compare-casing-sorting-culture-apis` |
| DOTNET-04 | sequential_30 | blocked | dependency_acquired | blocked_dependency | new failure/ledger package | `time-and-localization/dotnet-04-net-runtime-core-libraries-datetime-adddays-addmilliseconds-other-add-do` |
| DOTNET-05 | sequential_30 | verified_keep |   | verified_keep | already covered before this step | `serialization-and-binding/dotnet-configurationbinder-dictionary-append` |
| DOTNET-06 | sequential_30 | blocked | old_run/new_run | blocked_runtime | new failure/ledger package | `state-and-lifecycle/dotnet-06-ef-core-asnotracking-include-query-materialization` |
| DOTNET-07 | sequential_30 | blocked | fixture_created | blocked_runtime | new failure/ledger package | `serialization-and-binding/dotnet-07-ef-core-enums-mapped-inside-ef-json-columns` |
| DOTNET-09 | sequential_30 | verified_keep |   | verified_keep | already covered before this step | `parsing-and-ingestion/dotnet-csvhelper-culture-delimiter` |
| DOTNET-10 | sequential_30 | no_behavior_diff | output_assertion | rejected_no_diff | new failure/ledger package | `serialization-and-binding/dotnet-10-automapper-mapping-collections-and-destination-member-reuse-especially-u` |
| GO-001 | sequential_30 | verified_keep |   | verified_keep | already covered before this step | `serialization-and-binding/go-json-omitzero` |
| GO-003 | sequential_30 | verified_keep |   | verified_keep | already covered before this step | `routing-and-identity/go-servemux-method-brace-pattern` |
| GO-004 | sequential_30 | blocked | dependency_acquired | blocked_dependency | new failure/ledger package | `parsing-and-ingestion/go-004-net-url-net-http-url-query-url-parsequery-request-formvalue` |
| GO-005 | sequential_30 | blocked | dependency_acquired | blocked_dependency | new failure/ledger package | `parsing-and-ingestion/go-005-mime-multipart-multipart-part-filename` |
| GO-006 | sequential_30 | verified_keep |   | verified_keep | already covered before this step | `observability-and-logging/go-test-json-build-output-events` |
| GO-007 | sequential_30 | verified_keep |   | verified_keep | already covered before this step | `parsing-and-ingestion/go-yaml-v2-v3-boolean-strings` |
| GO-008 | sequential_30 | no_behavior_diff | output_assertion | rejected_no_diff | new failure/ledger package | `serialization-and-binding/go-008-github-com-burntsushi-toml-toml-newencoder-encode-float-output` |
| GO-009 | sequential_30 | blocked | fixture_created | blocked_runtime | new failure/ledger package | `serialization-and-binding/go-009-google-golang-org-protobuf-proto-marshaloptions-deterministic-true-marsh` |
| GO-010 | sequential_30 | blocked | dependency_acquired | blocked_dependency | new failure/ledger package | `validation-and-policy/go-010-github-com-go-playground-validator-v10-validator-new-struct-with-require` |
| JS-01 | sequential_30 | verified_keep |   | verified_keep | already covered before this step | `time-and-localization/js-node-full-icu-locale-month` |
| JS-02 | sequential_30 | verified_keep |   | verified_keep | already covered before this step | `serialization-and-binding/js-npm-lockfile-version` |
| JS-03 | sequential_30 | verified_keep |   | verified_keep | already covered before this step | `serialization-and-binding/js-prettier-trailing-comma-default` |
| JS-04 | sequential_30 | verified_keep |   | verified_keep | already covered before this step | `serialization-and-binding/js-jest-snapshot-format-default` |
| JS-05 | sequential_30 | verified_keep |   | verified_keep | already covered before this step | `validation-and-policy/js-mongoose-strictquery-default` |
| JS-07 | sequential_30 | blocked | new_run | blocked_runtime | new failure/ledger package | `runtime-semantics/js-07-tailwind-css-utility-css-defaults-for-border-divide-ring` |
| JS-08 | sequential_30 | no_behavior_diff | output_assertion | rejected_no_diff | new failure/ledger package | `parsing-and-ingestion/js-08-marked-marked-parse-markdown-to-html-defaults` |
| JS-10 | sequential_30 | verified_keep |   | verified_keep | already covered before this step | `validation-and-policy/js-handlebars-prototype-access-default` |
| JVM-JAVA-01 | sequential_30 | verified_keep |   | verified_keep | already covered before this step | `parsing-and-ingestion/java-jackson-xml-empty-element` |
| JVM-JAVA-02 | sequential_30 | verified_keep |   | verified_keep | already covered before this step | `serialization-and-binding/java-gson-enum-tostring` |
| JVM-JAVA-03 | sequential_30 | verified_keep |   | verified_keep | already covered before this step | `serialization-and-binding/java-hibernate-native-count-type` |
| JVM-JAVA-04 | sequential_30 | verified_keep |   | verified_keep | already covered before this step | `routing-and-identity/java-spring-boot-path-pattern-default` |
| NEW-20260520-010 | reverse_50 | blocked_offline_reproduction | dependency_acquired | blocked_runtime | new failure/ledger package | `inventory-and-fulfillment/new-20260520-010-google-merchant-product-input-success-is-not-product-approval` |
| NEW-20260520-009 | reverse_50 | blocked_offline_reproduction | dependency_acquired | blocked_runtime | new failure/ledger package | `state-and-lifecycle/new-20260520-009-etsy-webhooks-carry-resource-pointers-and-may-replay` |
| NEW-20260520-008 | reverse_50 | source_check_blocked | source_check | needs_source | new failure/ledger package | `routing-and-identity/new-20260520-008-taobao-sensitive-order-data-changes-to-masked-oaid-dependent-data` |
| NEW-20260520-007 | reverse_50 | source_check_blocked | source_check | needs_source | new failure/ledger package | `inventory-and-fulfillment/new-20260520-007-taobao-online-logistics-send-can-create-flow-without-changing-trade-stat` |
| NEW-20260520-006 | reverse_50 | blocked_offline_reproduction | dependency_acquired | blocked_runtime | new failure/ledger package | `state-and-lifecycle/new-20260520-006-mercado-libre-notifications-require-ack-plus-resource-refetch` |
| NEW-20260520-005 | reverse_50 | blocked_offline_reproduction | dependency_acquired | blocked_runtime | new failure/ledger package | `state-and-lifecycle/new-20260520-005-bigcommerce-webhook-delivery-can-duplicate-lightweight-events` |
| NEW-20260520-004 | reverse_50 | blocked_offline_reproduction | dependency_acquired | blocked_runtime | new failure/ledger package | `commerce-order-flow/new-20260520-004-adobe-commerce-bulk-api-accepts-queue-entries-that-later-fail` |
| NEW-20260520-003 | reverse_50 | blocked_offline_reproduction | dependency_acquired | blocked_runtime | new failure/ledger package | `inventory-and-fulfillment/new-20260520-003-walmart-processed-feed-does-not-imply-element-success` |
| NEW-20260520-002 | reverse_50 | blocked_offline_reproduction | dependency_acquired | blocked_runtime | new failure/ledger package | `inventory-and-fulfillment/new-20260520-002-amazon-feed-status-hides-per-record-business-failures` |
| NEW-20260520-001 | reverse_50 | blocked_offline_reproduction | dependency_acquired | blocked_runtime | new failure/ledger package | `commerce-order-flow/new-20260520-001-douyin-order-sync-returns-success-but-order-center-is-empty` |
| SEED-20260520-008 | reverse_50 | source_check_blocked | source_check | needs_source | new failure/ledger package | `commerce-order-flow/seed-20260520-008-ecommerce-order-to-erp-sync-chain-evidence` |
| SEED-20260520-007 | reverse_50 | blocked_offline_reproduction | dependency_acquired | blocked_runtime | new failure/ledger package | `observability-and-logging/seed-20260520-007-generic-integration-silent-failure-evidence` |
| SEED-20260520-006 | reverse_50 | source_check_blocked | source_check | needs_source | new failure/ledger package | `commerce-order-flow/seed-20260520-006-pinduoduo-order-field-openness-retrofit` |
| SEED-20260520-005 | reverse_50 | blocked_offline_reproduction | dependency_acquired | blocked_runtime | new failure/ledger package | `routing-and-identity/seed-20260520-005-meituan-merchant-id-is-unstable` |
| SEED-20260520-004 | reverse_50 | source_check_blocked | source_check | needs_source | new failure/ledger package | `commerce-order-flow/seed-20260520-004-jd-order-status-callback-silently-discarded` |
| SEED-20260520-003 | reverse_50 | source_check_blocked | source_check | needs_source | new failure/ledger package | `state-and-lifecycle/seed-20260520-003-taobao-message-ordering` |
| SEED-20260520-002 | reverse_50 | source_check_blocked | source_check | needs_source | new failure/ledger package | `routing-and-identity/seed-20260520-002-taobao-receiver-address-field-semantics` |
| SEED-20260520-001 | reverse_50 | source_check_blocked | source_check | needs_source | new failure/ledger package | `commerce-order-flow/seed-20260520-001-taobao-order-detail-field-semantics` |
| RB-NOK-010 | reverse_50 | blocked_dependency_or_runtime | dependency_acquired | blocked_dependency | new failure/ledger package | `parsing-and-ingestion/rb-nok-010-nokogiri-xml-html4-sax-entity-handling` |
| RB-RSP-009 | reverse_50 | verified_keep |   | verified_keep | already covered before this step | `runtime-semantics/ruby-rspec-aggregate-failures-return` |
| RB-SKQ-008 | reverse_50 | blocked_dependency_or_runtime | dependency_acquired | blocked_dependency | new failure/ledger package | `state-and-lifecycle/rb-skq-008-sidekiq-job-payload-timestamps` |
| RB-FAR-007 | reverse_50 | skipped_existing_record |   | rejected_no_diff | new failure/ledger package | `parsing-and-ingestion/rb-far-007-faraday-query-string-encoding` |
| RB-RACK-006 | reverse_50 | verified_keep |   | verified_keep | already covered before this step | `parsing-and-ingestion/ruby-rack-response-header-casing` |
| RB-RACK-005 | reverse_50 | skipped_existing_record |   | verified_keep | already covered before this step | `parsing-and-ingestion/ruby-rack-semicolon-query` |
| RB-AS-004 | reverse_50 | blocked_dependency_or_runtime | dependency_acquired | blocked_dependency | new failure/ledger package | `state-and-lifecycle/rb-as-004-rails-activesupport-activesupport-cache-serialization-format` |
| RB-AS-003 | reverse_50 | blocked_dependency_or_runtime | dependency_acquired | blocked_dependency | new failure/ledger package | `state-and-lifecycle/rb-as-003-rails-activesupport-activesupport-digest-defaults` |
| RB-AS-002 | reverse_50 | blocked_dependency_or_runtime | dependency_acquired | blocked_dependency | new failure/ledger package | `serialization-and-binding/rb-as-002-rails-activesupport-enumerable-sole-on-tuple-yielding-enumerables` |
| RB-AS-001 | reverse_50 | blocked_dependency_or_runtime | dependency_acquired | blocked_dependency | new failure/ledger package | `time-and-localization/rb-as-001-rails-activesupport-activesupport-timewithzone-to-time` |
| PY-SD-010 | reverse_50 | skipped_existing_record |   | verified_keep | already covered before this step | `runtime-semantics/py-attrs-nan-equality` |
| PY-SD-009 | reverse_50 | blocked_dependency_or_runtime | dependency_acquired | blocked_dependency | new failure/ledger package | `runtime-semantics/py-sd-009-cython-compiler-default-language-level-for-pyx-files` |
| PY-SD-008 | reverse_50 | verified_keep |   | verified_keep | already covered before this step | `state-and-lifecycle/py-sqlalchemy-autocommit-removed` |
| PY-SD-007 | reverse_50 | verified_keep |   | verified_keep | already covered before this step | `serialization-and-binding/py-pydantic-nested-subclass-serialization` |
| PY-SD-006 | reverse_50 | blocked_dependency_or_runtime | dependency_acquired | blocked_dependency | new failure/ledger package | `serialization-and-binding/py-sd-006-dask-dask-dataframe-string-dtype-inference-conversion` |
| PY-SD-005 | reverse_50 | verified_keep |   | verified_keep | already covered before this step | `parsing-and-ingestion/py-polars-join-null-key-matching` |
| PY-SD-004 | reverse_50 | blocked_dependency_or_runtime | dependency_acquired | blocked_dependency | new failure/ledger package | `runtime-semantics/py-sd-004-scikit-learn-sklearn-cluster-kmeans-n-init-omitted` |
| PY-SD-003 | reverse_50 | blocked_dependency_or_runtime | dependency_acquired | blocked_dependency | new failure/ledger package | `runtime-semantics/py-sd-003-scipy-scipy-stats-mode-with-omitted-keepdims` |
| PY-SD-002 | reverse_50 | blocked_dependency_or_runtime | dependency_acquired | blocked_dependency | new failure/ledger package | `serialization-and-binding/py-sd-002-pandas-dataframe-groupby-sort-false-with-ordered-categorical-grouper` |
| PY-SD-001 | reverse_50 | verified_keep |   | verified_keep | already covered before this step | `runtime-semantics/py-numpy-dtype-promotion` |
| PHP-10 | reverse_50 | blocked_dependency_or_runtime | dependency_acquired | blocked_dependency | new failure/ledger package | `routing-and-identity/php-10-guzzle-client-request-option-idn-conversion-default` |
| PHP-09 | reverse_50 | blocked_dependency_or_runtime | dependency_acquired | blocked_dependency | new failure/ledger package | `observability-and-logging/php-09-monolog-default-date-formatting-in-formatters-log-output` |
| PHP-08 | reverse_50 | verified_keep |   | verified_keep | already covered before this step | `time-and-localization/php-carbon-diffin-float-signed` |
| PHP-07 | reverse_50 | skipped_existing_record |   | verified_keep | already covered before this step | `time-and-localization/php-carbon-timestamp-timezone` |
| PHP-06 | reverse_50 | blocked_dependency_or_runtime | dependency_acquired | blocked_dependency | new failure/ledger package | `state-and-lifecycle/php-06-laravel-illuminate-collections-when-unless-conditional-callback-argument` |
| PHP-05 | reverse_50 | blocked_dependency_or_runtime | dependency_acquired | blocked_dependency | new failure/ledger package | `state-and-lifecycle/php-05-laravel-illuminate-filesystem-storage-put-write-writestream` |
| PHP-04 | reverse_50 | blocked_dependency_or_runtime | dependency_acquired | blocked_dependency | new failure/ledger package | `parsing-and-ingestion/php-04-symfony-serializer-csvencoder-decode-default-context` |
| PHP-03 | reverse_50 | skipped_existing_record |   | rejected_no_diff | new failure/ledger package | `serialization-and-binding/php-03-php-core-htmlspecialchars-htmlentities-defaults` |
| PHP-02 | reverse_50 | blocked_dependency_or_runtime | dependency_acquired | blocked_dependency | new failure/ledger package | `runtime-semantics/php-02-php-core-sorting-functions-sort-usort-uasort-etc` |
| PHP-01 | reverse_50 | blocked_dependency_or_runtime | dependency_acquired | blocked_dependency | new failure/ledger package | `runtime-semantics/php-01-php-core-loose-comparison` |
| JVM-JAVA-10 | reverse_50 | blocked_dependency_or_runtime | dependency_acquired | blocked_dependency | new failure/ledger package | `time-and-localization/jvm-java-10-java-stdlib-default-charset-apis-such-as-new-string-bytes-filereader-sca` |
| JVM-JAVA-09 | reverse_50 | blocked_dependency_or_runtime | dependency_acquired | blocked_dependency | new failure/ledger package | `runtime-semantics/jvm-java-09-maven-mvn-maven-config-parsing` |

## Validation Commands

Run after migration:

```powershell
python -m case_bank validate --cases docs/case-bank/cases
python -m case_bank index build --cases docs/case-bank/cases --out docs/case-bank/indexes --schema-out docs/case-bank/metadata.schema.json --expected-schema-out docs/case-bank/expected.schema.json
python -m case_bank pack --src docs/case-bank/cases --out <fresh-eval-package-dir>
python -m pytest silent_drift_miner/tests -q -p no:cacheprovider
```
