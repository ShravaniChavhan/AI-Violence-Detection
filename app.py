from flask import (Flask, request, render_template, send_from_directory)
import os
import tensorflow as tf
import cv2
import numpy as np
import uuid
from werkzeug.utils import secure_filename
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

app = Flask(__name__)

# UPLOAD CONFIGURATION
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {
    "mp4",
    "avi",
    "mov",
    "mkv",
    "webm"
}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024 # Maximum upload size = 100 MB.
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    # Check that:
    # 1. The filename contains a dot.
    # 2. The extension is present in our allowed list.
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )

# LOAD TRAINED MODEL
MODEL_PATH = "model/violence_detection_model.keras"
model = tf.keras.models.load_model(MODEL_PATH)

# MODEL INPUT CONFIGURATION
SEQUENCE_LENGTH = 16
IMAGE_HEIGHT = 224
IMAGE_WIDTH = 224

# FRAME EXTRACTION
def frames_extraction(video_path):

    frames_list = []
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(
            f"Could not open video: {video_path}"
        )
        return frames_list

    total_frames = int(
        cap.get(cv2.CAP_PROP_FRAME_COUNT)
    )

    if total_frames < SEQUENCE_LENGTH:
        cap.release()
        print(
            "Video contains fewer than "
            f"{SEQUENCE_LENGTH} frames."
        )

        return frames_list

    frame_indices = np.linspace(
        0,
        total_frames - 1,
        SEQUENCE_LENGTH,
        dtype=int
    )

    # Extract each selected frame.
    for frame_index in frame_indices:

        cap.set(
            cv2.CAP_PROP_POS_FRAMES,
            frame_index
        )

        success, frame = cap.read()

        if not success:
            continue

        frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        frame = cv2.resize(
            frame,
            (IMAGE_WIDTH, IMAGE_HEIGHT)
        )

        frame = preprocess_input(
            frame.astype(np.float32)
        )
        
        frames_list.append(frame)

    cap.release()

    return frames_list


# VIDEO PREDICTION
def predict_video(video_path):

    try:

        frames = frames_extraction(video_path)
        if len(frames) != SEQUENCE_LENGTH:

            print(
                "Could not extract exactly "
                f"{SEQUENCE_LENGTH} frames."
            )

            return None, None

        frames_array = np.array(
            frames,
            dtype=np.float32
        )

        frames_array = np.expand_dims(
            frames_array,
            axis=0
        )

        # Final model input shape:
        #
        # (1, 16, 224, 224, 3)
        #
        # 1  = one video
        # 16 = frames
        # 224 × 224 = image dimensions
        # 3 = RGB channels

        prediction = model.predict(
            frames_array,
            verbose=0
        )

        violence_probability = float(
            prediction[0][0]
        )

        if violence_probability >= 0.5:
            predicted_class = "Violence"
            confidence = violence_probability

        else:
            predicted_class = "NonViolence"
            confidence = 1 - violence_probability

        return predicted_class, confidence

    except Exception as e:
        print(
            f"Error during prediction: {e}"
        )

        return None, None



# HOME ROUTE
@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        if "video" not in request.files:
            return "No video was uploaded."

        video = request.files["video"]

        if video.filename == "":

            return "No video was selected."

        if not allowed_file(video.filename):
            return (
                "Invalid file type. "
                "Please upload a valid video."
            )

        # secure_filename removes potentially unsafe characters from the original filename.
        original_filename = secure_filename(
            video.filename
        )

       #Creates unique filename
        unique_filename = (
            f"{uuid.uuid4().hex}_"
            f"{original_filename}"
        )
        
        # Creates video path
        video_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            unique_filename
        )

        try:
            video.save(video_path)

            predicted_class, confidence = predict_video(
                video_path
            )

        except Exception as e:
            print(
                f"Error processing uploaded video: {e}"
            )
            if os.path.exists(video_path):
                os.remove(video_path)
            return (
                "An error occurred while "
                "processing the video."
            )

        if predicted_class is None:
            if os.path.exists(video_path):
                os.remove(video_path)

            return (
                "Could not process the video. "
                "Please upload a valid video with "
                "at least 16 readable frames."
            )

        return render_template(
            "result.html",
            prediction=predicted_class,
            confidence=f"{confidence * 100:.2f}",
            video_filename=unique_filename
        )

    return render_template("index.html")



# This route allows the browser to access the uploaded video on the result page.
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    
    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )

# if the uploaded video exceeds  100 MB limit.
@app.errorhandler(413)
def request_entity_too_large(error):
    return (
        "The uploaded video is too large. "
        "Please upload a video smaller than 100 MB."
    ), 413


if __name__ == "__main__":

    # test_video = "test_videos/NV_139.mp4"
    # predicted_class, confidence = predict_video(
    #     test_video
    # )
    # print("Prediction:", predicted_class)
    
    # if confidence is not None:
    #     print(
    #         "Confidence:",
    #         f"{confidence * 100:.2f}%"
    #     )
    app.run(debug=True)