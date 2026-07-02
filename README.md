# Steam Games Exploratory Data Analysis & Dashboard

A Python and Flask project to analyze over 114k games in the Steam Games Dataset. Features a clean dark-mode dashboard with interactive charts (using ApexCharts) and a static fallback mode (Matplotlib).

---

## Quick Setup

### 1. Local Development (Flask App)
This runs the full Python server locally, which loads and processes the dataset in-memory.

1. **Install requirements**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Add the data**: Grab `games.csv` from [Kaggle](https://www.kaggle.com/datasets/fronkongames/steam-games-dataset) and place it in a `data/` folder in the root directory.
3. **Run it**:
   ```bash
   python app.py
   ```
   Open `http://localhost:5000` in your browser.

*Note: You can still run the Jupyter notebook (`steam_eda.ipynb`) locally for the raw EDA code.*

---

## The Comma-Shift CSV Bug (Important)

While parsing the Kaggle `games.csv` file, I found a weird formatting issue in the raw dataset:
* The header line is missing a comma between `Discount` and `DLC count` (it reads as `DiscountDLC count`).
* Because of this, the header line has 39 columns, but the data rows have 40 columns (since they actually have a comma there).
* In previous analyses, this caused pandas to treat column 0 (AppID) as the index, shifting all header names by 1 to the right. 
* This shift meant the `Price` column was actually reading the `Discount` column! That's why previous stats showed an incorrect median price of $51.00 (which was actually a median discount percentage of 51%).
* It also caused the date-filtering helper to throw out 99.9% of the top games (like CS2, Dota 2, and PUBG) because their game names shifted into the date columns and got parsed as dates.

**How it's fixed:** I manually defined the correct 40-column headers list in `app.py` and passed it as `names=cols` when loading the CSV, completely fixing the column alignment for all 122,611 rows.

---

## Corrected Key Metrics

With the CSV parsing fixed, the actual Steam dataset stats are:
* **Free-to-Play Ratio**: **15.67%** (17,902 out of 114,198 games) are actually free-to-play. (The old shifted parsing showed 64% free because it counted any game with "0% discount" as free).
* **Median Pricing**: The actual median price of paid games is **$3.49** (demonstrating the massive tail of low-cost indie games and budget titles on Steam). 90% of paid games in this dataset are under $12.00.
* **Price vs. Quality**: The correlation between a game's price and its positive rating ratio is near-zero (0.015), showing that price does not indicate better quality.
* **Top 15 Most Reviewed**: The most-reviewed chart is now correctly populated with global blockbusters (Counter-Strike 2, PUBG, Dota 2, etc.) instead of being empty.

---

## Visuals & Frontend
* **UI Theme**: Clean dark mode inspired by Steam, with glassmorphism panels.
* **Metrics count-up**: Smooth JS number count-up on load.
* **Interactive Mode (ApexCharts)**: Animated charts with custom hover tooltips showing game name, pricing, and exact ratings.
* **Static Mode**: A toggle in the header switches the layout to render the original Matplotlib/Seaborn static images.
* **Performance**: Sub-10ms response times because all data aggregation is cached in memory.



