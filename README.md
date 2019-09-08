# Train Routes App

## Main Concepts Used
- Use Floyd–Warshall algorithm for the any-node-to-any-node shortest path calculation
    - Memory usage complexity: O(N^2)
    - Time complexity for the first time calcualtion: O(N^3)
    - Time complexity for subsequent queries: O(1)
- Use PEP 8 code style
- Use Dependency Injection for ease of doing unit tests
- Handle common IO errors to make the app operating gracefully at some degree
- Use some built in standard libraries of Python: csv, unittest
    - They can be written from scratches with bare hands later if needed

## Running
Just run this command

```
python3 main.py
```

In case we want to change the path to CSV route configuratino file from the default `routes.csv` to something else, specific `--file` argument, like below:

```
python3 main.py --file=routes.csv
```

## Testing
Just run this command 

```
python3 -m unittest test/*.py
```