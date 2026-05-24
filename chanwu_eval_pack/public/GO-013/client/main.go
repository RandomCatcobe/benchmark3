package main

import (
	"encoding/json"
	"fmt"

	"github.com/goccy/go-yaml"
)

type Value struct{}

func (Value) MarshalText() ([]byte, error) {
	return []byte("a: b"), nil
}

func main() {
	text, err := yaml.Marshal(map[string]Value{"v": {}})
	payload := map[string]any{"yaml": string(text)}
	if err != nil {
		payload["err"] = err.Error()
	}

	out, err := json.Marshal(payload)
	if err != nil {
		panic(err)
	}
	fmt.Println(string(out))
}
