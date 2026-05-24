package main

import (
	"encoding/json"
	"fmt"

	semver "github.com/Masterminds/semver/v3"
)

func main() {
	constraint, err := semver.NewConstraint(">1.0.0-beta.1 <2")
	if err != nil {
		panic(err)
	}

	version := semver.MustParse("1.0.0-beta.2")
	payload := map[string]any{
		"check": constraint.Check(version),
	}

	out, err := json.Marshal(payload)
	if err != nil {
		panic(err)
	}
	fmt.Println(string(out))
}
