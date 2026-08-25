[Contents](../Contents.md) | [Streamlit Overview](00_Overview.md)

# 10.7 Streamlit Skill Material Guide

This repository has Streamlit skill material in both `.agents/` and
`.claude/`. In this checkout, both paths point to the same skill:

```text
.agents/skills/developing-with-streamlit
.claude/skills/developing-with-streamlit
```

Use the skill as an instructor reference library. Do not ask students
to memorize it. Instead, use the references to create short demos,
review checklists, and extension exercises after students have built
the basic portfolio dashboard.

## Core Class Path

Use these references for the main Section 10 exercises:

| Skill Material | Use in Class |
| --- | --- |
| `references/environment-setup.md` | Explain Python version, dependency setup, `uv`, and `streamlit run`. |
| `references/cli.md` | Demo app launch, command-line flags, cache clearing, and diagnostics. |
| `references/code-organization.md` | Keep the first app in one file; later discuss when to split data logic from UI. |
| `references/data-display.md` | Teach `st.dataframe`, `column_config`, charts, and value formatting. |
| `references/layouts.md` | Sidebar filters stay in the sidebar; tables, charts, and metrics stay in the main page. |
| `references/dashboards.md` | Turn the portfolio report into a dashboard with KPI metrics and charts. |
| `references/performance.md` | Add `@st.cache_data` and discuss reruns. |

## Design and Interaction Extensions

Use these for short enhancement labs after Exercise 10.5:

| Skill Material | Extension Exercise |
| --- | --- |
| `references/design.md` | Polish the app title, captions, icons, status messages, and empty states. |
| `references/markdown.md` | Add Markdown labels, badges, and a short formula explanation for gain/loss. |
| `references/selection-widgets.md` | Compare `multiselect`, `pills`, `segmented_control`, `toggle`, and forms. |
| `references/session-state.md` | Add a reset button, remember a selected stock, or store student-created notes. |
| `references/theme.md` | Create `.streamlit/config.toml` and apply a theme deliberately. |
| `assets/templates/themes/README.md` | Let students choose from provided theme configs and critique readability. |

Suggested exercise sequence:

1. Replace the sidebar `multiselect` with `st.pills` when there are few stocks.
2. Add a `st.toggle("Show losers only")` filter.
3. Add a reset button that clears `st.session_state`.
4. Add a status badge such as `:red[Loss]` or `:green[Gain]`.
5. Apply one theme config and check contrast, table readability, and chart colors.

## Larger App Extensions

Use these references when students are ready to move beyond a single-file
dashboard:

| Skill Material | Extension Exercise |
| --- | --- |
| `references/multipage-apps.md` | Split the portfolio app into Dashboard, Data, and Notes pages. |
| `references/chat-ui.md` | Add a mock portfolio-help chat page that answers from static rules or canned examples. |
| `references/third-party-components.md` | Discuss when community components are useful and when they add maintenance risk. |
| `references/snowflake-connection.md` | Optional data-engineering demo: replace CSV loading with `st.connection`. |
| `assets/templates/apps/README.md` | Compare finished dashboard patterns before students design a capstone. |

Suggested capstone options:

* Adapt `dashboard-stock-peers` patterns to compare stocks in `prices.csv`.
* Adapt `dashboard-metrics` patterns to show portfolio totals over hypothetical time ranges.
* Adapt `dashboard-companies` patterns to build a sortable stock leaderboard.
* Adapt `dashboard-seattle-weather` as a non-finance example for students who want a second dataset.

## Custom Component Extensions

Custom components are advanced material. Use them only after students
are comfortable with normal Streamlit widgets and callbacks.

| Skill Material | Use in Class |
| --- | --- |
| `references/custom-components-v2.md` | Explain when native Streamlit widgets are not enough. |
| `references/ccv2-state-sync.md` | Teach the Python-to-JavaScript state loop. |
| `references/ccv2-theme-css-variables.md` | Show how custom components should inherit Streamlit theme tokens. |
| `references/ccv2-packaged-components.md` | Use only for a serious packaged component project. |
| `references/ccv2-troubleshooting.md` | Turn into a debugging checklist for component labs. |

Good classroom rule: try native Streamlit first. Move to a custom
component only for interactions that do not exist as native widgets,
such as drawing, drag-and-drop, or specialized JavaScript visualization.

## Instructor Checklist

Before teaching a Streamlit exercise, check:

* The app starts with `streamlit run Work/streamlit_app.py`.
* Data-loading functions skip blank CSV rows.
* Streamlit calls do not use deprecated `use_container_width`.
* Sidebar contains filters, not the main data display.
* Tables use `hide_index=True` and currency formatting where helpful.
* Empty filter results show a friendly message instead of an empty chart.
* `@st.cache_data` is used for CSV loading after students understand reruns.
* Optional advanced labs are labeled clearly so they do not derail the core Python course.
