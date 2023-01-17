package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"os"

	"github.com/google/cel-go/cel"
	"gopkg.in/yaml.v3"
)

func main() {
	// Parse the command line arguments.
	// Add input format flag
	var inputFormat string
	flag.StringVar(&inputFormat, "input", "json", "Input format (json, yaml, etc.)")
	flag.Parse()
	// Check that we have argument to evaluate.
	if flag.NArg() != 1 {
		log.Fatalf("usage: %s <expression>", os.Args[0])
	}
	if inputFormat != "json" && inputFormat != "yaml" {
		log.Fatalf("input format %s not supported", inputFormat)
	}
	// Take the first argument as the expression to evaluate.
	cel_expr := flag.Arg(0)

	// Create the environment and parse the expression.
	env, err := cel.NewEnv(
		cel.Variable("object", cel.DynType),
	)
	if err != nil {
		log.Fatalf("environment creation error: %s", err)
	}
	ast, issues := env.Compile(cel_expr)
	if issues != nil && issues.Err() != nil {
		log.Fatalf("type-check error: %s", issues.Err())
	}
	prg, err := env.Program(ast)
	if err != nil {
		log.Fatalf("program construction error: %s", err)
	}
	// Read the object from the STDIN and evaluate the expression as a JSON object.
	var data map[string]interface{}
	if inputFormat == "yaml" {
		if err := yaml.NewDecoder(os.Stdin).Decode(&data); err != nil {
			log.Fatalf("error reading yaml: %s", err)
		}
	} else if inputFormat == "json" {
		if err := json.NewDecoder(os.Stdin).Decode(&data); err != nil {
			log.Fatalf("error reading json: %s", err)
		}
	}

	out, _, err := prg.Eval(map[string]interface{}{
		"object": data})
	if err != nil {
		log.Fatalf("runtime error: %s", err)
	}
	fmt.Println(out)
}
