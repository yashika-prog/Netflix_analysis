# 🎬 Netflix Content Intelligence

An end-to-end Netflix catalog analysis — from raw CSV through Python EDA, Matplotlib dashboard, Jupyter notebook, and an interactive HTML visualization suite.

---

## 📁 Project Structure

```
├── netflix_movies__1_.csv            # Original raw dataset
├── netflix_analysis.py               # Standalone Python analysis script
├── netflix_analysis.ipynb            # Jupyter notebook (9 cells)
├── netflix_analysis_notebook.html    # Notebook exported as HTML (browser-ready)
├── netflix_analysis.png              # 12-panel Matplotlib dashboard (160 dpi)
├── Netflix_Visualizations.html       # Interactive visualization suite (3 sections)
└── README.md                         # This file
```

---

## 📊 Dataset Overview

| Property | Value |
|---|---|
| Source | `netflix_movies__1_.csv` |
| Total titles | 8,807 |
| Movies | 6,131 (69.6%) |
| TV Shows | 2,676 (30.4%) |
| Release year range | 1925 – 2021 |
| Date added range | 2008 – 2021 |
| Columns | 12 |
| Missing values | `director` (2,634), `cast` (825), `country` (831), `date_added` (10), `rating` (4), `duration` (3) |

### Column Reference

| Column | Type | Description |
|---|---|---|
| `show_id` | string | Unique title identifier |
| `type` | string | Movie / TV Show |
| `title` | string | Title name |
| `director` | string | Director(s) — 30% missing |
| `cast` | string | Cast list |
| `country` | string | Country of production |
| `date_added` | string | Date added to Netflix |
| `release_year` | int | Original production year |
| `rating` | string | Content rating (TV-MA, R, PG-13, etc.) |
| `duration` | string | Minutes (movies) or seasons (TV shows) |
| `listed_in` | string | Comma-separated genre tags |
| `description` | string | Short synopsis |

---

## 🔍 Key Insights

### Movies vs TV Shows
- Movies outnumber TV Shows **2.3:1** across the catalog
- Median movie runtime is **98 minutes** (sweet spot: 87–114 min)
- Most TV shows run only **1 season** — Netflix favors limited-run originals
- **TV-MA** is the dominant rating for both types

### Most Popular Genres
| Rank | Genre | Count |
|---|---|---|
| 1 | International Movies | 2,752 |
| 2 | Dramas | 2,427 |
| 3 | Comedies | 1,674 |
| 4 | International TV Shows | 1,351 |
| 5 | Documentaries | 869 |
| 6 | Action & Adventure | 859 |

Dramas and Comedies are the strongest **crossover genres** — appearing heavily in both Movies and TV Shows.

### Content Growth Trend

| Year | Movies Added | TV Shows Added | Total | YoY Growth |
|---|---|---|---|---|
| 2015 | 56 | 26 | 82 | — |
| 2016 | 253 | 176 | 429 | +423% |
| 2017 | 839 | 349 | 1,188 | +177% |
| 2018 | 1,237 | 412 | 1,649 | +39% |
| 2019 | 1,424 | 592 | **2,016** | +22% |
| 2020 | 1,284 | 595 | 1,879 | −7% |
| 2021 | 993 | 505 | 1,498 | −20% |

- **Peak year:** 2019 with 2,016 titles added
- **Fastest growth:** 2016→2017 (+177%) driven by global expansion
- **Decline from 2020:** pandemic-related production delays
- **Seasonal peak months:** January and October (awards season + holiday positioning)

### Country Production

| Rank | Country | Titles |
|---|---|---|
| 1 | United States | 3,690 |
| 2 | India | 1,046 |
| 3 | United Kingdom | 806 |
| 4 | Canada | 445 |
| 5 | France | 393 |
| 6 | Japan | 318 |
| 7 | Spain | 232 |
| 8 | South Korea | 231 |

The US produces more titles than the next **9 countries combined**, though Netflix's global-first strategy is evident in International Movies being the top genre.

---

## 📈 Deliverables

### `netflix_analysis.py` — Standalone Script
Run directly with Python. Produces `netflix_analysis.png`.

```bash
python netflix_analysis.py
```

**Sections:**
1. Load & Clean — date parsing, type splitting, duration extraction
2. Genre helpers — `get_genres()` Counter function
3. Trend data — yearly and monthly aggregations
4. Plot theme — Netflix-inspired dark palette
5. 12-panel Matplotlib figure (GridSpec layout)
6. Save at 160 dpi

---

### `netflix_analysis.ipynb` — Jupyter Notebook
9 cells designed for sequential execution with inline chart output.

| Cell | Content |
|---|---|
| 0 | Imports & dark theme (`%matplotlib inline`) |
| 1 | Load & clean — parse dates, split types, extract duration |
| 2 | Genre analysis — helper function + top-10 printout |
| 3 | Trend data — yearly adds & YoY growth calculation |
| 4 | Insight 1 — Movies vs TV Shows (4 inline charts) |
| 5 | Insight 2 — Most popular genres (3 inline charts) |
| 6 | Insight 3 — Release trends (2 inline charts) |
| 7 | Deep dives — Month / Countries / YoY growth |
| 8 | Export — saves full 12-panel `netflix_analysis.png` |
| 9 | Key insights summary table (Markdown) |

```bash
jupyter notebook netflix_analysis.ipynb
# or
jupyter lab netflix_analysis.ipynb
```

---

### `netflix_analysis_notebook.html` — Notebook HTML Export
The full Jupyter notebook rendered as a standalone HTML page — dark theme, monospace code cells, all 9 sections visible without Jupyter installed. Open in any browser.

---

### `Netflix_Visualizations.html` — Interactive Visualization Suite
Three-section scrollable page with sticky navigation, built in vanilla HTML/CSS/JS + Chart.js.

**Section 1 — Content Growth Over Years**
- Dual area chart: Movies vs TV Shows added per year (2013–2021)
- YoY growth rate bar chart (red = growth, teal = decline)
- Monthly additions heatmap (2016–2021) — color intensity encodes volume

**Section 2 — Genre Distribution**
- Donut chart — top 8 genres by share of catalog
- Ranked horizontal bars — all 15 genres with color gradient
- Grouped bar chart — Movie vs TV Show split per genre

**Section 3 — Country Production Map**
- SVG world map — countries colored by production volume; hover for exact title count
- Ranked horizontal bars — top 20 producing countries

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3 / pandas | Data loading, cleaning, aggregation |
| matplotlib | 12-panel static dashboard |
| Chart.js 4.4.1 | Interactive charts in HTML |
| Vanilla HTML / CSS / JS | Visualization suite UI |
| Google Fonts (Bebas Neue, DM Sans, DM Mono) | Typography |

---

## 🚀 How to Run

**Python script:**
```bash
pip install pandas matplotlib
python netflix_analysis.py
# → outputs netflix_analysis.png
```

**Jupyter notebook:**
```bash
pip install pandas matplotlib jupyter
jupyter notebook netflix_analysis.ipynb
# Run All Cells
```

**HTML files:**
Open `netflix_analysis_notebook.html` or `Netflix_Visualizations.html` directly in any modern browser — no server or dependencies needed. Place `netflix_movies__1_.csv` in the same directory as the Python files before running.

---

*Netflix Content Intelligence · netflix_movies__1_.csv · 8,807 titles · 1925–2021*
