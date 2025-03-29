import base64
import keyboard
import time
import pytesseract
from openai import OpenAI
from PIL import Image
import pyttsx3
from lib.silent_screenshot import main as silent_screenshot

engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
client = OpenAI(
    api_key="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"
)


def main():
    while True:
        # if keyboard.is_pressed("ctrl"):
        #     while True:
        #         print("Waiting")
        #         if keyboard.is_pressed("alt"):
        #             break
        #         time.sleep(0.2)
        # try:
        image, SAVED = silent_screenshot.main("ctrl", 2, 1, SAVE_PATH="screenshots/")
        extracted_text = pytesseract.image_to_string(image, lang="eng")
        print(extracted_text)
        # base64_image = encode_image(SAVED)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Answer the question, make your response short and to the point",
                        },
                        {
                            "type": "text",
                            "text": extracted_text,
                        },
                    ],
                }
            ],
        )

        print(response.choices[0])

        engine.say(response.choices[0].message.content)
        engine.runAndWait()

        # except Exception as e:
        #     print(e)
        #     engine.say("An error occurred. Please try again.")
        #     engine.runAndWait()
        time.sleep(0.2)


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


if __name__ == "__main__":
    main()
