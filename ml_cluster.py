from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

def cluster_unknown_errors(messages, n_clusters=2):
    if len(messages) < n_clusters:
        return {}

    vectorizer = TfidfVectorizer(stop_words="english")
    X = vectorizer.fit_transform(messages)

    model = KMeans(n_clusters=n_clusters, random_state=42)
    labels = model.fit_predict(X)

    clusters = {}
    for msg, label in zip(messages, labels):
        clusters.setdefault(label, []).append(msg)

    return clusters
