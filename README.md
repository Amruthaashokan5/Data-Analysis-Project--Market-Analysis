# 🏃‍♂️ Sports Retail Market Analysis — SQL · Python · Power BI · GenAI

End-to-end data analytics project that takes raw, messy e-commerce data for a sports & fitness retailer and turns it into an interactive **5-page Power BI dashboard** covering **conversion performance, social media engagement, customer sentiment, and AI-generated business insights**.

## 📌 Project Overview

This project simulates a real-world analytics workflow for an online sports equipment retailer selling 20 products (hockey sticks, ski boots, yoga mats, etc.). The goal was to answer four core business questions:

1. **Where are customers dropping off in the purchase funnel, and which products convert best?**
2. **How is social/content engagement (views, clicks, likes) trending across products and content types?**
3. **What do customer reviews tell us about satisfaction, and how does sentiment break down by product?**
4. **What AI-generated insights and recommendations can be derived automatically from the sentiment data?**

## 🛠️ Tech Stack

| Layer | Tools |
|---|---|
| Data Cleaning & Transformation | SQL Server (T-SQL) |
| Sentiment Analysis / Data Prep | Python (pandas, NLTK VADER) |
| AI Insight Generation | Gemma 4 via OpenRouter |
| Visualization & Reporting | Power BI (DAX, Power Query) |

## 🗂️ Data Model

The project uses a star-schema-style set of tables:

- `dim_customers`, `dim_geography` — customer demographics & location
- `dim_products` — product catalog with price tiers
- `fact_customer_journey` — funnel events (View → Click → Drop-off → Purchase)
- `fact_engagement_data` — content engagement (views, clicks, likes by content type)
- `fact_customer_reviews` — customer reviews with rating, text, and sentiment scoring
- `fact_customer_reviews_with_sentiment` — enriched reviews with SentimentScore, SentimentCategory, SentimentBucket

## 🧹 Data Cleaning (SQL)

Raw source data had several real-world quality issues, each resolved with a dedicated query:

| Script | What it fixes |
|---|---|
| `01_join_customer_geography.sql` | Enriches customers with country/city via LEFT JOIN on `GeographyID` |
| `02_price_categorization.sql` | Buckets products into Low (<$50) / Medium ($50–200) / High (>$200) using `CASE` |
| `03_clean_review_text.sql` | Strips inconsistent double-spacing from review text using `REPLACE` |
| `04_clean_engagement_data.sql` | Standardizes `ContentType` labels, splits combined `Views-Clicks` field, reformats dates, filters out "Newsletter" rows |
| `05_dedupe_customer_journey.sql` | Uses `ROW_NUMBER()` + `PARTITION BY` to remove duplicates; imputes missing `Duration` with `AVG() OVER` window function |

## 🐍 Sentiment Analysis (Python)

The cleaned `customer_reviews` table is pulled from SQL Server into Python via `SQLAlchemy` + `pyodbc`, processed, and written back to both a CSV and a new SQL table:

1. **Sentiment scoring** — NLTK's **VADER** (`SentimentIntensityAnalyzer`) computes a compound `SentimentScore` (-1 to 1) for each `ReviewText`
2. **Sentiment categorization** — a custom rule combines the VADER score *and* the customer's star `Rating` to assign a `SentimentCategory`: Positive, Negative, Mixed Positive, Mixed Negative, or Neutral
3. **Sentiment bucketing** — scores grouped into readable ranges (`SentimentBucket`): `0.5 to 1.0`, `0.0 to 0.49`, `-0.49 to 0.0`, `-1.0 to -0.5`
4. **Output** — enriched DataFrame exported to `fact_customer_reviews_with_sentiment.csv` and loaded into `dbo.fact_customer_reviews_with_sentiment` in SQL Server

**Libraries:** `pandas`, `nltk` (VADER), `sqlalchemy`, `pyodbc`

## 🤖 AI Insight Generation (Gemma 4 via OpenRouter)

After sentiment analysis, **Gemma 4 via OpenRouter** was used to automatically generate business intelligence from the scored review data:

- **Executive Summary** — AI-generated summary of 1,363 reviews: avg rating 3.69/5, avg sentiment score 0.19, 61.6% positive sentiment
- **Business Insights** — positive reviews at 61.6% (840 reviews), negative at 16.6% (226 reviews)
- **Recommendations** — monitor negative reviews, track sentiment trends, analyse positive review drivers

