import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Load the data
with open('website_info.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Create a DataFrame
df = pd.DataFrame(data)

# Create numerical features
df['num_products'] = df['products_services'].apply(len)
df['num_social_media'] = df['social_media'].apply(len)

# Select features for analysis
features = ['num_products', 'num_social_media']
X = df[features]

# Normalize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Visualizations
plt.figure(figsize=(10, 6))
plt.scatter(X['num_products'], X['num_social_media'])
plt.xlabel('Number of Products/Services')
plt.ylabel('Number of Social Media Platforms')
plt.title('Number of Products/Services vs Number of Social Media Platforms')
for i, company in enumerate(df['url']):
    plt.annotate(company.split('//')[1].split('.')[0], (X['num_products'][i], X['num_social_media'][i]))
plt.tight_layout()
plt.show()

# Determine optimal number of clusters using elbow method
inertias = []
k_range = range(1, 6)
for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X_scaled)
    inertias.append(kmeans.inertia_)

# Plot elbow curve
plt.figure(figsize=(10, 6))
plt.plot(k_range, inertias, marker='o')
plt.xlabel('Number of clusters (k)')
plt.ylabel('Inertia')
plt.title('Elbow Method for Optimal k')
plt.tight_layout()
plt.show()

# Perform K-means clustering with optimal k (let's say k=3 for this example)
kmeans = KMeans(n_clusters=3, random_state=42)
df['Cluster'] = kmeans.fit_predict(X_scaled)

# Visualize clusters
plt.figure(figsize=(12, 8))
scatter = plt.scatter(X['num_products'], X['num_social_media'], c=df['Cluster'], cmap='viridis')
plt.xlabel('Number of Products/Services')
plt.ylabel('Number of Social Media Platforms')
plt.title('K-means Clustering Results')
plt.colorbar(scatter)
for i, txt in enumerate(df['url']):
    plt.annotate(txt.split('//')[1].split('.')[0], (X['num_products'][i], X['num_social_media'][i]))
plt.tight_layout()
plt.show()

