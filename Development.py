from flask import Flask, request, redirect
import random
import string

app = Flask(__name)

# In-memory data store for URL mappings (You should use a database in production)
url_mappings = {}
user_tiers = {}  # User tier management

# Define tier-based request limits
tiers = {
    'Tier 1': 1000,
    'Tier 2': 100,
    # Define more tiers as needed
}

# Generate a random short URL
def generate_short_url():
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(6))  # You can adjust the length

# Shorten a URL
@app.route('/shorten', methods=['POST'])
def shorten_url():
    user = request.form['user']
    long_url = request.form['long_url']

    if user in user_tiers:
        tier = user_tiers[user]
        if tier in tiers and url_mappings.get(user, 0) >= tiers[tier]:
            return "Request limit exceeded for this tier."

    if long_url in url_mappings:
        return url_mappings[long_url]

    short_url = generate_short_url()
    url_mappings[long_url] = short_url
    url_mappings[user] = url_mappings.get(user, 0) + 1

    return short_url

# Redirect short URL to long URL
@app.route('/<short_url>')
def redirect_to_long_url(short_url):
    long_url = next((long for long, short in url_mappings.items() if short == short_url), None)
    if long_url:
        return redirect(long_url, code=302)
    else:
        return "Short URL not found."

if __name__ == '__main__':
    app.run()
