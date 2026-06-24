import streamlit as st
import pickle
import pandas as pd
import os 

st.set_page_config(
    page_title="Gurgaon Appartment Recommender",
    page_icon="🏡",
    layout="wide"
)

current_dir = os.path.dirname(__file__)

# 2. This dynamically links to the pickle file inside the same folder
location_df_path = os.path.join(current_dir, 'location_df.pkl')
cosine_sim1_path = os.path.join(current_dir, 'cosine_sim1.pkl')
cosine_sim2_path = os.path.join(current_dir, 'cosine_sim2.pkl')
cosine_sim3_path = os.path.join(current_dir, 'cosine_sim3.pkl')

# 3. Load them using the dynamic paths (always use 'rb' mode for loading pickles!)
location_df = pickle.load(open(location_df_path, 'rb'))
cosine_sim1 = pickle.load(open(cosine_sim1_path, 'rb'))
cosine_sim2 = pickle.load(open(cosine_sim2_path, 'rb'))
cosine_sim3 = pickle.load(open(cosine_sim3_path, 'rb'))

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
