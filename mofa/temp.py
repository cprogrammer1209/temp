import torch
import cv2
import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity as ssim
from inference_sdk import InferenceHTTPClient
from clip_model import VERIFY
from signature_tampering import detect_clone_tampering
import os


def main():
    # File path provided in the new format
    input_data = [
        {
            "imageFilePath": "negative/negative_1.jpg"
        }
    ]

    # Extracting the file path from the dictionary
    file_path = input_data[0]["imageFilePath"]  # Accessing the image path from the dictionary
    sign_image_path = ["og_1.jpg"]  # Changed to a string

    try:
        # Initialize Inference Client
        CLIENT = InferenceHTTPClient(
            api_url="https://detect.roboflow.com",
            api_key="R0gQ2F8GuATwGGzwdLtH"
        )
        '''
        THIS MODEL HAS HIGHER ACCURACY ON BLANK/ NON RULED PAGE

        CLIENT = InferenceHTTPClient(
            api_url="https://detect.roboflow.com",
            api_key="R0gQ2F8GuATwGGzwdLtH"
            )

        result = CLIENT.infer(your_image.jpg, model_id="sign_det-ixn1w/3")
        '''
        # Open and preprocess the image
        img = Image.open(file_path)
        img = img.convert("L")  # Convert to grayscale
        img = img.resize((1000, 1000))
        img.save(file_path)

        # Perform inference
        result = CLIENT.infer(file_path, model_id="detector-firma/1")
        predictions = result.get('predictions', [])

        if predictions:
            pred = predictions[0]  # Assume first prediction is the signature

            # Extract bounding box coordinates
            x = pred['x']
            y = pred['y']
            width = pred['width']
            height = pred['height']

            # Load the image
            image = Image.open(file_path)
            print(f"Original Coordinates - x: {x}, y: {y}, width: {width}, height: {height}")

            # Corrected bounding box coordinates
            left = int(x - (width / 2))
            upper = int(y - (height / 2))
            right = int(x + (width / 2))
            lower = int(y + (height / 2))

            coordinates = (left, upper, right, lower)

            # Crop the image
            cropped_image = image.crop(coordinates)
            cropped_image_path = 'cropped_image.jpg'

            # Save the cropped image
            cropped_image.save(cropped_image_path)
            print(f"Cropped image saved to {cropped_image_path}")

            # Use absolute path for better clarity
            cropped_image_path = os.path.abspath(cropped_image_path)
            print(f"Absolute path of cropped image: {cropped_image_path}")

            # Check if the cropped image exists before continuing
            if os.path.exists(cropped_image_path):
                cropped_cv2_image = cv2.imread(cropped_image_path)
                if cropped_cv2_image is None:
                    print(f"Error: Unable to read the image from {cropped_image_path}")
                    return
            else:
                print(f"Error: The file {cropped_image_path} does not exist.")
                return

            # Initialize the verifier
            verifier = VERIFY()

            # Verify the stamp
            is_valid_stamp = verifier.verify_stamp(cropped_image_path, sign_image_path)
            print(f"Stamp Verification Status: {is_valid_stamp['Status']}")

            # Check for cloning or tampering if stamp is valid or needs review
            if is_valid_stamp["Status"] in ["Valid", "Review Recommended"]:
                cloning_result = detect_clone_tampering(cropped_image_path)
                print(f"Cloning Detection Result: {cloning_result}")
        else:
            print("No Signature found.")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()