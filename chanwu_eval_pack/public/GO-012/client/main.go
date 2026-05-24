package main

import (
	"encoding/json"
	"fmt"

	"github.com/pelletier/go-toml/v2"
)

type Config struct {
	Count int `toml:"count,omitzero"`
}

func main() {
	text, err := toml.Marshal(Config{})
	payload := map[string]any{"toml": string(text)}
	if err != nil {
		payload["err"] = err.Error()
	}

	out, err := json.Marshal(payload)
	if err != nil {
		panic(err)
	}
	fmt.Println(string(out))
}
