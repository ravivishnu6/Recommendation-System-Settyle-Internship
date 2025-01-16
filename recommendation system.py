import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Sample data: Products and user purchase history
products_data = {
    'ProductID': [1, 2, 3, 4, 5],
    'ProductName': ['Laptop', 'Smartphone', 'Headphones', 'Charger', 'Mouse'],
    'Category': ['Electronics', 'Electronics', 'Accessories', 'Accessories', 'Accessories']
}

user_data = {
    'UserID': [1, 2, 3],
    'PurchaseHistory': ['Laptop Charger', 'Smartphone Headphones', 'Mouse Charger']
}

# Load data into DataFrames
products_df = pd.DataFrame(products_data)
users_df = pd.DataFrame(user_data)

# Content-Based Filtering (TF-IDF on categories)
def content_based_recommendation(product_name, top_n=3):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(products_df['Category'])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    product_index = products_df[products_df['ProductName'] == product_name].index[0]
    similar_indices = cosine_sim[product_index].argsort()[-top_n - 1:-1][::-1]
    
    recommendations = products_df.iloc[similar_indices]['ProductName'].tolist()
    return recommendations

# Collaborative Filtering (Simple Jaccard Similarity on user history)
def collaborative_filtering(user_id, top_n=3):
    user_history = users_df[users_df['UserID'] == user_id]['PurchaseHistory'].values[0]
    history_set = set(user_history.split())

    scores = {}
    for _, row in products_df.iterrows():
        product_set = set(row['ProductName'].split())
        jaccard_score = len(history_set & product_set) / len(history_set | product_set)
        scores[row['ProductName']] = jaccard_score

    # Get top recommendations
    recommendations = sorted(scores, key=scores.get, reverse=True)[:top_n]
    return recommendations

# Testing the functions
if __name__ == "__main__":
    print("Content-Based Recommendations for 'Laptop':")
    print(content_based_recommendation('Laptop'))

    print("\nCollaborative Filtering Recommendations for UserID 1:")
    print(collaborative_filtering(1))
