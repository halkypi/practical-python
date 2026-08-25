[Contents](../Contents.md) | [Prev (10 Streamlit)](../10_Streamlit/00_Overview.md)

# 11. Altair Charts

This section adds Altair to the Streamlit portfolio app.  Altair lets
you describe a chart as data plus visual encodings.  Streamlit gives
the chart a place to run.

You will build charts that:

* Map columns to position, color, size, and tooltips
* Compare cost, value, and gain or loss
* Add selections, brushes, and hover behavior
* Use Altair transforms for aggregation and ranking
* Compose charts with layers, facets, and repeated views

## Setup

From the top-level `practical-python/` directory, install the project:

```bash
python -m pip install -e .
```

If you use `uv`, run a demo with:

```bash
uv run streamlit run Work/Altair_Demos/basics.py
```

With a plain virtual environment, run:

```bash
streamlit run Work/Altair_Demos/basics.py
```

## Demo Files

The demo apps live in `Work/Altair_Demos/`.

* `basics.py` introduces `alt.Chart`, marks, encodings, sorting,
  color, size, tooltips, and simple filters.
* `portfolio_charts.py` turns the course portfolio files into Altair
  bar, rule, pie, and comparison charts.
* `interaction.py` shows point selections, interval brushes, hover
  highlights, linked charts, and an interactive legend.
* `transforms.py` shows aggregate, bin, calculate, fold, window, and
  top-k patterns.
* `composition.py` shows layers, horizontal and vertical composition,
  repeated charts, and facets.
* `gallery_explorer.py` collects a few classroom-sized examples by
  category.

The original Altair gallery has many more examples, including maps and
specialized projections.  Those are useful later, but they often depend
on geographic data files or external dataset URLs.  This section keeps
the first pass local and practical.

## Exercises

### Exercise 11.1: Encodings

Open `Work/Altair_Demos/basics.py`.  Find the scatter plot.  Change the
`color` encoding from stock name to gain or loss:

```python
color=alt.Color("change:Q", title="Gain/loss")
```

Notice how the same data can be read as categories or as values.

### Exercise 11.2: Tooltips

Add `return_pct` to a tooltip.  Format it as a percentage:

```python
alt.Tooltip("return_pct:Q", title="Return", format=".1%")
```

Tooltips are a good place for details that would clutter the main chart.

### Exercise 11.3: Filters

In `portfolio_charts.py`, add a sidebar widget that shows only winners
or losers.  Keep the filtering in ordinary Python before building the
chart.

### Exercise 11.4: Selections

In `interaction.py`, change the interval brush from the value chart to
the return chart.  Which linked view changes?

Selections are just another part of the chart specification.

### Exercise 11.5: Transforms

In `transforms.py`, change the top-k value from 3 to 5.  Read the
`transform_window()` call and find where the rank is computed.

Altair transforms are useful when a chart-specific calculation belongs
near the chart.

### Exercise 11.6: Composition

In `composition.py`, change one chart from vertical composition to
horizontal composition.  Keep the charts small enough that labels still
fit.

## Instructor Notes

Altair works best here as a next step after Section 10.  Start with
charts that students already understand from the portfolio app, then
show how Altair gives them more control.

Keep the vocabulary practical:

* A mark is the thing drawn.
* An encoding maps data to a visual property.
* A selection lets the user point at part of the data.
* A transform prepares data for a chart.

The maps in Altair's gallery are worth a separate lesson.  They are not
included in this first local set because they need geographic datasets
and projection details that would distract from the basic chart grammar.
