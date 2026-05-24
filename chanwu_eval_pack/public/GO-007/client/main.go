package main

import (
    "fmt"

    yaml "gopkg.in/yaml.v3"
)

func main() {
    var out map[string]any
    if err := yaml.Unmarshal([]byte("flag: on\nnope: no\n"), &out); err != nil {
        panic(err)
    }
    fmt.Printf("flag=%T:%v nope=%T:%v\n", out["flag"], out["flag"], out["nope"], out["nope"])
}
