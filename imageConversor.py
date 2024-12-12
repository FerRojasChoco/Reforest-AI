from flask import Flask, request, url_for
import cv2
import numpy as np
from io import BytesIO
from PIL import Image
from datetime import datetime

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_image():
    # Get the uploaded image
    image_file = request.files['image']
    
    # Convert the image to grayscale using OpenCV
    image = Image.open(image_file.stream)  # Use PIL to read the image
    image_np = np.array(image)  # Convert to NumPy array (needed for OpenCV)

    # Convert to grayscale
    gray_image = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)

    # Save the processed image temporarily in the static directory
    processed_image_path = 'static/grayscale_image.jpg'
    cv2.imwrite(processed_image_path, gray_image)
    
    # Generate the URL to the processed image
    timestamp = datetime.now().timestamp()  # Unique query parameter
    image_url = url_for('static', filename='grayscale_image.jpg', _external=True) + f"?v={timestamp}"

    return image_url  # Return the image URL to the frontend

if __name__ == '__main__':
    app.run(debug=True, port=5000)
