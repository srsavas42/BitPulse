import praw
import pandas as pd
import datetime
import time
import logging
import signal
import sys

logging.basicConfig(level=logging.INFO)

'''
Each post and comment uses 1 API call, reddit allows 1000 calls every 10 minutes for each api key. 
You can have multiple api keys by creating multiple apps in the reddit developer console https://www.reddit.com/prefs/apps/ .
I have already downloaded data from CryptoCurrency, Bitcoin, BitcoinBeginners, Altcoin, CryptoMarkets, Ehtereum from the past 5 years using subreddit_instance.top and subreddit_instance.new, but most of the posts are from 2021 and 2024.
I only gathered 30 comments for each post.
If you want to gather more comments, change 
    post.comments.replace_more(limit=30)  
    comments = post.comments.list()[:30]  
'''



# TODO: Replace these with your Reddit app credentials
client_id = 'PLACEHOLDER'
client_secret = 'PLACEHOLDER'
user_agent = 'PLACEHOLDER'

# Initialize the Reddit instance
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent)

logging.info("Initialized Reddit API connection.")

# TODO: List of subreddits to fetch data from
subreddits = ['altcoin', 'bitcoinBeginners']


posts_data = []
comments_data = []

# TODO: Time period
five_years_ago = datetime.datetime.now() - datetime.timedelta(days=5*365)

post_count = 0

# Function to save data and exit
def save_data_and_exit(signal_received, frame):
    logging.info("Signal received. Saving data and exiting...")
    posts_df = pd.DataFrame(posts_data)
    comments_df = pd.DataFrame(comments_data)
    posts_df.to_csv('reddit_posts_5_years.csv', index=False)
    comments_df.to_csv('reddit_comments_5_years.csv', index=False)
    logging.info("Data saved to 'reddit_posts_5_years.csv' and 'reddit_comments_5_years.csv'")
    sys.exit(0)

# Handle interrupt signals
signal.signal(signal.SIGINT, save_data_and_exit)
signal.signal(signal.SIGTERM, save_data_and_exit)

for subreddit in subreddits:
    logging.info(f"Fetching data from subreddit: {subreddit}")
    subreddit_instance = reddit.subreddit(subreddit)
    for post in subreddit_instance.top(time_filter='all', limit=None):  # Adjust limit to avoid too many requests
    # for post in subreddit_instance.new(limit=None):
        # Rate limit check
        print(f"Limit: {reddit.auth.limits['remaining']}")
        if reddit.auth.limits['remaining'] < 50:
            logging.info(f"Rate limit exceeded, sleeping for 10 minutes.")
            time.sleep(601)

        post_created = datetime.datetime.fromtimestamp(post.created_utc)
        if post_created >= five_years_ago:
            post_count += 1
            logging.info(f"Processed {post_count} posts")
            # Log post details
            logging.info(f"Processing post ID: {post.id}, Title: {post.title}, Subreddit: {subreddit}, time: {post_created}")
            
            # Store post data
            posts_data.append({
                'title': post.title,
                'score': post.score,
                'id': post.id,
                'subreddit': post.subreddit.display_name,
                'url': post.url,
                'num_comments': post.num_comments,
                'body': post.selftext,
                'created': post_created,
                'timestamp': post.created_utc  # Add UNIX timestamp
            })

            # Retrieve and store up to 30 comments for each post
            try:
                post.comments.replace_more(limit=30)  # Fetch up to 30 additional comments
                comments = post.comments.list()[:30]  # Limit to the first 30 comments
                for comment in comments:
                    comments_data.append({
                        'post_id': post.id,
                        'comment_id': comment.id,
                        'comment_body': comment.body,
                        'comment_score': comment.score,
                        'comment_created': datetime.datetime.fromtimestamp(comment.created_utc),
                        'comment_timestamp': comment.created_utc,  # UNIX timestamp 
                        'subreddit': post.subreddit.display_name
                    })
            except Exception as e:
                logging.error(f"Error fetching comments for post ID {post.id}: {e}")



# Convert post and comment data to DataFrames
logging.info("Converting data to DataFrames.")
posts_df = pd.DataFrame(posts_data)
comments_df = pd.DataFrame(comments_data)

# Save to CSV files
posts_df.to_csv('BitcoinBeginners_Altcoin_top_posts_5_years.csv', index=False)
comments_df.to_csv('BitcoinBeginners_Altcoin_top_comments_5_years.csv', index=False)

logging.info("Data saved")
