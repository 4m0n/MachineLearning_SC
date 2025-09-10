import pyautogui
import time
import os
from datetime import datetime
from pathlib import Path
from loguru import logger
from tqdm import tqdm
import typer
from typing import Optional
import threading
from pynput.keyboard import Listener
from playsound import playsound
import simpleaudio as sa
import winsound
#import cv2

app = typer.Typer()

key_pressed = None

def on_press(key):
    global key_pressed
    try:
        key_pressed = key.char  
    except AttributeError:
        key_pressed = str(key)
class AudioPlayer:
    def start_sound(self, duration = 0.3, freq = 640):
            winsound.Beep(freq, int(duration * 1000))
    def end_sound(self, duration = 0.8, freq = 340):
            winsound.Beep(freq, int(duration * 1000))
    def recording_sound(self, duration = 0.2, freq = 340):
            winsound.Beep(freq, int(duration * 1000))
            time.sleep(0.1)
            winsound.Beep(freq, int(duration * 1000))
            time.sleep(0.1)
            winsound.Beep(freq, int(duration * 1000))
# erstellt den screenshot / evlt später direkt noch zurechtschneiden
def make_screenshot():
    screenshot = pyautogui.screenshot()
    return screenshot

#speichert den screen (sollte auf jedem pc klappen)
def save_screenshot(screenshot, output_dir, praefix,first):
    try:
        base_dir = Path(__file__).resolve().parent.parent
        output_dir = base_dir / output_dir

        if not output_dir.exists():
            os.makedirs(output_dir)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{praefix}_{timestamp}.png"
        filepath = output_dir / filename
        screenshot.save(filepath)
        if first:
            logger.info("Start Recording")
            logger.debug(f"Output directory: {output_dir}")
            logger.debug(f"File path: {filepath}")
            logger.info(f"Screenshot saved to {filepath}")
    except Exception as e:
        logger.error(f"Error saving screenshot: {e}")
    
# wiederholt solang man will oder bis taste gedrückt wird
def record(intervall,output_dir,praefix):
    global key_pressed
    if intervall <= 0:
        logger.error("Intervall must be greater than 0 and duration must be non-negative.")
        return
    record = False
    first = True
    logger.info("Press p to start!")
    audio = AudioPlayer()
    while True:
        if record:
            screenshot = make_screenshot()
            save_screenshot(screenshot, output_dir, praefix,first)
            first = False
            time.sleep(intervall)
        if key_pressed == "p":
            key_pressed = None
            if record == False:
                audio.start_sound()
            if record:
                logger.info("Stop Recording")
                audio.end_sound()
                break
            record = True
        elif key_pressed == "o":
            key_pressed = None
            logger.info("StillRecording")
            audio.recording_sound()
            

    logger.info("Screen recording finished")


@app.command()
def screen_record_test(
    intervall: int = typer.Option(1, help="Intervall zwischen Screenshots in Sekunden"),
    output_dir: Path = typer.Option(Path(f"data/raw/screenshots/Session_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"), help="Ausgabeverzeichnis"),
    praefix: str = typer.Option("screenshot", help="Präfix für Dateinamen")
):
    listener = Listener(on_press=on_press)
    listener.start()
    record(intervall, output_dir, praefix)
    

    
if __name__ == "__main__":
    app()
    
