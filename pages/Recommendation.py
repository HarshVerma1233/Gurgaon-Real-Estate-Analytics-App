import streamlit as st
import pickle
import pandas as pd

st.set_page_config(
    page_title="Gurgaon Appartment Recommender",
    page_icon="🏡",
    layout="wide"
)

location_df = pickle.load(open(r'/home/harsh/Downloads/Populating_ubuntu/pages/location_df.pkl', 'rb'))

cosine_sim1 = pickle.load(open(r'/home/harsh/Downloads/Populating_ubuntu/pages/cosine_sim1.pkl', 'rb'))
cosine_sim2 = pickle.load(open(r'/home/harsh/Downloads/Populating_ubuntu/pages/cosine_sim2.pkl', 'rb'))
cosine_sim3 = pickle.load(open(r'/home/harsh/Downloads/Populating_ubuntu/pages/cosine_sim3.pkl', 'rb'))

def recommend_properties_with_scores(property_name, top_n=247):
    
    cosine_sim_matrix = cosine_sim1 + cosine_sim2 + cosine_sim3
    # cosine_sim_matrix = cosine_sim3
    
    # Get the similarity scores for the property using its name as the index
    sim_scores = list(enumerate(cosine_sim_matrix[location_df.index.get_loc(property_name)]))
    
    # Sort properties based on the similarity scores
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Get the indices and scores of the top_n most similar properties
    top_indices = [i[0] for i in sorted_scores[1:top_n+1]]
    top_scores = [i[1] for i in sorted_scores[1:top_n+1]]
    
    # Retrieve the names of the top properties using the indices
    top_properties = location_df.index[top_indices].tolist()
    
    # Create a dataframe with the results
    recommendations_df = pd.DataFrame({
        'PropertyName': top_properties,
        'SimilarityScore': top_scores
    })
    
    return recommendations_df

st.title('Select Location and Radius')
selected_loc = st.selectbox('Location: ', sorted(location_df.columns.tolist()))

radius = st.number_input('Radius in Kilometers: ')

if st.button('Search'):
    result_ser = location_df[location_df[selected_loc] < radius*1000][selected_loc].sort_values()
    
    for key, value in result_ser.items():
        st.text(str(key) + " " + str(round(value/1000)) + ' kms')

st.title('Recommend Appartment: ')
selected_appartment = st.selectbox('Select an appartment', sorted(location_df.index.to_list()))

if st.button('Recommend'):
    recommend = recommend_properties_with_scores(selected_appartment)
    st.dataframe(recommend, width='content')
