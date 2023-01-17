package main

import (
	"encoding/json"
	"fmt"
	"log"
	"os"

	"github.com/google/cel-go/cel"
)

func main() {
	// Check that we have argument to evaluate.
	if len(os.Args) < 2 {
		log.Fatalf("usage: %s <expression>", os.Args[0])
	}
	// Take the first argument as the expression to evaluate.
	cel_expr := os.Args[1]

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
	if err := json.NewDecoder(os.Stdin).Decode(&data); err != nil {
		log.Fatalf("error reading json: %s", err)
	}

	out, _, err := prg.Eval(map[string]interface{}{
		"object": data})
	if err != nil {
		log.Fatalf("runtime error: %s", err)
	}
	fmt.Println(out)
}
