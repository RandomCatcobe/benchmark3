# Environment For GO-007

        - Old version: gopkg.in/yaml.v2.
        - New version: gopkg.in/yaml.v3.
        - Adapter/API surface: library-api, yaml-parser.
        - Runtime: Go with gopkg.in/yaml.v2 or gopkg.in/yaml.v3 available.
- Version switching: change the import path in main.go or use the v2/v3 variants noted in comments.
- Probe shape: go run . and compare reflected value types.