These outputs are embedded directly into the Power BI dashboard's AI Insight page as structured tables.

**KPIs on AI Insight Page:** 1.363K Total Reviews · 3.69 Avg Rating · 0.19 Avg Sentiment Score · 840 Positive Reviews

## 📊 Power BI Dashboard — 5 Pages

All pages are filterable by **Year**, **Month**, and **Product Name** via cross-filtering slicers.

### Page 1 — Overview
High-level KPIs: **9.57% conversion rate**, **9M views**, **2M clicks**, **414K likes**, **3.69 avg rating**. Trends by month and product.

### Page 2 — Conversion Details
Purchase funnel (View → Click → Drop-off → Purchase), monthly conversion rate trend, and a product × month conversion-rate matrix.

### Page 3 — Social Media Details
Views/clicks/likes trend over time, content-type performance (Blog, Social Media, Video), and a product × month engagement matrix.

### Page 4 — Customer Reviews Details *(Updated)*
Sentiment category distribution bar chart, monthly sentiment trend line, review detail table, and a **donut chart** showing sentiment split:
- Positive: **61.63%** (840 reviews)
- Negative: **16.58%** (226 reviews)
- Mixed Negative: **14.38%** (196 reviews)
- Mixed Positive: **6.31%** (86 reviews)
- Neutral: **1.10%** (15 reviews)

### Page 5 — AI Insight *(NEW)*
AI-generated executive summary, business insights, and recommendations powered by **Gemma 4 via OpenRouter**, with 4 KPI cards: 1.363K reviews, 3.69 avg rating, 0.19 avg sentiment score, 840 positive reviews.

## 🔑 Key Insights

- Conversion rate peaks around **September (12.2%)** and dips mid-year — campaign timing matters
- **Hockey Stick** and **Ski Boots** are top-converting products (~15% each); **Soccer Ball** and **Swim Goggles** convert lowest (~6%)
- Engagement (views) shows a **declining trend** across the year even as clicks/likes stay flat — a potential content-fatigue signal
- **61.63% of reviews are Positive** with avg sentiment score 0.19 — overall sentiment is healthy
- **16.58% Negative reviews** (226 entries) warrant per-product monitoring for quality or service issues

## 🔄 Pipeline Flow

```
SQL Server (raw tables)
   → SQL cleaning scripts (joins, categorization, text/date cleanup, dedup)
   → Python (SQLAlchemy pull → VADER sentiment scoring → categorize/bucket)
   → fact_customer_reviews_with_sentiment.csv + new SQL table
   → Gemma 4 via OpenRouter (executive summary, insights, recommendations)
   → Power BI (5-page dashboard: Overview, Conversion, Social Media, Reviews, AI Insight)
```

## 📁 Repo Structure

```
├── sql/
│   ├── 01_join_customer_geography.sql
│   ├── 02_price_categorization.sql
│   ├── 03_clean_review_text.sql
│   ├── 04_clean_engagement_data.sql
│   └── 05_dedupe_customer_journey.sql
├── python/
│   └── sentiment_analysis.py
├── data/
│   └── fact_customer_reviews_with_sentiment.csv
├── powerbi/
│   └── Market_Analysis_Dashboard.pbix
├── screenshots/
│   ├── 01_Overview.png
│   ├── 02_Conversion_Details.png
│   ├── 03_Social_Media_Details.png
│   ├── 04_Customer_Reviews_Updated.png
│   └── 05_AI_Insight_Page.png
└── README.md
```

## 🚀 How to Reproduce

1. Restore the source tables in SQL Server (or adapt scripts to your RDBMS of choice)
2. Run the SQL scripts in `sql/` in order to clean and transform the raw tables
3. Run `python/sentiment_analysis.py` to generate the sentiment-scored review dataset
4. (Optional) Use Gemma 4 via OpenRouter to regenerate AI insights from the sentiment output
5. Open `powerbi/Market_Analysis_Dashboard.pbix` in Power BI Desktop, refresh data source connections, and explore

## 📜 Certifications

This project was updated after completing the **Dubai Future Foundation's 1 Million Prompters Program (2026)**, applied to build the AI Insight page using prompt engineering and Gemma 4 via OpenRouter.
