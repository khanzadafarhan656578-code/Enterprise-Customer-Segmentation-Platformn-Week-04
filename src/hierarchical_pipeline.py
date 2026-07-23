"""
Hierarchical Agglomerative Clustering Module
Enterprise Customer Segmentation Platform

Computes Ward's linkage matrix, generates publication-quality dendrograms with threshold lines,
runs Agglomerative Clustering, and compares performance with K-Means.
"""

import os
import sys
import time
from typing import Dict, Any, Tuple

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from sklearn.cluster import AgglomerativeClustering, KMeans
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score

from src.data_loader import DataLoaderPipeline

plt.style.use("seaborn-v0_8-whitegrid")


class HierarchicalPipeline:
    """
    Hierarchical Clustering Pipeline with Dendrogram generation and K-Means benchmark comparison.
    """

    def __init__(self, df_scaled: pd.DataFrame, output_dir: str = "charts", reports_dir: str = "reports"):
        self.df_scaled = df_scaled
        self.output_dir = output_dir
        self.reports_dir = reports_dir
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.reports_dir, exist_ok=True)

        self.feature_cols = [c for c in df_scaled.columns if c != "CUST_ID"]
        self.X = df_scaled[self.feature_cols].values
        self.linkage_matrix = None
        self.agglom_model = None

    def compute_linkage(self, method: str = "ward") -> np.ndarray:
        """
        Compute hierarchical linkage matrix on a representative subsample (4000 rows) for speed and clarity.
        """
        print(f"[HIERARCHICAL] Computing hierarchical linkage matrix (method='{method}')...")
        np.random.seed(42)
        idx = np.random.choice(len(self.X), size=min(4000, len(self.X)), replace=False)
        self.X_sample = self.X[idx]
        
        t0 = time.time()
        self.linkage_matrix = linkage(self.X_sample, method=method)
        t1 = time.time()
        print(f"[HIERARCHICAL] Linkage matrix computed in {t1 - t0:.2f} seconds.")
        return self.linkage_matrix

    def plot_dendrogram(self, max_d: float = 120.0):
        """
        Plot high-resolution publication-quality Dendrogram with horizontal cut threshold.
        """
        if self.linkage_matrix is None:
            self.compute_linkage()

        fig, ax = plt.subplots(figsize=(14, 8))
        
        # Truncate dendrogram for clean visualization (p=30 leaf nodes)
        dendrogram(
            self.linkage_matrix,
            truncate_mode="lastp",
            p=35,
            leaf_rotation=90.0,
            leaf_font_size=10.0,
            show_contracted=True,
            ax=ax
        )

        ax.set_title("Hierarchical Clustering Dendrogram (Ward Linkage Truncated)", pad=15)
        ax.set_xlabel("Cluster Sample Size (Leaf Nodes)")
        ax.set_ylabel("Euclidean Distance (Ward Linkage)")

        # Horizontal threshold cut line
        if max_d:
            ax.axhline(y=max_d, color="r", linestyle="--", linewidth=2, label=f"Cut Threshold (d = {max_d})")
            ax.legend(loc="upper right")

        filepath = os.path.join(self.output_dir, "dendrogram.png")
        plt.savefig(filepath, dpi=300, bbox_inches="tight")
        plt.close()
        print(f"[HIERARCHICAL] Saved dendrogram to {filepath}")

    def fit_agglomerative(self, n_clusters: int = 4) -> Tuple[AgglomerativeClustering, np.ndarray, Dict[str, float]]:
        """
        Fit Agglomerative Clustering and evaluate metrics.
        """
        print(f"[HIERARCHICAL] Fitting Agglomerative Clustering with n_clusters={n_clusters}...")
        t0 = time.time()
        self.agglom_model = AgglomerativeClustering(n_clusters=n_clusters, linkage="ward")
        labels = self.agglom_model.fit_predict(self.X)
        t1 = time.time()
        exec_time = t1 - t0

        sil = silhouette_score(self.X, labels, sample_size=3000, random_state=42)
        ch = calinski_harabasz_score(self.X, labels)
        db = davies_bouldin_score(self.X, labels)

        metrics = {
            "n_clusters": n_clusters,
            "Execution_Time_Sec": round(exec_time, 4),
            "Silhouette_Score": round(sil, 4),
            "Calinski_Harabasz": round(ch, 2),
            "Davies_Bouldin": round(db, 4)
        }
        print(f"[HIERARCHICAL] Agglomerative (K={n_clusters}) -> Silhouette: {sil:.4f}, CH: {ch:.2f}, DB: {db:.4f}, Time: {exec_time:.3f}s")
        return self.agglom_model, labels, metrics

    def generate_comparison_report(self, k: int = 4) -> pd.DataFrame:
        """
        Generate detailed comparison table between K-Means and Hierarchical Clustering.
        """
        # K-Means evaluation
        t0 = time.time()
        km = KMeans(n_clusters=k, random_state=42, n_init=20).fit(self.X)
        t1 = time.time()
        km_time = t1 - t0
        km_labels = km.labels_
        km_sil = silhouette_score(self.X, km_labels, sample_size=3000, random_state=42)
        km_ch = calinski_harabasz_score(self.X, km_labels)
        km_db = davies_bouldin_score(self.X, km_labels)

        # Hierarchical evaluation
        _, hc_labels, hc_metrics = self.fit_agglomerative(n_clusters=k)

        comparison_data = [
            {
                "Algorithm": "K-Means Clustering",
                "Clusters (K)": k,
                "Silhouette Score": round(km_sil, 4),
                "Calinski-Harabasz": round(km_ch, 2),
                "Davies-Bouldin": round(km_db, 4),
                "Execution Time (s)": round(km_time, 4),
                "Scalability": "High O(K*N*d)",
                "Memory Usage": "Low O(N)",
                "Interpretability": "High (Centroid-based)",
                "Business Recommendation": "Primary Production Model"
            },
            {
                "Algorithm": "Hierarchical (Ward Agglomerative)",
                "Clusters (K)": k,
                "Silhouette Score": round(hc_metrics["Silhouette_Score"], 4),
                "Calinski-Harabasz": round(hc_metrics["Calinski_Harabasz"], 2),
                "Davies-Bouldin": round(hc_metrics["Davies_Bouldin"], 4),
                "Execution Time (s)": round(hc_metrics["Execution_Time_Sec"], 4),
                "Scalability": "Medium O(N^2 log N)",
                "Memory Usage": "High O(N^2)",
                "Interpretability": "High (Dendrogram taxonomy)",
                "Business Recommendation": "Exploratory Taxonomy Benchmark"
            }
        ]

        df_comp = pd.DataFrame(comparison_data)
        csv_path = os.path.join(self.reports_dir, "clustering_comparison.csv")
        df_comp.to_csv(csv_path, index=False)
        print(f"[HIERARCHICAL] Saved clustering algorithm comparison to {csv_path}")
        return df_comp


if __name__ == "__main__":
    loader = DataLoaderPipeline()
    raw = loader.load_data()
    clean, scaled = loader.clean_and_preprocess()

    hierarchical_pipe = HierarchicalPipeline(scaled)
    hierarchical_pipe.compute_linkage()
    hierarchical_pipe.plot_dendrogram(max_d=120.0)
    df_comp = hierarchical_pipe.generate_comparison_report(k=4)
    print("\nModel Comparison Report:")
    print(df_comp.to_string(index=False))
