import streamlit as st
import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import KFold, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler, OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.svm import SVR

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

from sklearn.decomposition import PCA

st.set_page_config(page_title = 'ViZ Demo')

with open ('/home/harsh/Downloads/Populating_ubuntu/pages/df.pkl','rb') as file:
    df = pickle.load(file)

with open ('/home/harsh/Downloads/Populating_ubuntu/pages/pipeline.pkl','rb') as file:
    pipeline = pickle.load(file)


st.header('Enter your Inputs - ')

# Property Type
property_type = st.selectbox('Property Type', ['house', 'flat'])

# Sector
sector = st.selectbox('Sector ', sorted(df['sector'].unique().tolist()))

#Bedroom and Bathroom
bedroom = float(st.selectbox('Number of Bed Room', sorted(df['bedRoom'].unique().tolist())))
bathroom = float(st.selectbox('Number of Bath Room', sorted(df['bathroom'].unique().tolist())))

# Balcony
balcony = st.selectbox('Number of Balcony', sorted(df['balcony'].unique().tolist()))

#Age Possession
property_age = st.selectbox('Property Age', sorted(df['agePossession'].unique().tolist()))  

#Built-up Area
built_up_area = float(st.number_input('Built Area')) 

# Servant Room and Store Room
# gg = {'Yes':1, 'No':0}
servant_room = st.selectbox('Servant Room', [1.0,0.0])
store_room = st.selectbox('Store Room', [0.0,1.0])

# Furshing Type
furnishing_type = st.selectbox(
    'Furnishing Type',
    sorted(df['furnishing_type'].unique().tolist())
)

#Luxury Category
luxury_category = st.selectbox('Luxury Type', df['luxury_category'].unique().tolist())

#Floor Number
floor_number = st.selectbox('Floor Number', df['floor_category'].unique().tolist())

if st.button('Predict'):

    #make a dataframe --> predict --> display
    

    data = [[property_type, sector, bedroom, bathroom, balcony, property_age, built_up_area, servant_room, store_room, 
             furnishing_type, luxury_category, floor_number]]
    columns = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
        'agePossession', 'built_up_area', 'servant room', 'store room',
        'furnishing_type', 'luxury_category', 'floor_category']

    # Convert to DataFrame
    one_df = pd.DataFrame(data, columns=columns)

    st.dataframe(one_df)

    # predict
    base_price = np.expm1(pipeline.predict(one_df))[0]
    low = base_price - 0.22
    high = base_price + 0.22

    # display
    st.text("Range of Price for the given flat is {} Cr and {} Cr".format(round(low,2), round(high,2)))