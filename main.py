from PIL import Image
import pytesseract
import pyttsx3

# from google_trans_new import google_translator
from deep_translator import GoogleTranslator
from lib.silent_screenshot import main as silent_screenshot

engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)

# Set up Tesseract
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load and process the image
# image = Image.open("path_to_your_image.jpg")
while True:
    try:
        image = silent_screenshot.main("ctrl", 2, 1, SAVE_PATH="screenshots/")[0]
        extracted_text = pytesseract.image_to_string(image, lang="eng")
        print(extracted_text)

        # Initialize the translator
        translator = GoogleTranslator(source="ar", target="en")
        # translated = translator.translate(extracted_text)  # Change en to the target language

        print("Original Text:", extracted_text)
        # print("Translated Text:", translated)
        engine.say(extracted_text)
        engine.runAndWait()
    except Exception as e:
        print(e)
        engine.say("An error occurred. Please try again.")
        engine.runAndWait()
