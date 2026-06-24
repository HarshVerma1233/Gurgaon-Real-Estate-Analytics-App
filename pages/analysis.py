import plotly.express as px  
import streamlit as st    
import pandas as pd 
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
import os  # <-- Step 1: Add OS module for relative path calculations

# Step 2: Single page config call at the very top handling title and structural wide layout
st.set_page_config(page_title='Plotting Demo', layout="centered")

st.title('Analysis')

st.header('Sector Price per Sqft Geomap')

# Step 3: Resolve dynamic cloud paths for datasets
current_dir = os.path.dirname(__file__)
# Moving one level up to look into your dataset/ folder
dataset_dir = os.path.join(os.path.dirname(current_dir), 'dataset')

data_viz_path = os.path.join(dataset_dir, 'data_viz.csv')
word_cloud_path = os.path.join(dataset_dir, 'word_cloud_dataset.csv')

new_df = pd.read_csv(data_viz_path)

group_df = new_df.groupby('sector').mean(numeric_only=True)[['price','price_per_sqft','built_up_area','latitude','longitude']]

fig_map = px.scatter_mapbox(group_df, lat="latitude", lon="longitude", color="price_per_sqft", size='built_up_area',
                        color_continuous_scale=px.colors.cyclical.IceFire, zoom=10, 
                        mapbox_style="open-street-map")

st.plotly_chart(fig_map, use_container_width=True)


st.header("Sector Features Word Cloud")

# Cache data reading to dramatically speed up page renders on Streamlit Cloud
@st.cache_data
def load_data():
    df = pd.read_csv(word_cloud_path)
    df['sector'] = df['sector'].str.strip().str.title()
    df['features'] = df['features'].fillna('').astype(str)
    return df

df = load_data()

sectors = sorted(df['sector'].unique())
selected_sector = st.selectbox("Choose a Sector:", sectors)

filtered_df = df[df['sector'] == selected_sector]
combined_text = " ".join(filtered_df['features'].tolist())

if combined_text.strip():
    wordcloud = WordCloud(
        width=800, 
        height=400, 
        background_color='white', 
        colormap='viridis',
        collocations=False 
    ).generate(combined_text)

    fig_wc, ax_wc = plt.subplots(figsize=(10, 5))
    ax_wc.imshow(wordcloud, interpolation='bilinear')
    ax_wc.axis('off')
    st.pyplot(fig_wc)

st.header('Price VS Area')

choice = st.selectbox('Property: ',['flat', 'house', 'House and Flats'])

if choice == 'flat':
    fig_scatter = px.scatter(new_df[new_df['property_type'] == 'flat'], x ='built_up_area', y='price', color = 'bedRoom')
elif choice == 'house':
    fig_scatter = px.scatter(new_df[new_df['property_type'] == 'house'], x ='built_up_area', y='price', color = 'bedRoom')
else:
    fig_scatter = px.scatter(new_df, x ='built_up_area', y='price', color = 'bedRoom')

st.plotly_chart(fig_scatter, use_container_width=True)

st.header('BHK in Sector')

df['sector'] = df['sector'].astype(str).str.strip().str.title()
new_df['sector'] = new_df['sector'].astype(str).str.strip().str.title()

sector_option = new_df['sector'].unique().tolist()  
sector_option.insert(0, 'Overall')

choice2 = st.selectbox('Sector: ', sector_option)

if choice2 == 'Overall':
    fig_pie = px.pie(new_df, names = 'bedRoom')
    st.plotly_chart(fig_pie, use_container_width=True)
else:
    fig_pie = px.pie(new_df[new_df['sector'] == choice2], names= 'bedRoom')
    st.plotly_chart(fig_pie, use_container_width=True)


st.header('Side by Side BHK and Price Comparison! ')

fig_box = px.box(new_df[new_df['bedRoom'] <= 4], x='bedRoom', y= 'price')
st.plotly_chart(fig_box, use_container_width=True)

st.header('Side by Side Distribution plot for Property Type')

fig_dist, ax_dist = plt.subplots(figsize=(10, 4))

sns.histplot(
    data=new_df[new_df['property_type'].isin(['house', 'flat'])],
    x='price',
    hue='property_type',
    kde=True,
    multiple="layer",
    ax=ax_dist
)

st.pyplot(fig_dist)