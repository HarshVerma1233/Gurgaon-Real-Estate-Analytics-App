import plotly.express as px  
import streamlit as st    
import pandas as pd 
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title='Plotting Demo')

st.title('Analysis ')

st.header('Sector Price per Sqft Geomap')

new_df = pd.read_csv('/home/harsh/Downloads/Populating_ubuntu/dataset/data_viz.csv')

group_df = new_df.groupby('sector').mean(numeric_only=True)[['price','price_per_sqft','built_up_area','latitude','longitude']]

fig = px.scatter_mapbox(group_df, lat="latitude", lon="longitude", color="price_per_sqft", size='built_up_area',
                        color_continuous_scale=px.colors.cyclical.IceFire, zoom=10, 
                        mapbox_style="open-street-map")

st.plotly_chart(fig, use_container_width=True)

st.set_page_config(layout="centered")
st.header("Sector Features Word Cloud")

# 1. Load your 2-column dataset
@st.cache_data
def load_data():
    df = pd.read_csv('/home/harsh/Downloads/Populating_ubuntu/dataset/word_cloud_dataset.csv')
    
    df['sector'] = df['sector'].str.strip().str.title()
    df['features'] = df['features'].fillna('').astype(str)
    return df

df = load_data()

# 2. Setup the Sidebar or Main Page Dropdown Selector
sectors = sorted(df['sector'].unique())
selected_sector = st.selectbox("Choose a Sector:", sectors)

# 3. Filter and combine the text features for the chosen sector
filtered_df = df[df['sector'] == selected_sector]
combined_text = " ".join(filtered_df['features'].tolist())

# 4. Generate and display the cloud
if combined_text.strip():
    wordcloud = WordCloud(
        width=800, 
        height=400, 
        background_color='white', 
        colormap='viridis',
        collocations=False 
    ).generate(combined_text)

    # Plotting using Matplotlib
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    
    # Display the final image container in your Streamlit dashboard
    st.pyplot(fig)

st.header('Price VS Area')

choice = st.selectbox('Property: ',['flat', 'house', 'House and Flats'])

if choice == 'flat':
    fig2 = px.scatter(new_df[new_df['property_type'] == 'flat'], x ='built_up_area', y='price', color = 'bedRoom')
elif choice == 'house':
    fig2 = px.scatter(new_df[new_df['property_type'] == 'house'], x ='built_up_area', y='price', color = 'bedRoom')
else:
    fig2 = px.scatter(new_df, x ='built_up_area', y='price', color = 'bedRoom')

st.plotly_chart(fig2, use_container_width=True)

st.header('BHK in Sector')

df['sector'] = df['sector'].astype(str).str.strip().str.title()
new_df['sector'] = new_df['sector'].astype(str).str.strip().str.title()

# Adding an Overall choice to the select list. 
sector_option = new_df['sector'].unique().tolist()  
sector_option.insert(0, 'Overall')

choice2 = st.selectbox('Sector: ', sector_option)

if choice2 == 'Overall':
    fig2 = px.pie(new_df, names = 'bedRoom')
    
    st.plotly_chart(fig2, use_container_width=True)
else:
    fig2 = px.pie(new_df[new_df['sector'] == choice2], names= 'bedRoom')

    st.plotly_chart(fig2, use_container_width=True)

st.dataframe(new_df)

st.header('Side by Side BHK and Price Comparison! ')

fig3 = px.box(new_df[new_df['bedRoom'] <= 4], x='bedRoom', y= 'price')

st.plotly_chart(fig3)

st.header('Side by Side Distribution plot for Property Type')

fig3, ax = plt.subplots(figsize=(10, 4))

# One line handles both groups seamlessly using 'hue'
sns.histplot(
    data=new_df[new_df['property_type'].isin(['house', 'flat'])],
    x='price',
    hue='property_type',
    kde=True,
    multiple="layer",
    ax=ax
)

st.pyplot(fig3)