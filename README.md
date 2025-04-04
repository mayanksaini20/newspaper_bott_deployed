# Newspaper Bot Deployed

This project is a Telegram bot designed to process images of Hindi newspapers. It extracts news articles from the images and converts them into audio files, allowing users to listen to the news in Hindi.

## Features

- **Article Detection**: Utilizes a modified YOLOv8 architecture to detect and extract news articles from newspaper images.
- **Text Extraction**: Employs Tesseract OCR to convert the extracted article images into text.
- **Audio Conversion**: Uses gTTS (Google Text-to-Speech) to convert the extracted text into audio files.
- **Telegram Integration**: The bot operates within Telegram, allowing users to interact by sending newspaper images and receiving audio news.

## How It Works

1. **Dataset Creation**: A dataset is created by annotating newspaper images with bounding boxes around articles using a modified YOLOv8 architecture.
2. **Model Training**: The YOLOv8 model is trained on this dataset to detect articles in newspaper images.
3. **Article Extraction**: The trained model detects and extracts article regions from new newspaper images.
4. **Text Recognition**: Tesseract OCR converts the extracted article images into text.
5. **Audio Generation**: gTTS converts the recognized text into audio files.
6. **User Interaction**: Users interact with the bot on Telegram by sending newspaper images and receiving the corresponding audio news.

## Getting Started

To set up and run the Newspaper Bot locally, follow these steps:

### Prerequisites

- Python 3.x
- pip (Python package installer)
- Telegram account

### Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/mayanksaini20/newspaper_bott_deployed.git

2. **Navigate to the Project Directory**:
   ```bash
   cd newspaper_bott_deployed
3. **Install Required Packages**:
   ```bash
   pip install -r requirements.txt

### Usage

1. **Run the Bot:**:

   ```bash
   python bot.py

2. **Interact via Telegram:**:
   
- Open Telegram and search for "Newspaper Bot".
- Start the bot by typing /start.
- Set the language to Hindi by typing /setlanguage and selecting Hindi.
- Send a clear image of a Hindi newspaper to the bot.
- The bot will process the image and send back audio files of the extracted news articles.

### Techniques Used

- YOLOv8 for Article Detection: A modified YOLOv8 model is used to detect and extract articles from newspaper images.
- Tesseract OCR for Text Extraction: Converts the extracted article images into text.
- gTTS for Audio Conversion: Transforms the extracted text into audio files.

### Notes

- Ensure that the newspaper images sent to the bot are clear and of high quality for optimal processing.
- The bot is currently not deployed online; it needs to be run locally as described above.

### Acknowledgments
This project is licensed under the MIT License. See the LICENSE file for details.
