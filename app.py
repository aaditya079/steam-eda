from flask import Flask, render_template, jsonify
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os

app = Flask(__name__)

DATA_PATH = 'data/games.csv'
OUTPUT_PATH = 'static/charts'
os.makedirs(OUTPUT_PATH, exist_ok=True)

# Keep data in memory so we don't reload a 380MB file on every single click
df_cache = None
stats_cache = {}
chart_cache = {}

def generate_charts(df):
    # Chart 1: Genre game counts
    genre_series = df['Genres'].str.split(',').explode().str.strip()
    top_genres = genre_series.value_counts().head(15)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_genres.values, y=top_genres.index, hue=top_genres.index, palette='viridis', legend=False)
    plt.title('Top 15 Genres by Number of Games')
    plt.xlabel('Game Count')
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_PATH}/top_genres.png', dpi=150)
    plt.close()

    # Chart 2: Price distribution for budget games
    paid = df[(df['Price'] > 0) & (df['Price'] <= 25)]
    plt.figure(figsize=(10, 5))
    sns.histplot(paid['Price'], bins=40, kde=True, color='steelblue')
    plt.title('Price Distribution of Paid Games (Under $25)')
    plt.xlabel('Price (USD)')
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_PATH}/price_dist.png', dpi=150)
    plt.close()

    # Chart 3: Price vs Rating scatter
    filtered = df[df['Total Reviews'] >= 50]
    plt.figure(figsize=(8, 5))
    sns.scatterplot(data=filtered, x='Price', y='Rating Ratio', alpha=0.3)
    plt.xlim(0, 60)
    plt.title('Price vs Rating Ratio (50+ reviews)')
    plt.xlabel('Price (USD)')
    plt.ylabel('Positive Rating Ratio')
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_PATH}/price_vs_rating.png', dpi=150)
    plt.close()

    # Chart 4: Absolute blockbusters (by review counts)
    top_reviewed = df.nlargest(15, 'Total Reviews')[['Name', 'Total Reviews']].copy()
    top_reviewed['Name'] = top_reviewed['Name'].str[:30]
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Total Reviews', y='Name', data=top_reviewed, hue='Name', palette='magma', legend=False)
    plt.title('Top 15 Most Reviewed Games on Steam')
    plt.xlabel('Total Reviews')
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_PATH}/top_reviewed.png', dpi=150)
    plt.close()

    # Chart 5: Dual axis volume vs average rating
    genre_df = df[df['Total Reviews'] >= 50].copy()
    genre_df = genre_df.assign(Genre=genre_df['Genres'].str.split(',')).explode('Genre')
    genre_df['Genre'] = genre_df['Genre'].str.strip()
    genre_stats = genre_df.groupby('Genre').agg(
        count=('Name', 'count'),
        avg_rating=('Rating Ratio', 'mean')
    ).sort_values('count', ascending=False).head(15)
    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax1.barh(genre_stats.index, genre_stats['count'], color='steelblue', alpha=0.6)
    ax1.set_xlabel('Game Count')
    ax2 = ax1.twiny()
    ax2.plot(genre_stats['avg_rating'], genre_stats.index, 'ro-')
    ax2.set_xlabel('Avg Rating Ratio')
    plt.title('Top 15 Genres — Volume vs Avg Rating')
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_PATH}/genre_rating.png', dpi=150)
    plt.close()

