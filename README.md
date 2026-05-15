# Steam Games Exploratory Data Analysis (EDA)

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458.svg)
![Seaborn](https://img.shields.io/badge/Seaborn-Visualization-blueviolet.svg)

An in-depth exploratory data analysis of the [Steam Games Dataset](https://www.kaggle.com/datasets/fronkongames/steam-games-dataset) from Kaggle. This project analyzes over 114,000 games to uncover key trends in pricing, genre popularity, user ratings, and community engagement.

## 📊 Key Findings

- **Indie Dominance**: The Indie genre is by far the most common, featuring over 80,000 games. This is nearly double the second most popular genre, Action (47,000 games).
- **Price ≠ Quality**: There is a near-zero correlation (0.015) between a game's price and its user rating. A higher price tag does not guarantee a better game on Steam!
- **Free-to-Play Landscape**: A staggering **64%** of all games on Steam are entirely free.
- **Pricing Clusters**: For paid games, pricing tends to cluster around standard psychological price points: $10, $15, $20, and $25.
- **Median Pricing**: The median price for a paid game is $51, indicating that while many cheap games exist, the majority of paid titles are priced above the $25 mark.

## 📈 Visualizations

The Jupyter Notebook (`steam_eda.ipynb`) includes several detailed visualizations to illustrate these findings:
1. **Top 15 Genres by Game Count** - Bar chart showing genre popularity.
2. **Price Distribution of Paid Games** - Histogram detailing how paid games are priced.
3. **Price vs. Rating Scatter Plot** - Filtered for games with 50+ reviews to showcase the lack of correlation between cost and quality.
4. **Top 15 Most Reviewed Games** - Highlighting the most engaged-with titles on the platform.
5. **Genre Volume vs. Average Rating** - A comparative look at the quantity of games in a genre versus their overall reception.

## 🚀 How to Run Locally

1. **Clone the repository**:
   ```bash
   git clone https://github.com/aaditya079/steam-eda.git
   cd steam-eda
   ```

2. **Install dependencies**:
   Make sure you have Python installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Download the Data**:
   Download the `games.csv` file from [Kaggle](https://www.kaggle.com/datasets/fronkongames/steam-games-dataset) and place it in the `data/` directory.

4. **Launch the Notebook**:
   ```bash
   jupyter notebook steam_eda.ipynb
   ```

## 🛠️ Tech Stack

- **Python**: Core programming language.
- **Pandas**: Data manipulation, aggregation, and cleaning.
- **Matplotlib & Seaborn**: Data visualization and plotting.

## 📁 Dataset

The dataset used for this project is the **Steam Games Dataset**, updated regularly on Kaggle:  
👉 [Steam Games Dataset — Kaggle](https://www.kaggle.com/datasets/fronkongames/steam-games-dataset)

---
*Developed as a data science portfolio project.*
