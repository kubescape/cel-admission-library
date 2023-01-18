package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"os"

	"github.com/google/cel-go/cel"
	"gopkg.in/yaml.v3"
	"k8s.io/apiserver/pkg/cel/library"
)

func main() {
	// Parse the command line arguments.
	// Add input format flag
	var inputFormat string
	flag.StringVar(&inputFormat, "input", "json", "Input format (json, yaml, etc.)")
	var paramsFile string
	flag.StringVar(&paramsFile, "params", "", "File containing parameters")
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

	var params map[string]interface{}
	if paramsFile != "" {
		// Read the parameters from the file as a YAML object.
		f, err := os.Open(paramsFile)
		if err != nil {
			log.Fatalf("error opening params file: %s", err)
		}
		if err := yaml.NewDecoder(f).Decode(&params); err != nil {
			log.Fatalf("error reading params file: %s", err)
		}
	}

	// Create the environment and parse the expression.
	var opts []cel.EnvOption
	opts = append(opts, cel.Variable("object", cel.DynType))
	opts = append(opts, cel.Variable("params", cel.DynType))
	opts = append(opts, library.ExtensionLibs...)
	env, err := cel.NewEnv(opts...)
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
		"object": data, "params": params})
	if err != nil {
		log.Fatalf("runtime error: %s", err)
	}
	fmt.Println(out)
}