def init_app_data():
    global df_cache, stats_cache, chart_cache
    print("Pre-loading Steam dataset into memory...")
    
    # Note: The raw CSV has a broken header ("DiscountDLC count" is missing a comma).
    # We supply corrected columns manually to fix the shift and align the fields properly.
    cols = [
        'AppID', 'Name', 'Release date', 'Estimated owners', 'Peak CCU', 
        'Required age', 'Price', 'Discount', 'DLC count', 'About the game', 
        'Supported languages', 'Full audio languages', 'Reviews', 'Header image', 
        'Website', 'Support url', 'Support email', 'Windows', 'Mac', 'Linux', 
        'Metacritic score', 'Metacritic url', 'User score', 'Positive', 'Negative', 
        'Score rank', 'Achievements', 'Recommendations', 'Notes', 
        'Average playtime forever', 'Average playtime two weeks', 
        'Median playtime forever', 'Median playtime two weeks', 
        'Developers', 'Publishers', 'Categories', 'Genres', 'Tags', 
        'Screenshots', 'Movies'
    ]
    
    # Read only the 5 columns we actually care about to speed up parsing
    df = pd.read_csv(DATA_PATH, names=cols, header=0, usecols=['Name', 'Genres', 'Price', 'Positive', 'Negative'])
    df.dropna(subset=['Name', 'Genres', 'Price', 'Positive', 'Negative'], inplace=True)
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    df.dropna(subset=['Price'], inplace=True)
    df['Total Reviews'] = df['Positive'] + df['Negative']
    df['Rating Ratio'] = df['Positive'] / (df['Total Reviews'] + 1)
    df['Price Type'] = df['Price'].apply(lambda x: 'Free' if x == 0 else 'Paid')
    df_cache = df
    
    # Pre-generate static fallback charts on startup
    generate_charts(df)
    
    # Cache card stats
    stats_cache = {
        'total_games': len(df),
        'free_games': len(df[df['Price'] == 0]),
        'paid_games': len(df[df['Price'] > 0]),
        'median_price': round(df[df['Price'] > 0]['Price'].median(), 2)
    }
    
    # Pre-calculate data payloads for the interactive JS charts
    # 1. Genres count
    genre_series = df['Genres'].str.split(',').explode().str.strip()
    top_genres = genre_series.value_counts().head(15)
    chart_cache['top_genres'] = {
        'labels': top_genres.index.tolist(),
        'values': top_genres.values.tolist()
    }
    
    # 2. Budget price distribution
    paid = df[(df['Price'] > 0) & (df['Price'] <= 25)]
    bins = pd.cut(paid['Price'], bins=40)
    bin_counts = bins.value_counts().sort_index()
    bin_labels = [f"${r.left:.2f} - ${r.right:.2f}" for r in bin_counts.index]
    chart_cache['price_dist'] = {
        'labels': bin_labels,
        'values': bin_counts.values.tolist()
    }
    
    # 3. Price vs Rating scatter (sample to 1200 points to keep canvas snappy)
    filtered = df[df['Total Reviews'] >= 50]
    scatter_sample = filtered.sample(n=min(1200, len(filtered)), random_state=42)[['Price', 'Rating Ratio', 'Name']]
    scatter_sample = scatter_sample[scatter_sample['Price'] <= 60]
    chart_cache['price_vs_rating'] = [
        {'x': round(row['Price'], 2), 'y': round(row['Rating Ratio'], 3), 'name': row['Name']}
        for _, row in scatter_sample.iterrows()
    ]
    
    # 4. Top reviewed games
    top_reviewed = df.nlargest(15, 'Total Reviews')[['Name', 'Total Reviews']].copy()
    top_reviewed['Name'] = top_reviewed['Name'].str[:30]
    chart_cache['top_reviewed'] = {
        'labels': top_reviewed['Name'].tolist(),
        'values': top_reviewed['Total Reviews'].tolist()
    }
    
    # 5. Genre combo (volume vs rating)
    genre_df = df[df['Total Reviews'] >= 50].copy()
    genre_df = genre_df.assign(Genre=genre_df['Genres'].str.split(',')).explode('Genre')
    genre_df['Genre'] = genre_df['Genre'].str.strip()
    genre_stats = genre_df.groupby('Genre').agg(
        count=('Name', 'count'),
        avg_rating=('Rating Ratio', 'mean')
    ).sort_values('count', ascending=False).head(15)
    chart_cache['genre_rating'] = {
        'labels': genre_stats.index.tolist(),
        'counts': genre_stats['count'].tolist(),
        'ratings': [round(r, 3) for r in genre_stats['avg_rating'].tolist()]
    }
    print("Application data ready!")
    
    # Save static JSON files in static/api/ for GitHub Pages hosting
    static_api_path = 'static/api'
    os.makedirs(static_api_path, exist_ok=True)
    import json
    
    with open(f'{static_api_path}/stats.json', 'w', encoding='utf-8') as f:
        json.dump(stats_cache, f)
    with open(f'{static_api_path}/top-genres.json', 'w', encoding='utf-8') as f:
        json.dump(chart_cache['top_genres'], f)
    with open(f'{static_api_path}/price-dist.json', 'w', encoding='utf-8') as f:
        json.dump(chart_cache['price_dist'], f)
    with open(f'{static_api_path}/price-vs-rating.json', 'w', encoding='utf-8') as f:
        json.dump(chart_cache['price_vs_rating'], f)
    with open(f'{static_api_path}/top-reviewed.json', 'w', encoding='utf-8') as f:
        json.dump(chart_cache['top_reviewed'], f)
    with open(f'{static_api_path}/genre-rating.json', 'w', encoding='utf-8') as f:
        json.dump(chart_cache['genre_rating'], f)
    print("Static JSON files generated in static/api/!")

# Trigger dataset parsing immediately on import
init_app_data()

@app.route('/')
def index():
    return render_template('index.html', stats=stats_cache)

# REST APIs for frontend visualizations
@app.route('/api/stats')
def api_stats():
    return jsonify(stats_cache)

@app.route('/api/charts/top-genres')
def api_top_genres():
    return jsonify(chart_cache['top_genres'])

@app.route('/api/charts/price-dist')
def api_price_dist():
    return jsonify(chart_cache['price_dist'])

@app.route('/api/charts/price-vs-rating')
def api_price_vs_rating():
    return jsonify(chart_cache['price_vs_rating'])

@app.route('/api/charts/top-reviewed')
def api_top_reviewed():
    return jsonify(chart_cache['top_reviewed'])

@app.route('/api/charts/genre-rating')
def api_genre_rating():
    return jsonify(chart_cache['genre_rating'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)