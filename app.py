import streamlit as st
from content_based_filtering import content_recommendation
from collaborative_filtering import collaborative_recommendation
from hybrid_recommendations import HybridRecommenderSystem
from scipy.sparse import load_npz
import pandas as pd
from numpy import load


# load the data
cleaned_data_path = "data/interim/cleaned_data.csv"
songs_data = pd.read_csv(cleaned_data_path)

# load the transformed data
transformed_data_path = "data/processed/transformed_data.npz"
transformed_data = load_npz(transformed_data_path)

# load the track ids
track_ids_path = "data/interim/track_ids.npy"
track_ids = load(track_ids_path, allow_pickle=True)

# load the filtered songs data
filtered_data_path = "data/interim/collab_filtered_data.csv"
filtered_data = pd.read_csv(filtered_data_path)

# load the interaction matrix
interaction_matrix_path = "data/processed/interaction_matrix.npz"
interaction_matrix = load_npz(interaction_matrix_path)

# load the transformed hybrid data
transformed_hybrid_data_path = "data/processed/transformed_hybrid_data.npz"
transformed_hybrid_data = load_npz(transformed_hybrid_data_path)

# Title
st.title("Welcome to the Spotify Song Recommender!")

# Subheader
st.write("### Enter the name of a song and the recommender will suggest similar songs 🎵🎧")

# Text Input
# song_name = st.text_input("Enter a song name:")
song_name = st.selectbox("Select a song name:", filtered_data["name"].unique())
st.write("You entered:", song_name.title())

# lowercase the input
song_name = song_name.lower()

# artist name
# artist_name = st.text_input("Enter the artist name:")
artist_name = st.selectbox(
    "Select an artist name:",
    filtered_data[(filtered_data["name"] == song_name)]["artist"].unique(),
)
st.write("You entered:", artist_name.title())
artist_name = artist_name.lower()

# k recommndations
k = st.selectbox("How many recommendations do you want?", [5, 10, 15, 20], index=0)

filtering_type = st.selectbox(
    "Select the type of filtering: ",
    ["Content-Based Filtering", "Collaborative Filtering", "Hybrid Recommender System"],
)

# Button
if filtering_type == "Content-Based Filtering":
    if st.button("Get Recommendations"):
        if ((songs_data["name"] == song_name) & (songs_data["artist"] == artist_name)).any():
            st.write(
                "Recommendations for", f"**{song_name.title()}** by **{artist_name.title()}**"
            )
            recommendations = content_recommendation(
                song_name=song_name,
                artist_name=artist_name,
                songs_data=songs_data,
                transformed_data=transformed_data,
                k=k,
            )

            # Display Recommendations
            for ind, recommendation in recommendations.iterrows():
                song_name = recommendation["name"].title()
                artist_name = recommendation["artist"].title()

                if ind == 0:
                    st.markdown("## Currently Playing")
                    st.markdown(f"#### **{song_name}** by **{artist_name}**")
                    st.audio(recommendation["spotify_preview_url"])
                    st.write("---")
                elif ind == 1:
                    st.markdown("### Next Up 🎵")
                    st.markdown(f"#### {ind}. **{song_name}** by **{artist_name}**")
                    st.audio(recommendation["spotify_preview_url"])
                    st.write("---")
                else:
                    st.markdown(f"#### {ind}. **{song_name}** by **{artist_name}**")
                    st.audio(recommendation["spotify_preview_url"])
                    st.write("---")
        else:
            st.write(
                f"Sorry, we couldn't find {song_name} in our database. Please try another song."
            )
elif filtering_type == "Collaborative Filtering":
    if st.button("Get Recommendations"):
        if ((filtered_data["name"] == song_name) & (filtered_data["artist"] == artist_name)).any():
            st.write(
                "Recommendations for", f"**{song_name.title()}** by **{artist_name.title()}**"
            )
            recommendations = collaborative_recommendation(
                song_name=song_name,
                artist_name=artist_name,
                track_ids=track_ids,
                songs_data=filtered_data,
                interaction_matrix=interaction_matrix,
                k=k,
            )

            # Display Recommendations
            for ind, recommendation in recommendations.iterrows():
                song_name = recommendation["name"].title()
                artist_name = recommendation["artist"].title()

                if ind == 0:
                    st.markdown("## Currently Playing")
                    st.markdown(f"#### **{song_name}** by **{artist_name}**")
                    st.audio(recommendation["spotify_preview_url"])
                    st.write("---")
                elif ind == 1:
                    st.markdown("### Next Up 🎵")
                    st.markdown(f"#### {ind}. **{song_name}** by **{artist_name}**")
                    st.audio(recommendation["spotify_preview_url"])
                    st.write("---")
                else:
                    st.markdown(f"#### {ind}. **{song_name}** by **{artist_name}**")
                    st.audio(recommendation["spotify_preview_url"])
                    st.write("---")
        else:
            st.write(
                f"Sorry, we couldn't find {song_name} in our database. Please try another song."
            )

elif filtering_type == "Hybrid Recommender System":

    # diversity slider
    diversity = st.slider(
        label="Diversity in Recommendations", min_value=1, max_value=9, value=5, step=1
    )
    content_based_weight = 1 - (diversity / 10)

    # plot a bar graph
    chart_data = pd.DataFrame(
        {"type": ["Personalized", "Diverse"], "ratio": [10 - diversity, diversity]}
    )

    st.bar_chart(chart_data, x="type", y="ratio")
    
    if st.button("Get Recommendations"):
        st.write("Recommendations for", f"**{song_name.title()}** by **{artist_name.title()}**")
        recommender = HybridRecommenderSystem(
            number_of_recommendations=k, weight_content_based=content_based_weight
        )

        # get the recommendations
        recommendations = recommender.give_recommendations(
            song_name=song_name,
            artist_name=artist_name,
            songs_data=filtered_data,
            transformed_matrix=transformed_hybrid_data,
            track_ids=track_ids,
            interaction_matrix=interaction_matrix,
        )
        # Display Recommendations
        for ind, recommendation in recommendations.iterrows():
            song_name = recommendation["name"].title()
            artist_name = recommendation["artist"].title()

            if ind == 0:
                st.markdown("## Currently Playing")
                st.markdown(f"#### **{song_name}** by **{artist_name}**")
                st.audio(recommendation["spotify_preview_url"])
                st.write("---")
            elif ind == 1:
                st.markdown("### Next Up 🎵")
                st.markdown(f"#### {ind}. **{song_name}** by **{artist_name}**")
                st.audio(recommendation["spotify_preview_url"])
                st.write("---")
            else:
                st.markdown(f"#### {ind}. **{song_name}** by **{artist_name}**")
                st.audio(recommendation["spotify_preview_url"])
                st.write("---")
