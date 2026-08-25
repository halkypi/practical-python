# Altair demo apps

Run these from the repository root.

| App | Run command | Purpose |
| --- | --- | --- |
| Basics | `streamlit run Work/Altair_Demos/basics.py` | Introduces Altair marks, encodings, sorting, color, size, tooltips, and filters. |
| Portfolio charts | `streamlit run Work/Altair_Demos/portfolio_charts.py` | Builds practical portfolio charts from `Work/Data/portfolio.csv` and `Work/Data/prices.csv`. |
| Interaction | `streamlit run Work/Altair_Demos/interaction.py` | Shows selections, brushes, hover highlights, linked charts, and interactive legends. |
| Transforms | `streamlit run Work/Altair_Demos/transforms.py` | Shows aggregate, bin, calculate, fold, window, rank, and top-k transforms. |
| Composition | `streamlit run Work/Altair_Demos/composition.py` | Shows layers, chart concatenation, repeated views, and facets. |
| Gallery explorer | `streamlit run Work/Altair_Demos/gallery_explorer.py` | A small classroom explorer inspired by the larger Altair gallery. |

These demos use local course data first.  A few examples add compact
synthetic rows when interaction or composition needs more points.

Map examples are intentionally left out of the first pass.  Altair's map
gallery is excellent, but those examples usually need topojson files,
geographic datasets, or external data URLs.
