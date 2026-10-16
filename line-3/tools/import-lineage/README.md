# Import Lineage

`lineage.py` follows one named Python module through a source tree and prints the
shortest import path from a chosen entry point. It reads source text only; it
never imports or executes the project being inspected.

Try it with the included example:

```sh
python3 line-3/tools/import-lineage/lineage.py line-3/tools/import-lineage/examples app service
```

The output is a compact JSON object containing the path and whether the target
was found. It handles relative imports, absolute local imports, and cycles.

Observed: the command above prints a two-edge path from `app.py` to
`service.py`; it also reports missing targets without executing example code.

Limitations: dynamic imports and imports assembled from runtime values cannot
be inferred from static Python syntax.
