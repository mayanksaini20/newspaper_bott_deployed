# import cv2
# import os
# import pytesseract
# from gtts import gTTS
# from ultralytics import YOLO
# import matplotlib.pyplot as plt
# import time

# # Paths
# model_path = "best_30_epochs.pt"  # Update this to your local model path
# input_image_path = "WhatsApp Image 2024-09-09 at 23.54.33_dc3f29db.jpg"  # Update this to your image path
# output_dir = "cropped_boxes"

# # Load the YOLO model
# model = YOLO(model_path)

# # Create a directory to save cropped images and audio files
# os.makedirs(output_dir, exist_ok=True)

# # Perform inference on an image
# results = model(input_image_path)

# # Get the original image for cropping
# original_image = cv2.imread(input_image_path)

# # List to store extracted texts
# extracted_texts = []

# # Loop over the detected objects
# total_boxes = len(results[0].boxes.xyxy)
# print(f"Total boxes detected: {total_boxes}")

# for i, box in enumerate(results[0].boxes.xyxy):
#     print(f"Processing box {i}...")  # Debugging statement

#     try:
#         x1, y1, x2, y2 = map(int, box)
#         confidence = results[0].boxes.conf[i]  # Get confidence score

#         if confidence > 0.1:  # Threshold for confidence
#             # Crop the image using the bounding box coordinates
#             cropped_img = original_image[y1:y2, x1:x2]

#             # Save the cropped image to the output folder
#             cropped_img_path = os.path.join(output_dir, f"cropped_box_{i}.jpg")
#             cv2.imwrite(cropped_img_path, cropped_img)
#             print(f"Cropped image saved as {cropped_img_path}")

#             # Convert cropped image to RGB for OCR
#             cropped_img_rgb = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB)

#             # Perform OCR on the cropped image
#             text = pytesseract.image_to_string(cropped_img_rgb, lang='hin')  # Use 'hin' for Hindi
#             print(f"Extracted text from box {i}: {text}")

#             # Clean up the extracted text
#             cleaned_text = "\n".join(line.strip().replace(":", "") for line in text.splitlines() if line.strip())
            
#             # Append cleaned text to the list
#             extracted_texts.append(cleaned_text)

#             print(f"Text from box {i}:")
#             print(cleaned_text)

#             # Display the cropped image using matplotlib without blocking the script
#             plt.imshow(cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB))  # Convert BGR to RGB
#             plt.title(f'Cropped Image {i}')
#             plt.show(block=False)
#             plt.pause(2)  # Pause to allow display of each image for 2 seconds before moving to the next one

#     except Exception as e:
#         print(f"Error processing box {i}: {e}")

# # Convert all extracted texts to audio at the end
# for i, cleaned_text in enumerate(extracted_texts):
#     if cleaned_text.strip():  # Only convert if there is text
#         audio_file = os.path.join(output_dir, f"output_box_{i}.mp3")  # Define audio file name
#         try:
#             # Use gTTS to convert text to audio
#             tts = gTTS(text=cleaned_text, lang='hi')
#             tts.save(audio_file)
#             print(f"Audio saved as {audio_file}")
#         except Exception as e:
#             print(f"Error converting text to audio for box {i}: {e}")

# No need for cv2.imshow or cv2.destroyAllWindows

#7565910815:AAHSAT6AtHwhBdcqtLdvrIAjhI_6ZRrKRUc

import os
import cv2
import pytesseract
from gtts import gTTS
from ultralytics import YOLO
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import logging

# Paths
model_path = "best_30_epochs.pt"  # Update this to your local model path
output_dir = "cropped_boxes"

# Initialize YOLO model
model = YOLO(model_path)

# Set up logging for the bot
logging.basicConfig(level=logging.INFO)

# Define the start function for the bot
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi! Send me an image of a newspaper and I will process it.')

# Define the image handler for processing images
def handle_image(update: Update, context: CallbackContext) -> None:
    # Get the image from the user
    image = update.message.photo[-1].get_file()
    input_image_path = os.path.join(output_dir, "input_image.jpg")
    image.download(input_image_path)
    
    # Perform inference using YOLO
    results = model(input_image_path)
    original_image = cv2.imread(input_image_path)

    extracted_texts = []
    
    for i, box in enumerate(results[0].boxes.xyxy):
        try:
            x1, y1, x2, y2 = map(int, box)
            confidence = results[0].boxes.conf[i]
            
            if confidence > 0.1:
                # Crop the image
                cropped_img = original_image[y1:y2, x1:x2]
                cropped_img_path = os.path.join(output_dir, f"cropped_box_{i}.jpg")
                cv2.imwrite(cropped_img_path, cropped_img)
                
                # Send the cropped image back to the user
                context.bot.send_photo(chat_id=update.message.chat_id, photo=open(cropped_img_path, 'rb'))
                
                # OCR and text extraction
                cropped_img_rgb = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB)
                text = pytesseract.image_to_string(cropped_img_rgb, lang='hin')
                cleaned_text = "\n".join(line.strip().replace(":", "") for line in text.splitlines() if line.strip())
                extracted_texts.append(cleaned_text)
                
                # Convert text to audio and send back
                if cleaned_text.strip():
                    audio_file = os.path.join(output_dir, f"output_box_{i}.mp3")
                    tts = gTTS(text=cleaned_text, lang='hi')
                    tts.save(audio_file)
                    context.bot.send_audio(chat_id=update.message.chat_id, audio=open(audio_file, 'rb'))
        
        except Exception as e:
            print(f"Error processing box {i}: {e}")

# Main function to set up the bot
def main() -> None:
    # Your Telegram Bot API Token
    TELEGRAM_BOT_TOKEN = '7565910815:AAHSAT6AtHwhBdcqtLdvrIAjhI_6ZRrKRUc'  # Replace with your actual token

    # Set up the bot
    updater = Updater(TELEGRAM_BOT_TOKEN)

    # Register handlers
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.photo, handle_image))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    os.makedirs(output_dir, exist_ok=True)
    main()
