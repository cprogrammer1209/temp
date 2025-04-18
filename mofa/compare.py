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