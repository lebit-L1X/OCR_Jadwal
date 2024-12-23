import cv2
import pytesseract
import requests
import numpy as np
from io import BytesIO
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import Flask-CORS

app = Flask(__name__)
# Enable CORS
CORS(app, resources={r"/process_schedule": {"origins": "http://localhost:5173"}}, supports_credentials=True) # Enable CORS for all routes

def preprocess_image(image):
    # Convert the image from BytesIO to a NumPy array
    image_np = np.array(bytearray(image), dtype=np.uint8)
    image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    return image, hsv_image

def find_schedules(hsv_image):
    # Define HSV ranges for schedule cells
    lower_color1 = np.array([85, 20, 200])  # Adjust these values as needed
    upper_color1 = np.array([100, 60, 255])

    lower_color2 = np.array([35, 20, 200])  # Adjust these values as needed
    upper_color2 = np.array([45, 60, 255])

    # Create masks and combine them
    mask1 = cv2.inRange(hsv_image, lower_color1, upper_color1)
    mask2 = cv2.inRange(hsv_image, lower_color2, upper_color2)
    combined_mask = cv2.bitwise_or(mask1, mask2)

    # Clean up the mask
    kernel = np.ones((5, 5), np.uint8)
    cleaned_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_CLOSE, kernel)

    # Find contours
    contours, _ = cv2.findContours(cleaned_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def extract_time(image):
    # Convert image to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define blue color range for time
    lower_blue = np.array([95, 100, 100])
    upper_blue = np.array([105, 255, 255])

    # Create mask and find contours
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    max_area = 0
    max_contour = None
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > max_area:
            max_area = area
            max_contour = contour

    if max_contour is not None:
        x, y, w, h = cv2.boundingRect(max_contour)
        roi = image[y:y + h, x:x + w]
        return pytesseract.image_to_string(roi, config='--psm 7').strip(), x
    return "Time not found", None

def extract_name(image):
    # Convert image to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define blue color range for class name
    lower_blue = np.array([90, 10, 240])
    upper_blue = np.array([100, 50, 255])

    # Create mask and find contours
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    max_area = 0
    max_contour = None

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > max_area:
            max_area = area
            max_contour = contour

    if max_contour is not None:
        x, y, w, h = cv2.boundingRect(max_contour)
        roi = image[y:y + h, x:x + w]
        return pytesseract.image_to_string(roi).strip()
    return "Class name not found"

@app.route('/process_schedule', methods=['POST'])
def process_schedule():
    # Get the URL from the form data
    image_url = request.form.get('url')

    if not image_url:
        return jsonify({"error": "URL not provided in the request"}), 400

    # Fetch the image from the URL
    response = requests.get(image_url)
    
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch image from URL"}), 500
    
    # Process the image
    image_data = response.content
    image, hsv_image = preprocess_image(image_data)

    # Find schedule regions
    contours = find_schedules(hsv_image)

    # Process each schedule
    padding_top = 30  # Adjust to include time section
    days_of_week = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
    
    schedules = []
    
    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)

        # Extend bounding box
        y_extended = max(0, y - padding_top)
        h_extended = y + h - y_extended
        roi = image[y_extended:y_extended + h_extended, x:x + w]

        # Extract time and class name
        time, x_position = extract_time(roi)
        class_name = extract_name(roi)

        # Adjust the x_position to be relative to the original image
        if x_position is not None:
            x_position += x  # Add the x value of the contour to the x_position from the ROI

            # Determine the day based on x position
            day_width = image.shape[1] // 6  # Divide width by 6 for Monday to Saturday
            day_index = x_position // day_width
            day = days_of_week[day_index] if 0 <= day_index < len(days_of_week) else "Invalid day"
        else:
            day = "Invalid day"
        
        # Store results only if both time and class name are found
        if time and class_name and time != "Time not found" and class_name != "Class name not found":
            schedules.append({
                "day": day,
                "time": time,
                "class_name": class_name
            })
    
    return jsonify({"schedules": schedules})

if __name__ == '__main__':
    app.run(debug=True)
