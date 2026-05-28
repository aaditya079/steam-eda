# Steam Games Exploratory Data Analysis (EDA) & Web Dashboard

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-Web_App-000000.svg)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458.svg)
![ApexCharts](https://img.shields.io/badge/ApexCharts-Interactive_Visualization-FF4560.svg)
![Seaborn](https://img.shields.io/badge/Seaborn-Static_Visualization-blueviolet.svg)

An in-depth exploratory data analysis and high-performance interactive web dashboard analyzing over 114,000 games on Steam, exploring pricing structures, genres, user ratings, and review density.

---

## 🔍 Critical Update: The Missing Comma Column-Shift Bug

During development, we discovered and resolved a major, structural column-shifting bug in how the raw Kaggle dataset (`data/games.csv`) was being parsed:
* **The Cause**: The CSV header line was missing a comma between `Discount` and `DLC count` (merged as `DiscountDLC count`). This left the header line with 39 columns while all 122k+ data rows had 40 columns.
* **The Impact**: Pandas automatically shifted the column headers. For 99.96% of the dataset, the **Game Name** was shifted into `AppID`, the **Release Date** was shifted into `Name`, and the **Discount Percentage** was loaded as the `Price`! Previous findings showing a median price of $51.00 were actually showing a median discount of 51%, and a date-filtering helper discarded 99.96% of games (including blockbusters like *Counter-Strike 2* and *Dota 2*).
* **The Fix**: We explicitly supplied a custom corrected column headers list to `pd.read_csv` to align all 122,611 rows with their true attributes.

---

## 📊 True Key Findings (Corrected)

With the parsing alignment fixed, the correct data benchmarks are:
* **True Free-to-Play Ratio**: Exactly **15.67%** (17,902 out of 114,198) of games on Steam are entirely free-to-play. 
* **True Median Pricing**: The actual median price of a paid game on Steam is **$3.49** (demonstrating the massive long-tail distribution of low-cost indie games and budget titles). In fact, 90% of paid titles retail for under $12.00.
* **Price ≠ Quality**: The correlation between a game's price and its positive rating ratio is near-zero (0.015), proving that price does not indicate better reception on Steam.
* **Indie Dominance**: The `Indie` genre is by far the most popular by volume, with over 80,000 games, followed by `Action` (~47,000 games).

---

## 💻 Web Dashboard Features

We have built a gorgeous, high-performance web dashboard to visualizes these findings:
* **Steam-Inspired Dark Theme**: Built with a sleek, glassmorphic layout using linear gradients of electric cyan and hot magenta.
* **Sub-10ms Response Times**: Loads the dataset once on server startup and caches calculated data payloads and charts, ensuring instantaneous page rendering.
* **ApexCharts Interactive Integration**: Fully animated horizontal and vertical bar charts, scatter plots with custom HTML hover tooltips displaying individual game names and coordinates, and a dual-axis volume vs. rating combo chart.
* **Dashboard View Switcher**: A centered header sliding switch that allows users to toggle seamlessly between **Interactive Charts (ApexCharts)** and the **Static Fallback (Matplotlib)**.
* **KPI Countup Animations**: Custom ease-out count-up numbers for all metrics on load.

---

## 🚀 Usage Methods

You can explore and run this dashboard in two different ways depending on your needs:

### Method 1: Run Locally (Full Flask Web Server)
This method launches a local development server that processes the raw dataset and serves dynamic, live requests.
1. **Setup Environment**:
   ```bash
   # Clone the repository
   git clone https://github.com/aaditya079/steam-eda.git
   cd steam-eda
   
   # Install dependencies
   pip install -r requirements.txt
   ```
2. **Download the Data**: Download the `games.csv` file from [Kaggle](https://www.kaggle.com/datasets/fronkongames/steam-games-dataset) and place it inside a folder named `data/`.
3. **Launch the Server**:
   ```bash
   python app.py
   ```
   Open your browser and navigate to `http://localhost:5000`.

*Note: You can also explore the raw exploratory steps in the Jupyter Notebook by running `jupyter notebook steam_eda.ipynb`.*

---

### Method 2: Host Statically (GitHub Pages Deployment)
Because GitHub Pages only supports static hosting (no active Python backend), we have implemented a **standalone static build mode**! 
1. **How it works**: When `app.py` is executed locally, it automatically outputs pre-aggregated, lightweight JSON files for all metrics and visualizations into `static/api/`.
2. **Relative Path Routing**: The root `index.html` detects if it is running on GitHub Pages and automatically routes data requests to fetch these local static JSON payloads relative to the repository base URL instead of querying the Flask server.
3. **How to enable on GitHub Pages**:
   - Go to your repository settings on GitHub.
   - Select **Pages** from the sidebar menu.
   - Under **Build and deployment**, set the source branch to `master` and the directory to `/ (root)`.
   - Click Save. Your dashboard will be hosted instantly at `https://<your-username>.github.io/steam-eda/` with full interactive ApexCharts and animated transitions!


