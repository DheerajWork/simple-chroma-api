# Install required package if not already installed
# pip install facebook-scraper

from facebook_scraper import get_posts

# Search for posts from a public page related to 'Asia Cup'
# Example: 'cricbuzz' page
page = 'cricbuzz'  # You can change this to other popular cricket pages

# Number of posts to fetch
number_of_posts = 20

# Search keyword
search_keyword = "India wins Asia Cup"

scraped_posts = []
for post in get_posts(page, pages=3):  # pages=3 means it will scan 3 pages worth of posts
    if search_keyword.lower() in post['text'].lower():
        scraped_posts.append({
            'post_text': post['text'],
            'post_time': str(post['time']),
            'post_url': post['post_url'],
        })
    if len(scraped_posts) >= number_of_posts:
        break

# Print results
for idx, post in enumerate(scraped_posts, 1):
    print(f"{idx}. Time: {post['post_time']}\nPost: {post['post_text']}\nURL: {post['post_url']}\n")
