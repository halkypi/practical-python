[Contents](../Contents.md) | [Prev (9 Packages)](../09_Packages/00_Overview.md)

# 10. Streamlit Applications

This section adapts the portfolio exercises into a small Streamlit app.
The goal is not to abandon scripts.  The goal is to show how the same
Python functions you wrote earlier can become an interactive data tool.

You will build a portfolio dashboard that:

* Reads `Work/Data/portfolio.csv`
* Reads `Work/Data/prices.csv`
* Computes cost, current value, and gain or loss
* Lets a user filter holdings
* Displays a table and chart

## Setup

Streamlit is a third-party package.  From the top-level
`practical-python/` directory, install the project dependencies:

```bash
python -m pip install -e .
```

If you use `uv`, you can run:

```bash
uv run streamlit run Work/streamlit_app.py
```

With a plain virtual environment, run:

```bash
streamlit run Work/streamlit_app.py
```

## Exercises

### Exercise 10.1: Your first Streamlit app

Open `Work/streamlit_app.py`.  Run it with:

```bash
streamlit run Work/streamlit_app.py
```

Change the title and caption.  Save the file and refresh the browser if
needed.  Notice that Streamlit runs your Python script from top to
bottom whenever the page changes.

Add a slider:

```python
shares = st.slider("Shares", min_value=0, max_value=500, value=100)
price = st.number_input("Price", min_value=0.0, value=42.0)
st.write("Market value:", shares * price)
```

This is the same calculation style as earlier exercises, but now the
input comes from widgets instead of command-line editing.

### Exercise 10.2: Read course data

In `Work/streamlit_app.py`, write functions to read the portfolio and
price files.  You can adapt earlier work from `pcost.py`, `report.py`,
and `fileparse.py`.

Add this import at the top of the file:

```python
import csv
```

Suggested function names:

```python
def read_portfolio(filename):
    ...

def read_prices(filename):
    ...
```

Use `csv.DictReader` for the portfolio file.  Convert `shares` to an
integer and `price` to a float.  For the price file, return a dictionary
that maps a stock name to its latest price.  Skip blank rows--CSV files
often have a trailing blank line.

The price-reading loop should look like this:

```python
for row in rows:
    if not row:
        continue
    name, price = row
    prices[name] = float(price)
```

After loading the data, display it:

```python
portfolio = read_portfolio(DATA_DIR / "portfolio.csv")
st.dataframe(portfolio, hide_index=True)
```

### Exercise 10.3: Make useful rows

Create a function that combines the portfolio and price data into rows
suited for display:

```python
def make_report(portfolio, prices):
    ...
```

Each row should include:

* `name`
* `shares`
* `purchase_price`
* `current_price`
* `cost`
* `value`
* `change`

Display the report with `st.dataframe()`.  Add `column_config` so money
columns show as currency.  Hide the index.

For example:

```python
st.dataframe(
    report,
    column_config={
        "cost": st.column_config.NumberColumn("Cost", format="$%.2f"),
        "value": st.column_config.NumberColumn("Value", format="$%.2f"),
    },
    hide_index=True,
)
```

### Exercise 10.4: Add interaction

Add a sidebar with app-level filters:

```python
names = {row["name"] for row in report}

with st.sidebar:
    selected = st.multiselect("Stocks", sorted(names), default=sorted(names))
    min_value = st.slider("Minimum value", 0, 20000, 0, step=500)
```

Filter the report so only selected stocks with a value above the slider
are shown.  Keep the table in the main page, not in the sidebar.

```python
filtered = [
    row for row in report if row["name"] in selected and row["value"] >= min_value
]
```

### Exercise 10.5: Add metrics and a chart

At the top of the page, display three metrics:

* Total cost
* Current value
* Gain or loss

Then add a bar chart that compares value by stock:

```python
if filtered:
    st.bar_chart(filtered, x="name", y="value", x_label="Stock", y_label="Value")
else:
    st.info("No holdings match the current filters.")
```

For a finished reference, see `Solutions/10_5/streamlit_app.py`.

### Exercise 10.6: Cache the data loading

Decorate your file-reading functions with `@st.cache_data`.  Restart
the app and confirm that the app still works.

Caching is useful here because widgets cause reruns.  You want the
filtering and display to update immediately, but you do not need to read
the CSV files from disk on every interaction.

## Instructor Notes

This section works well after Section 3, when students have working
functions in `report.py`.  It also works as a capstone after Section 9:
students can import their packaged portfolio code instead of keeping all
functions in one file.

Keep the emphasis on ordinary Python.  Streamlit should feel like a
thin interactive layer over data loading, transformation, and display.

For a complete map of the local Streamlit skill material and how to use
it in class, see [10.7 Streamlit Skill Material Guide](01_Skill_Material_Guide.md).
For a reusable testing assistant prompt, see
[10.8 Testing/QE Agent Prompt](02_Testing_QE_Agent_Prompt.md).
