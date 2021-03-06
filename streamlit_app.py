import streamlit as st
import cv2
import tensorflow as tf
import numpy as np
from keras.models import load_model
import sys

# Loading the Inception model
model = load_model('model.h5', compile=(False))


# Functions
def predict(frame, model):
    # Pre-process the image for model prediction
    img = cv2.resize(frame, (299, 299))
    img = img.astype(np.float32)
    img = np.expand_dims(img, axis=0)

    img /= 255.0

    # Predict with the Inceptionv3 model
    prediction = model.predict(img)

    # Convert the prediction into text
    pred_text = tf.keras.applications.inception_v3.decode_predictions(prediction, top=1)
    for (i, (imagenetID, label, prob)) in enumerate(pred_text[0]):
        label = ("{}: {:.2f}%".format(label, prob * 100))
    
    #Return the predicted label and its corresponding probability
    st.markdown(label)


def predict2(frame, model):
    # Pre-process the image for model prediction
    img = cv2.resize(frame, (299, 299))
    img = img.astype(np.float32)
    img = np.expand_dims(img, axis=0)

    img /= 255.0

    # Predict with the Inceptionv3 model
    prediction = model.predict(img)

    # Convert the prediction into text
    pred_text = tf.keras.applications.inception_v3.decode_predictions(prediction, top=1)
    for (i, (imagenetID, label, prob)) in enumerate(pred_text[0]):
        pred_class = label
    
    #Return the predicted class for Search comparison
    return pred_class


def object_detection(search_key, frame, model):
    label = predict2(frame, model)
    #Convert the string to lower case for effective comparison
    label = label.lower()
    if label.find(search_key) > -1:
        st.image(frame, caption=label)

        return sys.exit()
    else:
        pass
        


# Main App
def main():
    """Deployment using Streamlit"""
    st.title("Object Detection App")
    st.text("Built with Streamlit and Inceptionv3")

    activities = ["Detect Objects", "About"]
    choice = st.sidebar.selectbox("Choose Activity", activities)

    if choice == "Detect Objects":
        st.subheader("Upload Video")

        video_file = st.file_uploader("Choose a video...", type=["mp4", "avi"])

        if video_file is not None:
            path = video_file.name
            with open(path, mode='wb') as f:
                f.write(video_file.read())
                st.success("Saved File")
                video_file = open(path, "rb").read()
                st.video(video_file)
            cap = cv2.VideoCapture(path)
            

            if st.button("Detect Objects"):

                # Start the video prediction loop
                while cap.isOpened():
                    ret, frame = cap.read()

                    if not ret:
                        break

                    # Perform object detection
                    predict(frame, model)

                   

                cap.release()
                
                

            key = st.text_input('Search key')
            key = key.lower()

            if key is not None:

                if st.button("Search for an object"):

                    # Start the video prediction loop
                    while cap.isOpened():
                        ret, frame = cap.read()

                        if not ret:
                            break

                        # Perform object detection
                        object_detection(key, frame, model)
                        

                        

                    cap.release()
                   
                    

                    #Return statement if object is not found
                    st.text("Object not found")

    elif choice == "About":
        st.subheader("About")
        st.text("Built with Streamlit and Inceptionv3")
        st.subheader("By")
        st.text("Watifadza Dziva\nThabolezwe Mabandla")


if __name__ == '__main__':
    main()
