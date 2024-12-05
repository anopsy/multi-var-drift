import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

# Generate data
np.random.seed(42)
data = pd.DataFrame({
    'X': np.random.normal(loc=0, scale=1, size=1000),
    'Z': np.random.normal(loc=0, scale=1, size=1000),
    'Y': np.random.normal(loc=0, scale=1, size=1000)
})

# Create a dynamic correlation
corr_factor = st.slider('Correlation factor', min_value=-1.0, max_value=1.0, step=0.1, value=0.0)
data['Z'] = data['X'] * corr_factor + data['Z'] * (1 - abs(corr_factor))
data['Y'] = data['Z'] * corr_factor + data['Y'] * (1 - abs(corr_factor))

# Ensure the data is numeric
data['X'] = pd.to_numeric(data['X'], errors='coerce')
data['Z'] = pd.to_numeric(data['Z'], errors='coerce')
data['Y'] = pd.to_numeric(data['Y'], errors='coerce')

# Normalize the correlation factor for color mapping
norm = Normalize(vmin=-1, vmax=1)
colors = plt.cm.viridis(norm(corr_factor))

# Plotting
fig, ax = plt.subplots(2, 2, figsize=(12, 12), gridspec_kw={'width_ratios': [4, 1], 'height_ratios': [1, 4], 'wspace': 0.1, 'hspace': 0.1})
ax_scatter = ax[1, 0]
ax_histx = ax[0, 0]
ax_histy = ax[1, 1]

# Scatter plot with fixed axes
ax_scatter.scatter(data['Y'], data['Z'], color=colors)
ax_scatter.set_xlabel('Y')
ax_scatter.set_ylabel('Z')
ax_scatter.set_xlim(-3, 3)
ax_scatter.set_ylim(-3, 3)

# X distribution with fixed axes
sns.histplot(data['Y'], ax=ax_histx, kde=True, color="blueviolet")
#ax_histx.set_title('Multivariate Drift')
ax_histx.set_xlim(-3, 3)
ax_histx.set_xlabel('')
ax_histx.set_ylabel('Distribution of Y')

# Z distribution with fixed axes
sns.histplot(y=data['Z'], ax=ax_histy, kde=True, color="fuchsia")
#ax_histy.set_title('Distribution of Z')
ax_histy.set_ylim(-3, 3)
ax_histy.set_xlabel('Distribution of Z')
#ax_histy.set_ylabel('Distribution of Z',labelpad=0)


# Hide the empty subplot
ax[0, 1].axis('off')

# Add a color bar for reference
cbar = fig.colorbar(ax_scatter.collections[0], ax=ax, orientation='vertical', fraction=0.02, pad=0.04)
cbar.set_label('Correlation Factor')

st.pyplot(fig)
