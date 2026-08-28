"""Exploratory analysis of the Udacity exoplanet dataset.

This script examines exoplanet characteristics, discovery trends,
correlations, and changes in summary statistics over time.
"""

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import seaborn as sns

DATA_FILE = "udacity_exoplanet.csv"
exoplanets = pd.read_csv(DATA_FILE)

# =============================================================================
# INITIAL DATA INSPECTION
# =============================================================================

print("\nFirst five rows:")
print(exoplanets.head())

print("\nDataset dimensions:")
print(exoplanets.shape)

print("\nColumn names:")
print(exoplanets.columns.tolist())

print("\nDataset information:")
exoplanets.info()

print("\nSummary statistics:")
print(exoplanets.describe())

print("\nMissing values by column:")
print(exoplanets.isna().sum())

print("\nNumber of duplicated rows:")
print(exoplanets.duplicated().sum())

number_of_rows, number_of_columns = exoplanets.shape

print(
    f"\nThe dataset contains {number_of_rows:,} exoplanets "
    f"and {number_of_columns} variables."
)

# =============================================================================
# PLANET AND HOST STAR ANALYSIS
# =============================================================================

number_of_planets = exoplanets["pl_name"].nunique()
number_of_hosts = exoplanets["hostname"].nunique()

print(f"\nThe dataset contains {number_of_planets:,} exoplanets ")
print(f"The dataset contains {number_of_hosts:,} hosts")

host_counts = exoplanets["hostname"].value_counts()
print(f"\nStars with the most orbiting planets discovered: {host_counts.head(10)}\n")

multi_planet_hosts = host_counts[host_counts > 1]
print(f"\nThe number of multi-planetary star systems:"
      f"{len(multi_planet_hosts)}")

# =============================================================================
# PLANET-RADIUS DISTRIBUTION
# =============================================================================

plt.figure(figsize=(8, 5))

plt.hist(
    exoplanets["pl_rade"],
    bins=25,
    edgecolor="black",
    alpha=0.7
)

plt.title("Distribution of Exoplanet Radii")
plt.xlabel("Planet Radius (Earth Radii)")
plt.ylabel("Number of Planets")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.show()

# =============================================================================
# EXOPLANET DISCOVERIES BY YEAR
# =============================================================================

discoveries_per_year = (
    exoplanets["disc_year"]
    .value_counts()
    .sort_index()
)

print("\nDiscoveries per year:")
print(discoveries_per_year)

plt.figure(figsize=(10, 5))

plt.bar(
    discoveries_per_year.index,
    discoveries_per_year.values,
    color="steelblue",
    edgecolor="black",
    alpha=0.7
)

plt.title("Exoplanet Discoveries by Year")
plt.xlabel("Discovery Year")
plt.ylabel("Number of Discoveries")
plt.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.show()

# Discovery counts peaked in 2014.
# This surge may have been driven by Kepler mission data releases.

# =============================================================================
# INTERACTIVE RADIUS AND MASS ANALYSIS
# =============================================================================

fig = px.scatter(
    exoplanets,
    x="pl_rade",
    y="pl_bmasse",
    color="disc_year",
    hover_data=["pl_name"],
    title="Relationship Between Exoplanet Radius and Mass",
    labels={
        "pl_rade": "Planet Radius (Earth Radii)",
        "pl_bmasse": "Planet Mass (Earth Masses)",
        "disc_year": "Discovery Year",
        "pl_name": "Planet Name"
    }
)

fig.show()

# =============================================================================
# SUMMARY STATISTICS AND CORRELATION ANALYSIS
# =============================================================================

summary_columns = ["pl_rade", "pl_bmasse", "pl_orbper"]

print("\nSummary statistics for planet characteristics:")
print(exoplanets[summary_columns].describe())

correlation_matrix = exoplanets[summary_columns].corr()

correlation_labels = {
    "pl_rade": "Planet Radius",
    "pl_bmasse": "Planet Mass",
    "pl_orbper": "Orbital Period"
}

correlation_matrix = correlation_matrix.rename(
    index=correlation_labels,
    columns=correlation_labels
)

plt.figure(figsize=(7, 6))

sns.heatmap(
    correlation_matrix,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    vmin=-1,
    vmax=1,
    center=0
)

plt.title("Correlation Between Exoplanet Characteristics")
plt.tight_layout()
plt.show()

# =============================================================================
# PLANET CHARACTERISTICS OVER TIME
# =============================================================================

radius_by_year = exoplanets.groupby("disc_year")["pl_rade"].mean()
mass_by_year = exoplanets.groupby("disc_year")["pl_bmasse"].mean()

plt.figure(figsize=(10, 5))

plt.bar(
    mass_by_year.index,
    mass_by_year.values,
    color="limegreen",
    edgecolor="black",
    alpha=0.7
)

plt.title("Mean Planet Mass by Discovery Year")
plt.xlabel("Discovery Year")
plt.ylabel("Mean Planet Mass (Earth Masses)")
plt.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.show()


radius_stats = exoplanets.groupby("disc_year")["pl_rade"].agg(
    ["mean", "median"]
)

plt.figure(figsize=(10, 5))

plt.plot(
    radius_stats.index,
    radius_stats["mean"],
    marker="o",
    label="Mean Radius"
)

plt.plot(
    radius_stats.index,
    radius_stats["median"],
    marker="o",
    label="Median Radius"
)

plt.title("Mean and Median Planet Radius by Discovery Year")
plt.xlabel("Discovery Year")
plt.ylabel("Planet Radius (Earth Radii)")
plt.legend()
plt.grid(alpha=0.3)

plt.tight_layout()
plt.show()

# =============================================================================
# 3D VISUALISATION OF PLANET CHARACTERISTICS
# =============================================================================

fig = px.scatter_3d(
    exoplanets,
    x="pl_bmasse",
    y="pl_rade",
    z="pl_orbper",
    color="disc_year",
    hover_name="pl_name",
    hover_data=[
        "hostname",
        "discoverymethod"
    ],
    title="Planet Mass, Radius and Orbital Period",
    labels={
        "pl_bmasse": "Planet Mass (Earth Masses)",
        "pl_rade": "Planet Radius (Earth Radii)",
        "pl_orbper": "Orbital Period (Days)",
        "disc_year": "Discovery Year",
        "hostname": "Host Star",
        "discoverymethod": "Discovery Method"
    },
    log_z=True
)

fig.show()