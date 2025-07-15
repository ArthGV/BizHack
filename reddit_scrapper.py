import praw
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

reddit = praw.Reddit(
    client_id="lAEQursNAYjOYke1-KXaUA",
    client_secret="kjmVSk4KqvBj19jNTMIfISlI_diGJA",
    user_agent="brand_scraper_v1"
)

def get_subreddit_posts(subreddit, limit=500):
    """
    Get subreddit post from a subreddit
    """
    posts = []
    for submission in reddit.subreddit(subreddit).new(limit=limit):
        posts.append({
            "title": submission.title,
            "selftext": submission.selftext,
            "created_utc": submission.created_utc,
            "score": submission.score
        })
    return pd.DataFrame(posts)

def get_brand_posts(brand, subreddit="MakeupAddiction", limit=100):
    """
    Get subreddit post from a subreddit related to a specific brand
    """
    posts = []
    for submission in reddit.subreddit(subreddit).search(brand, limit=limit):
        posts.append({
            "title": submission.title,
            "score": submission.score,
            "num_comments": submission.num_comments,
            "created_utc": submission.created_utc,
            "url": submission.url,
            "selftext": submission.selftext
        })
    return posts

analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(posts):
    for post in posts:
        text = post["title"] + " " + post["selftext"]
        scores = analyzer.polarity_scores(text)
        post["sentiment"] = scores
    return posts

# import streamlit as st
# import pandas as pd
# import time

# st.title("Reddit Brand Marketing Dashboard")

# brand = st.text_input("Enter Brand", "L'Oreal")
# subreddit = st.text_input("Enter Subreddit", "beauty")
# limit = st.slider("Number of Posts to Fetch", 10, 200, 50)

# if st.button("Get Data"):
#     with st.spinner("Fetching posts..."):
#         posts = get_brand_posts(brand, subreddit, limit)
#         posts = analyze_sentiment(posts)
#         df = pd.DataFrame(posts)

#     st.success(f"Fetched {len(df)} posts")

#     st.write("Sample Posts")
#     st.dataframe(df[["title", "score", "num_comments", "sentiment"]])

#     # Sentiment distribution
#     sentiment_df = pd.json_normalize(df["sentiment"])
#     sentiment_df['compound_label'] = sentiment_df['compound'].apply(
#         lambda x: "positive" if x > 0.05 else ("negative" if x < -0.05 else "neutral")
#     )
#     st.write("Sentiment Distribution")
#     st.bar_chart(sentiment_df['compound_label'].value_counts())
