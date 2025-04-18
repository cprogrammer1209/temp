import torch
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import argparse
import pymongo
import json
from PIL import Image, ImageDraw
from inference_sdk import InferenceHTTPClient
import os
import cv2
config={}
with open('config.json', 'r') as f:
    config = json.load(f)
print ("config file loaded on start")


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

def get_args():
    parser = argparse.ArgumentParser(description='File I/O')
    parser.add_argument(
        '-i',
        '--input',
        type=str,
        help="full path to data files",
        required=True)

    parser.add_argument(
        '-t',
        '--timestamp',
        type=str,
        help="timestamp",
        required=True)

    args = parser.parse_args()
    local_path = args.input
    local_time = args.timestamp

    return local_path, local_time


class VERIFY:
    def __init__(self, model_ID="openai/clip-vit-base-patch32", validity_threshold=0.8, review_threshold=0.7):
        # Load the CLIP model
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = CLIPModel.from_pretrained(model_ID).to(self.device)
        self.preprocess = CLIPProcessor.from_pretrained(model_ID)
        self.validity_threshold = validity_threshold  # Threshold for validity (0.8)
        self.review_threshold = review_threshold      # Threshold for review recommended (0.7)

    def load_and_preprocess_image(self, image_path):
        """Load and preprocess an image for CLIP."""
        try:
            image = Image.open(image_path).convert("RGB")
            image_tensor = self.preprocess(images=image, return_tensors="pt").pixel_values
            return image_tensor.to(self.device)
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")
            return None

    def compute_similarity(self, embedding_a, embedding_b):
        """Compute the cosine similarity between two image embeddings."""
        return torch.nn.functional.cosine_similarity(embedding_a, embedding_b)

    def verify_stamp(self, reference_image_path, stamp_image_paths):
        """
        Verify stamps against a reference image.

        Args:
            reference_image_path (str): Path to the reference image.
            stamp_image_paths (list): List of paths to stamp images to verify.

        Returns:
            dict: The result of the verification process, including validity status.
        """
        # Load the reference image
        stamp_a = self.load_and_preprocess_image(reference_image_path)

        if stamp_a is not None:
            # Calculate the embedding for stamp_a
            with torch.no_grad():
                embedding_a = self.model.get_image_features(stamp_a)

            for stamp_path in stamp_image_paths:
                stamp_b = self.load_and_preprocess_image(stamp_path)

                if stamp_b is not None:
                    with torch.no_grad():
                        embedding_b = self.model.get_image_features(stamp_b)

                        # Compute the cosine similarity
                        similarity_score = self.compute_similarity(embedding_a, embedding_b).item()
                        print(f"Similarity score: {similarity_score * 100:.2f}%")
                        
                        # Check if the similarity score is above the threshold for validity
                        if similarity_score > self.validity_threshold:
                            status_reason = {"Status": "Valid"}
                            return status_reason  # Return valid if similarity score is above the threshold
                        elif similarity_score > self.review_threshold and similarity_score <= self.validity_threshold:
                            status_reason = {"Status": "Review Recommended"}
                            return status_reason  # Review if score is between 0.7 and 0.8

        status_reason = {"Status": "Rejected","similarity_score":similarity_score}
        return status_reason  # Return rejected if no valid stamps were found
    

def match_signature_mofa(data,timestamp):
    try:
        print("data input in function------",data)
        input =data['input']
        eventId = input['eventId']
        input_data = input['doc_filePath']
        # Extracting the file path from the dictionary
        file_path = input_data[0]["imageFilePath"]  # Accessing the image path from the dictionary
        user_to_find = input['folderName']  
        validity_threshold = int(input['approve_threshold'])/100
        
        review_threshold =  int(input['reject_threshold'])/100

        myclient = pymongo.MongoClient(config['dbConnection'])
        db = myclient[config['db']]

        # Access the 'signatures' collection
        signatures_collection = db['signatures']

        # Find all documents and retrieve the 'filePath' field
        file_paths = list(signatures_collection.find({"name":user_to_find}, {'filePath': 1, '_id': 0})) 
        sign_image_path=[]
        sign_image_path = sign_image_path.append(file_paths[0]['filePath'])

        # Open and preprocess the image
        img = Image.open(file_path)
        img = img.convert("L")  # Convert to grayscale
        img = img.resize((1000, 1000))
        img.save(file_path)

        # Perform inference
        result = CLIENT.infer(file_path, model_id="detector-firma/1")
        predictions = result.get('predictions', [])

        if predictions:
            pred = predictions[0]  # Assuming we are working with the first prediction

            # Extracting bounding box coordinates
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
            cropped_image_path = eventId+'_cropped_image.jpg'

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
            verifier = VERIFY("openai/clip-vit-base-patch32",validity_threshold=validity_threshold,review_threshold=review_threshold)
            is_valid_stamp = verifier.verify_stamp(cropped_image_path, sign_image_path)  # Pass file paths, not images
            print(f"Stamp Verification Status: {is_valid_stamp['Status']}")

            outputData ={ 
            'sign_status' : is_valid_stamp["Status"],
            'match_threshold':is_valid_stamp["similarity_score"],
            'statusCode':'200'
            }

        else:
            print("No predictions found.")
            outputData ={ 
                'sign_status' : "No predictions found",
                'match_threshold':"0",
                'statusCode':'400',
            }

        with open("file_"+timestamp+".json", "w") as f:
            json.dump(outputData, f)

            
        return outputData
        
    except Exception as e:
        print (e)



if __name__=="__main__":
    print("\n\n\n\n[INFO] FILE TRIGGER ..", get_args()[0],"\t",get_args()[1], "\n\n")
    match_signature_mofa(json.load(open(get_args()[0], "r")), get_args()[1])
