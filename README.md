This script processes an image of a schedule (e.g., a timetable screenshot) and extracts information about the time, class names, and corresponding days of the week. It uses OpenCV for image processing and PyTesseract for text recognition.

## Prerequisites
Required Libraries:
OpenCV: For image processing tasks.

Install via pip:
```bash
pip install opencv-python
```
PyTesseract: For Optical Character Recognition (OCR).

Install via pip:
```bash
pip install pytesseract
```
Also install Tesseract-OCR on your system.

NumPy: For array manipulations.

Install via pip:
```bash
pip install numpy
```
Image File:
Ensure you have an image file named siak.png in the current working directory.

How the Script Works
1. Preprocess Image
The function preprocess_image(image_path):

Reads the input image (siak.png) using OpenCV.
Converts the image to HSV color space for more effective color-based filtering.

3. Find Schedule Regions
The function find_schedules(hsv_image):

Defines HSV color ranges to detect regions representing schedules.
Uses OpenCV’s cv2.inRange() to create binary masks for these color ranges.
Combines the masks and applies morphological operations to clean up noise.
Detects contours of the schedule regions using cv2.findContours().

3. Extract Time and Class Name
The functions extract_time(image) and extract_name(image):

Define HSV color ranges specific to the time and class name sections.
Create binary masks and find contours to locate these text regions.
Use pytesseract.image_to_string() to extract text from the detected regions.

4. Identify Day of the Week
The script calculates the horizontal position (x_position) of the detected time or class name region within the image.
Divides the image width into six equal parts, corresponding to the days from Monday to Saturday.
Maps the region's horizontal position to the appropriate day.

5. Main Workflow
The main() function:

Loads the image and preprocesses it.
Detects schedule regions using find_schedules.
Processes each schedule region:
Extracts the time and class name.
Determines the day based on the region's position.
Prints the extracted information in a structured format.
Output
For each detected schedule region, the script outputs:

Day: The day of the week (e.g., "Monday").
Time: The schedule's time (e.g., "08:00-10:00").
Class Name: The name of the class (e.g., "Mathematics").

Adjust the HSV ranges in find_schedules, extract_time, and extract_name for different image color schemes or lighting conditions.
Modify padding_top and day_width to fine-tune region detection for your specific image layout.
Hosted_main.py also can be run, which hosts the program locally using Flask.
