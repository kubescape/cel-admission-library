# CEL CLI
Testing CEL code easily

## How to build
```bash
go mod tidy
go build .
```

## How to use
```bash
$ echo "{\"field\":0}" | go run main.go "object.field < 1"
true
```
