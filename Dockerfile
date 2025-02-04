# set up the base image
FROM python:3.12

# set the working directory
WORKDIR /app/

# copy the requirements file to workdir
COPY requirements.txt .

# install the requirements
RUN pip install -r requirements.txt

# Copy all required data files at once
COPY ./data/interim/collab_filtered_data.csv \
     ./data/interim/track_ids.npy \
     ./data/interim/cleaned_data.csv \
     ./data/interim/


COPY ./data/processed/interaction_matrix.npz \
     ./data/processed/transformed_data.npz \
     ./data/processed/transformed_hybrid_data.npz \
     ./data/processed/


# Copy all required Python scripts at once
COPY app.py \
     collaborative_filtering.py \
     content_based_filtering.py \
     hybrid_recommendations.py \
     data_cleaning.py \
     transform_filtered_data.py \
     ./

# expose the port on the container
EXPOSE 8000

# run the streamlit app
CMD [ "streamlit", "run", "app.py", "--server.port", "8000", "--server.address", "0.0.0.0"]