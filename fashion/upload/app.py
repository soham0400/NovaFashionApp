import numpy as np
import pickle as pkl
import tensorflow as tf
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.layers import GlobalMaxPool2D
from sklearn.neighbors import NearestNeighbors
import os
import streamlit as st
import pandas as pd

st.header('Fashion Recommendation System')

Image_features = pkl.load(open('Images_features.pkl', 'rb'))
filenames = pkl.load(open('filenames.pkl', 'rb'))
df = pd.read_csv('price.csv')

def extract_features_from_images(image_path, model):
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_expand_dim = np.expand_dims(img_array, axis=0)
    img_preprocess = preprocess_input(img_expand_dim)
    result = model.predict(img_preprocess).flatten()
    norm_result = result / np.linalg.norm(result)
    return norm_result

model = ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
model.trainable = False

model = tf.keras.models.Sequential([
    model,
    GlobalMaxPool2D()
])

neighbors = NearestNeighbors(n_neighbors=6, algorithm='brute', metric='euclidean')
neighbors.fit(Image_features)

# Load images from the "upload" folder
upload_folder = "upload"
uploaded_images = []
for filename in os.listdir(upload_folder):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        uploaded_images.append(os.path.join(upload_folder, filename))

if len(uploaded_images) > 0:
    st.subheader('Uploaded Images')
    for img_path in uploaded_images:
        st.image(img_path)
        input_img_features = extract_features_from_images(img_path, model)
        distance, indices = neighbors.kneighbors([input_img_features])
        st.subheader('Recommendations for Uploaded Image')
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.image(filenames[indices[0][1]])
        with col2:
            st.image(filenames[indices[0][2]])
        with col3:
            st.image(filenames[indices[0][3]])
        with col4:
            st.image(filenames[indices[0][4]])
        with col5:
            st.image(filenames[indices[0][5]])
else:
    st.write("No images uploaded yet.")
