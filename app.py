from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
import random
from flask_sqlalchemy import SQLAlchemy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load data
trending_products = pd.read_csv("models/trending_products.csv")
train_data = pd.read_csv("models/clean_data.csv")

# Flask configuration
app.secret_key = "alskdjfwoeieiurlskdjfslkdjf"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///ecom.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Models
class Signup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Signin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Create tables
with app.app_context():
    db.create_all()

# Utility: truncate long product names
def truncate(text, length):
    return text[:length] + "..." if len(text) > length else text

# Content-based recommender
def content_based_recommendations(train_data, item_name, top_n=10):
    if item_name not in train_data['Name'].values:
        return pd.DataFrame()

    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix_content = tfidf_vectorizer.fit_transform(train_data['Tags'])
    cosine_similarities_content = cosine_similarity(tfidf_matrix_content, tfidf_matrix_content)

    item_index = train_data[train_data['Name'] == item_name].index[0]
    similar_items = list(enumerate(cosine_similarities_content[item_index]))
    similar_items = sorted(similar_items, key=lambda x: x[1], reverse=True)[1:top_n+1]
    recommended_item_indices = [x[0] for x in similar_items]

    return train_data.iloc[recommended_item_indices][['Name', 'ReviewCount', 'Brand', 'ImageURL', 'Rating']]

# Static image URLs for UI
random_image_urls = [
    "static/img/img_1.png", "static/img/img_2.png", "static/img/img_3.png",
    "static/img/img_4.png", "static/img/img_5.png", "static/img/img_6.png",
    "static/img/img_7.png", "static/img/img_8.png",
]
price_list = [40, 50, 60, 70, 100, 122, 106, 50, 30, 50]

# Home route
@app.route("/")
def index():
    images = [random.choice(random_image_urls) for _ in range(len(trending_products))]
    return render_template('index.html', trending_products=trending_products.head(8),
                           truncate=truncate, random_product_image_urls=images,
                           random_price=random.choice(price_list))

# Redirect route
@app.route("/index")
def indexredirect():
    return redirect(url_for("index"))

# Main recommendation page
@app.route("/main")
def main():
    images = [random.choice(random_image_urls) for _ in range(8)]
    return render_template('main.html', content_based_rec=pd.DataFrame(), truncate=truncate,
                           random_product_image_urls=images, random_price=random.choice(price_list))

# Signup
@app.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        new_signup = Signup(username=username, email=email, password=password)
        db.session.add(new_signup)
        db.session.commit()

        images = [random.choice(random_image_urls) for _ in range(len(trending_products))]
        return render_template('index.html', trending_products=trending_products.head(8), truncate=truncate,
                               random_product_image_urls=images, random_price=random.choice(price_list),
                               signup_message='User signed up successfully!')
    return render_template("signup.html")  # Add a signup.html page if not yet created

# Signin
@app.route("/signin", methods=['POST', 'GET'])
def signin():
    if request.method == 'POST':
        username = request.form['signinUsername']
        password = request.form['signinPassword']

        new_signin = Signin(username=username, password=password)
        db.session.add(new_signin)
        db.session.commit()

        images = [random.choice(random_image_urls) for _ in range(len(trending_products))]
        return render_template('index.html', trending_products=trending_products.head(8), truncate=truncate,
                               random_product_image_urls=images, random_price=random.choice(price_list),
                               signup_message='User signed in successfully!')
    return render_template("signin.html")  # Add a signin.html page if not yet created

# Recommendations route
@app.route("/recommendations", methods=['POST', 'GET'])
def recommendations():
    if request.method == 'POST':
        prod = request.form.get('prod')
        nbr = int(request.form.get('nbr'))
        content_based_rec = content_based_recommendations(train_data, prod, top_n=nbr)

        if content_based_rec.empty:
            return render_template('main.html', content_based_rec=pd.DataFrame(),
                                   message="No recommendations available.",
                                   truncate=truncate, random_product_image_urls=[],
                                   random_price=0)
        else:
            images = [random.choice(random_image_urls) for _ in range(len(content_based_rec))]
            return render_template('main.html', content_based_rec=content_based_rec,
                                   truncate=truncate, random_product_image_urls=images,
                                   random_price=random.choice(price_list))
    return redirect(url_for("main"))

if __name__ == '__main__':
    app.run(debug=True)
