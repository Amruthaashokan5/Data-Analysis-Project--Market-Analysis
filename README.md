
# 🏃‍♂️ Sports Retail Market Analysis — SQL · Python · Power BI

End-to-end data analytics project that takes raw, messy e-commerce data for a sports & fitness retailer and turns it into an interactive Power BI dashboard covering **conversion performance, social media engagement, and customer sentiment**.

## 📌 Project Overview

This project simulates a real-world analytics workflow for an online sports equipment retailer selling ~20 products (hockey sticks, ski boots, yoga mats, etc.). The goal was to answer three core business questions:

1. **Where are customers dropping off in the purchase funnel, and which products convert best?**
2. **How is social/content engagement (views, clicks, likes) trending across products and content types?**
3. **What do customer reviews tell us about satisfaction, and how does sentiment break down by product?**

## 🛠️ Tech Stack

| Layer | Tools |
|---|---|
| Data Cleaning & Transformation | SQL Server (T-SQL) |
| Sentiment Analysis / Data Prep | Python |
| Visualization & Reporting | Power BI |

## 🗂️ Data Model

The project uses a star-schema-style set of tables:

- `dim_customers`, `dim_geography` — customer demographics & location
- `dim_products` — product catalog with price tiers
- `fact_customer_journey` — funnel events (View → Click → Drop-off → Purchase)
- `fact_engagement_data` — content engagement (views, clicks, likes by content type)
- `fact_customer_reviews` — customer reviews with rating, text, and sentiment scoring

## 🧹 Data Cleaning (SQL)

Raw source data had several real-world quality issues, each resolved with a dedicated query:

| Script | What it fixes |
|---|---|
| `01_join_customer_geography.sql` | Enriches customers with country/city via a LEFT JOIN on `GeographyID` |
| `02_price_categorization.sql` | Buckets products into Low (<$50) / Medium ($50–200) / High (>$200) price tiers using `CASE` |
| `03_clean_review_text.sql` | Strips inconsistent double-spacing from review text |
| `04_clean_engagement_data.sql` | Standardizes `ContentType` labels (e.g. "Socialmedia" → "SOCIAL MEDIA"), splits a combined `Views-Clicks` string into separate numeric columns, reformats dates, and filters out irrelevant "Newsletter" rows |
| `05_dedupe_customer_journey.sql` | Uses `ROW_NUMBER()` + `PARTITION BY` to detect and remove duplicate journey events, and imputes missing `Duration` values with the daily average via a window function (`AVG() OVER`) |

## 🐍 Sentiment Analysis (Python)

The cleaned `customer_reviews` table is pulled from SQL Server into Python (via `SQLAlchemy` + `pyodbc`), processed, and written back to both a CSV and a new SQL table:

1. **Sentiment scoring** — `NLTK`'s **VADER** (`SentimentIntensityAnalyzer`) computes a compound `SentimentScore` (-1 to 1) for each `ReviewText`.
2. **Sentiment categorization** — a custom rule combines the VADER score *and* the customer's star `Rating` to assign a `SentimentCategory`: Positive, Negative, Mixed Positive, Mixed Negative, or Neutral. Using both signals together (not just text sentiment) catches cases like a positively-worded review with a low rating, or vice versa.
3. **Sentiment bucketing** — scores are grouped into readable ranges (`SentimentBucket`): `0.5 to 1.0`, `0.0 to 0.49`, `-0.49 to 0.0`, `-1.0 to -0.5`.
4. **Output** — the enriched DataFrame is exported to `fact_customer_reviews_with_sentiment.csv` and loaded into a new `dbo.fact_customer_reviews_with_sentiment` table in SQL Server, which feeds the Customer Reviews Details page in Power BI.

**Libraries:** `pandas`, `nltk` (VADER), `sqlalchemy`, `pyodbc`

## 📊 Power BI Dashboard

The report has 4 connected pages, all filterable by **Year** and **Month**, with a product-level slicer:

1. **Overview** — high-level KPIs: 9.57% conversion rate, 9M views, 2M clicks, 414K likes, 3.69 avg. rating, with trends by month and product.

## Overview

2. **Conversion Details** — purchase funnel (View → Click → Drop-off → Purchase), monthly conversion rate trend, and a product × month conversion-rate matrix.


3. **Social Media Details** — views/clicks/likes trend over time, content-type performance (Blog, Social Media, Video), and a product × month engagement matrix.


4. **Customer Reviews Details** — sentiment category distribution, sentiment trend by month, and a rating-vs-review-count scatter plot by sentiment.


## 🔑 Key Insights

- Conversion rate fluctuates seasonally, peaking around **September (12.2%)** and dipping mid-year.
- **Hockey Stick** and **Ski Boots** are the top-converting products (~15% each); **Soccer Ball** and **Swim Goggles** convert lowest (~6%).
- Engagement (views) shows a **declining trend** across the year even as clicks/likes stay relatively flat — a potential content-fatigue signal worth investigating.
- The majority of reviews (~62%) skew **Positive**, with a smaller but notable share of Mixed Negative sentiment worth monitoring for at-risk products.

## 🔄 Pipeline Flow


SQL Server (raw tables)
   → SQL cleaning scripts (joins, categorization, text/date cleanup, dedup)
   → Python (pull via SQLAlchemy → VADER sentiment scoring → categorize/bucket)
   → fact_customer_reviews_with_sentiment.csv  +  new SQL table
   → Power BI (data model + 4-page report)


## 📁 Repo Structure


├── sql/
│   ├── 01_join_customer_geography.sql
│   ├── 02_price_categorization.sql
│   ├── 03_clean_review_text.sql
│   ├── 04_clean_engagement_data.sql
│   └── 05_dedupe_customer_journey.sql
├── python/
│   └── sentiment_analysis.py   # pulls reviews from SQL, scores with VADER, writes CSV + SQL table back
├── data/
│   └── fact_customer_reviews_with_sentiment.csv
├── powerbi/
│   └── Market_Analysis_Dashboard.pbix
└── README.md


## 🚀 How to Reproduce

1. Restore the source tables in SQL Server (or adapt scripts to your RDBMS of choice).
2. Run the SQL scripts in `sql/` in order to clean and transform the raw tables.
3. Run `python/sentiment_analysis.py` to generate the sentiment-scored review dataset.
4. Open `Market_Analysis_Dashboard.pbix` in Power BI Desktop, refresh the data source connections, and explore.
