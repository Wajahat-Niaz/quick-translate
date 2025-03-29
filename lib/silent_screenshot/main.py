import os
import pyautogui
import time
import keyboard
import pyttsx3

HOTKEY = "ctrl"  # The key/s to trigger the script
MOUSE_STILL_DELAY = 3  # The time in seconds to wait for the mouse to remain still before recording the first corner
SECOND_MOUSE_STILL_DELAY = 2  # The time in seconds to wait for the mouse to remain still before recording the second corner
SAVE_PATH = os.getcwd() + "/screenshots/"  # The path to save the screenshots


engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)


def mouse_still_for(seconds):
    # Record the initial position and start time
    initial_position = pyautogui.position()
    start_time = time.time()

    while True:
        # Check the current mouse position
        current_position = pyautogui.position()

        # If the position has changed, reset start time and position
        if current_position != initial_position:
            initial_position = current_position
            start_time = time.time()

        # If the specified time has passed without movement, return the position
        if time.time() - start_time >= seconds:
            return initial_position

        # Delay to reduce CPU usage
        time.sleep(0.1)


def main(
    HOTKEY: str | None = None,
    MOUSE_STILL_DELAY: int = 3,
    SECOND_MOUSE_STILL_DELAY: int = 2,
    SAVE_PATH: str | None = None,
    engine: pyttsx3.engine.Engine = pyttsx3.init(),
):
    while True:
        if (
            HOTKEY and keyboard.is_pressed(HOTKEY) or (not HOTKEY)
        ):  # If the hotkey is pressed, check for mouse stillness. If the hotkey isn't specified, this will be ignored
            print("Hotkey Pressed")
            first_corner = mouse_still_for(MOUSE_STILL_DELAY)  # Record the first corner
            print("First Corner: ", first_corner)
            engine.say("First")
            engine.runAndWait()
            second_corner = mouse_still_for(
                SECOND_MOUSE_STILL_DELAY
            )  # Record the second corner
            print("Second Corner: ", second_corner)
            engine.say("Second")
            engine.runAndWait()
            try:
                SAVED = SAVE_PATH + str(time.time()) + ".png" if SAVE_PATH else None
                screenshot = pyautogui.screenshot(
                    SAVED,
                    region=(
                        first_corner[0],
                        first_corner[1],
                        second_corner[0] - first_corner[0],
                        second_corner[1] - first_corner[1],
                    ),
                )  # Take screenshot
                print("Screenshot saved!")
                return (screenshot, SAVED)

            except FileNotFoundError:
                print("Save directory does not exist, Creating...")
                os.mkdir(SAVE_PATH)  # Create save directory if it doesn't exist

            except ValueError:
                screenshot = pyautogui.screenshot(
                    SAVE_PATH + str(time.time()) + ".png" if SAVE_PATH else None,
                    region=(
                        second_corner[0],
                        second_corner[1],
                        first_corner[0] - second_corner[0],
                        first_corner[1] - second_corner[1],
                    ),
                )
                return screenshot
            # TODO: Add more error handling for pyautogui screenshot function

        time.sleep(0.2)  # Delay to reduce CPU usage


if __name__ == "__main__":
    while True:
        main(HOTKEY, MOUSE_STILL_DELAY, SECOND_MOUSE_STILL_DELAY, SAVE_PATH, engine)
