import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from fuzzywuzzy import process

@st.cache_data
def load_data():
    df = pd.read_csv('books.csv')
    tfidf = TfidfVectorizer(stop_words='english')
    df['description'] = df['description'].fillna('')
    tfidf_matrix = tfidf.fit_transform(df['description'])
    cosine_similarity = linear_kernel(tfidf_matrix)
    indices = pd.Series(df.index, index=df['title']).drop_duplicates()
    return df, cosine_similarity, indices

df, cosine_similarity, indices = load_data()

def get_closest_title(input_title, titles):
    """Find the closest matching title in the dataset"""
    closest_match = process.extractOne(input_title, titles)
    return closest_match[0] if closest_match[1] >= 60 else None

def get_book_recommendation(input_title, cos_similarity=cosine_similarity):
    title = get_closest_title(input_title, df['title'])

    if title is None:
        return f"Sorry, there is no recommendation for '{input_title}' at the moment. Try something else."
    
    index = indices[title]
    similarity_scores = tuple(enumerate(cos_similarity[index]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    similarity_scores = similarity_scores[:10]
    similarity_index = [i[0] for i in similarity_scores]
    recommendations = df.iloc[similarity_index]
    if recommendations.empty:
        return "No recommendations found for this title."
    else:
        return recommendations

# Streamlit UI
st.title('Book Recommendation System')

with st.form(key='recommendation_form'):
    input_title = st.text_input('Enter a book title:')
    submit_button = st.form_submit_button(label='Get Recommendations')

if submit_button or input_title:
    if input_title:
        result = get_book_recommendation(input_title)
        if isinstance(result, str):
            st.write(result)
        elif isinstance(result, pd.DataFrame):
            if result.empty:
                st.write('No recommendations found for this title.')
            else:
                st.write(f"Recommendations for '{input_title}':")
                for i, row in enumerate(result.itertuples(), 1):
                    st.markdown(f"**{i}. {row.title}**")
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        if pd.notna(row.image_url):
                            st.image(row.image_url, width=100)
                    with col2:
                        st.write(f"**Author:** {row.author}")
                        st.write(f"**Description:** {row.description}")
    else:
        st.write('Please enter a book title.')
