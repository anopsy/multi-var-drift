import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize


np.random.seed(42)
data = pd.DataFrame({
    'Z': np.random.normal(loc=0, scale=1, size=1000),
    'X': np.random.normal(loc=0, scale=1, size=1000),
    'Y': np.random.normal(loc=0, scale=1, size=1000)
})


corr_factor = st.slider('Correlation factor', min_value=-1.0, max_value=1.0, step=0.1, value=0.0)
data['X'] = data['Z'] * corr_factor + data['X'] * (1 - abs(corr_factor))
data['Y'] = data['X'] * corr_factor + data['Y'] * (1 - abs(corr_factor))


data['X'] = pd.to_numeric(data['X'], errors='coerce')
data['Z'] = pd.to_numeric(data['Z'], errors='coerce')
data['Y'] = pd.to_numeric(data['Y'], errors='coerce')


norm = Normalize(vmin=-1, vmax=1)
colors = plt.cm.viridis(norm(corr_factor))


fig, ax = plt.subplots(2, 2, figsize=(12, 12), gridspec_kw={'width_ratios': [4, 1], 'height_ratios': [1, 4], 'wspace': 0.2, 'hspace': 0.2})
ax_scatter = ax[1, 0]
ax_histx = ax[0, 0]
ax_histy = ax[1, 1]


ax_scatter.scatter(data['X'], data['Y'], color=colors)
ax_scatter.set_xlabel('X')
ax_scatter.set_ylabel('Y')
ax_scatter.set_xlim(-3, 3)
ax_scatter.set_ylim(-3, 3)


sns.histplot(data['Y'], ax=ax_histx, kde=True, color="blueviolet")
#ax_histx.set_title('Multivariate Drift')
ax_histx.set_xlim(-3, 3)
ax_histx.set_xlabel('')
ax_histx.set_ylabel('Distribution of X')


sns.histplot(y=data['Z'], ax=ax_histy, kde=True, color="fuchsia")
ax_histy.set_ylim(-3, 3)
ax_histy.set_xlabel('Distribution of X')


ax[0, 1].axis('off')


cbar = fig.colorbar(ax_scatter.collections[0], ax=ax, orientation='vertical', fraction=0.02, pad=0.04)
cbar.set_label('Correlation Factor')

st.pyplot(fig)
