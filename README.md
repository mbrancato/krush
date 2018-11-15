# krush

Krush uses simple templating logic to assist in the deployment of resources to Kubernetes. It allows operators to better align their process with GitOps by removing deployment variables and allowing those to be handled by downstream manual or CI/CD processes. When run, krush takes the rendered manifests and pipes the output to a `kubectl apply` command.

## Getting Started

To use krush, minimal changes are required to existing manifests. The manifests can define any Kubernetes resource, and the variables may exist anywhere in the manifest, including content of ConfigMaps.

* Variables are identified with [Jinja2](http://jinja.pocoo.org/docs/latest/templates/)-style (e.g. `{{ variable_name }}`)
* All manifest files are expected to end in `.yaml` or `.yml`
* A file may be provided that defines some or all variable values
* For any undefined variables, krush will prompt the user for the value

In the simplest form, krush can be run with no options from within a directory tree containing templated manifests and it will prompt the user for the values of each variable.

```
krush
```

### Prerequisites

* kubectl must be installed and accessible in the PATH
* Any authentication needed for kubectl must be performed prior to running krush

### Installing

To install krush and its dependencies, run the following:

```
python setup.py install
```

## Usage

```
Usage:
  krush [--vars=<file.vars>] [path]

Arguments:
  path                    Optional search path or file name

Options:
  --vars=<file.vars>      File with variables defined and assigned
  -h, --help              Show this message and exit.
```

## Variable Files

Variable files are in YAML format. To avoid detection as a Kubernetes manifest, the variable file should not have a `.yaml` or `.yml` file. The key name in the variable file corresponds to the template's variable name.

For example, a template with a variable defined as `{{ url }}` can be provided in a variable file as:

```
url: "http://www.github.com"
```

## License

This project is licensed under the Apache License, Version 2.0 - see the [LICENSE](LICENSE) file for details
