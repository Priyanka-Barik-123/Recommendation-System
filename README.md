# Recommendation-System
E-Commerce Product Recommendation System
This is a Flask-based web application that provides smart product recommendations using machine learning. The system analyzes product metadata and customer reviews to recommend similar products to users, enhancing the online shopping experience.

🚀 Features
🔍 Content-Based Filtering using product features

🧠 Machine Learning model (TF-IDF + Cosine Similarity)

🗂️ Product dataset from Amazon/Walmart

🧾 Review text cleaning with spaCy

🔐 User Signup & Login (SQLite)

💻 Frontend: HTML, CSS, Bootstrap

🌐 Backend: Python Flask

📂 Project Structure
arduino
Copy
Edit
├── app.py
├── model.pkl
├── templates/
│   ├── home.html
│   ├── product.html
│   └── login.html
├── static/
│   └── styles.css
├── dataset/
│   ├── amazon.csv
│   └── Test_data.csv
├── requirements.txt
└── README.md
📊 ML Workflow
Data Cleaning & Preprocessing

TF-IDF Vectorization of product descriptions

Cosine Similarity for recommendations

Flask app to serve recommendations based on user input

💻 How to Run
bash
Copy
Edit
git clone https://github.com/yourusername/product-recommendation-system.git
cd product-recommendation-system
pip install -r requirements.txt
python app.py
Then open http://127.0.0.1:5000/ in your browser.

🧠 Future Enhancements
Collaborative filtering

Add-to-cart & purchase simulation

User behavior tracking

Real-time product search and filtering

📌 Tech Stack
Python, Flask

Pandas, NumPy, scikit-learn, spaCy

HTML/CSS, Bootstrap

SQLite

