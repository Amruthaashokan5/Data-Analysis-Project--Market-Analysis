# pip install pandas nltk sqlalchemy pyodbc

import pandas as pd
import pyodbc
import nltk
from sqlalchemy import create_engine
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Download the VADER lexicon for sentiment analysis if not already present.
nltk.download('vader_lexicon')

# Define a function to fetch data from a SQL database using SQLAlchemy
def fetch_data_from_sql():
    engine = create_engine(
        "mssql+pyodbc://DESKTOP-KM4UJD9\\SQLEXPRESS/PortfolioProject_MarketingAnalytics"
        "?driver=SQL+Server&trusted_connection=yes"
    )
    
    # Define the SQL query to fetch customer reviews data
    query = "SELECT ReviewID, CustomerID, ProductID, ReviewDate, Rating, ReviewText FROM dbo.customer_reviews"
    
    # Execute the query and fetch the data into a DataFrame
    df = pd.read_sql(query, engine)
    
    # Return the fetched data as a DataFrame
    return df

# Fetch the customer reviews data from the SQL database
customer_reviews_df = fetch_data_from_sql()

# Initialize the VADER sentiment intensity analyzer for analyzing the sentiment of text data
sia = SentimentIntensityAnalyzer()

# Define a function to calculate sentiment scores using VADER
def calculate_sentiment(review):
    # Get the sentiment scores for the review text
    sentiment = sia.polarity_scores(review)
    # Return the compound score, which is a normalized score between -1 (most negative) and 1 (most positive)
    return sentiment['compound']

# Define a function to categorize sentiment using both the sentiment score and the review rating
def categorize_sentiment(score, rating):
    # Use both the text sentiment score and the numerical rating to determine sentiment category
    if score > 0.05:  # Positive sentiment score
        if rating >= 4:
            return 'Positive'        # High rating and positive sentiment
        elif rating == 3:
            return 'Mixed Positive'  # Neutral rating but positive sentiment
        else:
            return 'Mixed Negative'  # Low rating but positive sentiment
    elif score < -0.05:  # Negative sentiment score
        if rating <= 2:
            return 'Negative'        # Low rating and negative sentiment
        elif rating == 3:
            return 'Mixed Negative'  # Neutral rating but negative sentiment
        else:
            return 'Mixed Positive'  # High rating but negative sentiment
    else:  # Neutral sentiment score
        if rating >= 4:
            return 'Positive'        # High rating with neutral sentiment
        elif rating <= 2:
            return 'Negative'        # Low rating with neutral sentiment
        else:
            return 'Neutral'         # Neutral rating and neutral sentiment

# Define a function to bucket sentiment scores into text ranges
def sentiment_bucket(score):
    if score >= 0.5:
        return '0.5 to 1.0'    # Strongly positive sentiment
    elif 0.0 <= score < 0.5:
        return '0.0 to 0.49'   # Mildly positive sentiment
    elif -0.5 <= score < 0.0:
        return '-0.49 to 0.0'  # Mildly negative sentiment
    else:
        return '-1.0 to -0.5'  # Strongly negative sentiment

# Apply sentiment analysis to calculate sentiment scores for each review
customer_reviews_df['SentimentScore'] = customer_reviews_df['ReviewText'].apply(calculate_sentiment)

# Apply sentiment categorization using both text sentiment score and rating
customer_reviews_df['SentimentCategory'] = customer_reviews_df.apply(
    lambda row: categorize_sentiment(row['SentimentScore'], row['Rating']), axis=1)

# Apply sentiment bucketing to categorize scores into defined ranges
customer_reviews_df['SentimentBucket'] = customer_reviews_df['SentimentScore'].apply(sentiment_bucket)

# Display the first few rows of the DataFrame with sentiment scores, categories, and buckets
print(customer_reviews_df.head())

# Save the DataFrame with sentiment scores, categories, and buckets to Desktop
customer_reviews_df.to_csv(r'C:\Users\asus\Desktop\fact_customer_reviews_with_sentiment.csv', index=False)
print("CSV saved to Desktop successfully!")

# Save the results back to SQL Server using pyodbc directly
conn = pyodbc.connect(
    "Driver={SQL Server};"
    "Server=DESKTOP-KM4UJD9\\SQLEXPRESS;"
    "Database=PortfolioProject_MarketingAnalytics;"
    "Trusted_Connection=yes;"
)
cursor = conn.cursor()

# Drop table if it already exists and recreate fresh
cursor.execute("""
    IF OBJECT_ID('dbo.fact_customer_reviews_with_sentiment', 'U') IS NOT NULL
    DROP TABLE dbo.fact_customer_reviews_with_sentiment
""")

# Create the table with correct column types
cursor.execute("""
    CREATE TABLE dbo.fact_customer_reviews_with_sentiment (
        ReviewID          INT,
        CustomerID        INT,
        ProductID         INT,
        ReviewDate        DATE,
        Rating            INT,
        ReviewText        NVARCHAR(MAX),
        SentimentScore    FLOAT,
        SentimentCategory NVARCHAR(50),
        SentimentBucket   NVARCHAR(50)
    )
""")

# Insert each row into the table
for _, row in customer_reviews_df.iterrows():
    cursor.execute("""
        INSERT INTO dbo.fact_customer_reviews_with_sentiment
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
    row['ReviewID'],
    row['CustomerID'],
    row['ProductID'],
    row['ReviewDate'],
    row['Rating'],
    row['ReviewText'],
    row['SentimentScore'],
    row['SentimentCategory'],
    row['SentimentBucket']
    )

# Commit the transaction and close the connection
conn.commit()
cursor.close()
conn.close()
print("Table saved to SQL Server successfully!")