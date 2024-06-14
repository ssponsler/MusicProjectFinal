import os
import features
import mfcc
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer

if __name__ == '__main__':
    print("clustering.py executed directly")
    cluster_folder('song.wav')

def cluster_folder(audio_dir):
    # get a list of all .wav files in the directory
    audio_files = [os.path.join(audio_dir, f) for f in os.listdir(audio_dir) if f.endswith('.wav')]

    # extract feature vectors for each audio file
    feature_vectors = []
    average_pitches = []
    for audio_file in audio_files:
        feature_vector, avg_pitch = mfcc.extract_features(audio_file)
        feature_vectors.append(feature_vector)
        average_pitches.append(avg_pitch)
        print(f"Finished retrieving feature vectors for {audio_file}.")

    # create a DataFrame from the feature vectors
    X = pd.DataFrame(feature_vectors)

    # replace missing values (NaN) with the mean of their associated columns
    imp = SimpleImputer(missing_values=np.nan, strategy='mean')
    X = imp.fit_transform(X)

    # set the desired number of clusters
    num_clusters = 7

    # initialize the k-means clustering model
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)

    # fit the model to the feature matrix
    kmeans.fit(X)

    # get the cluster labels for each song
    cluster_labels = kmeans.labels_

    # print the cluster assignments
    for i, label in enumerate(cluster_labels):
        print(f"Audio file {os.path.basename(audio_files[i])} belongs to cluster {label}")

    # analyze cluster centers (centroids)
    print("\nCluster centroids:")
    for i, centroid in enumerate(kmeans.cluster_centers_):
        print(f"Cluster {i}: {centroid}")

    # perform PCA to reduce dimensionality to 2 components
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X)

    # create a new DataFrame for plotting that includes PCA components and cluster labels
    plot_df = pd.DataFrame(X_pca, columns=['PC1', 'PC2'])
    plot_df['Cluster'] = cluster_labels

    # set up the matplotlib figure
    plt.figure(figsize=(20, 16))

    # plot density plots for each cluster
    for label in plot_df['Cluster'].unique():
        subset = plot_df[plot_df['Cluster'] == label]
        sns.kdeplot(data=subset, x='PC1', y='PC2', fill=True, levels=20, alpha=0.5, label=f'Cluster {label}')

    # plot scatter points on top of the density plot
    colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k']  # List of colors for each cluster
    for label, color in enumerate(colors):
        indices = np.where(cluster_labels == label)
        plt.scatter(X_pca[indices, 0], X_pca[indices, 1], c=color, label=f'Cluster {label}', alpha=0.5, s=50)

        # add text annotations for each point
        for i in indices[0]:
            file_name = os.path.basename(audio_files[i])
            avg_pitch = average_pitches[i]
            annotation = f"{file_name}\nPitch Vector: {avg_pitch:.2f}"
            plt.annotate(annotation, (X_pca[i, 0], X_pca[i, 1]), fontsize=8)

    plt.title("Density Plot with Scatter Points of Audio File Clusters")
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.legend()
    plt.tight_layout()
    plt.show()
