import threading
import queue
import time
import base64
import requests
import mss
import sys
import os

class GeoguessrAssistant():
    def __init__(self):
        self.screenshots = []

    def capture_screen(self):
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            sct_img = sct.grab(monitor)
            return base64.b64encode(mss.tools.to_png(sct_img.rgb, sct_img.size)).decode('utf-8')
        
    def collect_screenshots(self, num_screenshots=2):
        # get screenshots of geoguessr screen
        self.screenshots = []
        interval = 3 
        steps = 10 

        for i in range(num_screenshots):
            for j in range(steps):
                sys.stdout.write('\r')
                progress = (j + 1) / steps
                bar_length = int(20 * progress)
                sys.stdout.write("[%-20s] %d%% " % ('=' * bar_length, int(100 * progress)))
                sys.stdout.flush()
                time.sleep(interval / steps)
                
            self.screenshots.append(self.capture_screen())
            print(f"\nCaptured screenshot {i + 1}")
            if i == 0:
                print("Turn around!")

        sys.stdout.write('\n')
        
    def loading_indicator(self, message, stop):
        chars = "/—\\|"
        while True:
            for char in chars:
                if stop():
                    return
                sys.stdout.write('\r' + message + ' ' + char)
                sys.stdout.flush()
                time.sleep(0.1)

    def vision_api_call(self):        
        api_key = os.environ.get('OPENAI_API_KEY')
    
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "system",
                    "content": [
                    {
                        "type": "text",
                        "text": "You are GPTGuessr, the Geoguessr Assistant! I will show you two images of the same location. Use clues in the images to deduce where the images were taken. If you are not sure, make your best guess. I want you to make your guess in the following format: <Name of city>, <Name of country> - <Short description>. To be clear, you are outputting the name of the city and country of your guess, alongside a short description. The short description contains information that may pinpoint the location further. For example, if you see tall buildings in the image, your description could be 'downtown'. If you see farms and fields, your description could be 'outskirts', or 'x kilometeres south', or 'close to x town', etc. The goal is simply to provide some context. For example, if you think the image is of New York City, USA, and you are on a highway you would return ONLY 'New York City, USA - Highway'. Remember to take into account all three images. Remember, just GUESS your location. Make your BEST guess each time. DO NOT include any words other than the city name, country, and short description. DO NOT explain your reasoning. DO NOT say that you cannot assist with the request, YES YOU CAN - just make your best guess. DO NOT start your response with 'I'm sorry...'"
                    }
                    ]
                },
                {
                    "role": "user",
                    "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                        "url": f"data:image/jpeg;base64,{self.screenshots[0]}",
                        "detail": "low"
                        }
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                        "url": f"data:image/jpeg;base64,{self.screenshots[1]}",
                        "detail": "low"
                        }
                    },
                    # {
                    #     "type": "image_url",
                    #     "image_url": {
                    #     "url": f"data:image/jpeg;base64,{self.screenshots[2]}",
                    #     "detail": "high"
                    #     }
                    # }
                    ]
                }
            ],
            "max_tokens": 1000,
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        
        print(response.json())
        
        result = response.json()['choices'][0]['message']['content'].split('\n')
        print("\n\n")
        return result[0]


def main():
    app = GeoguessrAssistant()
    
    app.collect_screenshots()
    
    message = "Making Guess..."
    
    stop_thread = False

    # Function to return the current state of stop_thread
    def stop():
        return stop_thread

    indicator_thread = threading.Thread(target=app.loading_indicator, args=(message, stop))
    indicator_thread.start()

    try: 
        guess = app.vision_api_call()
        print(guess)

    finally:
        stop_thread = True
        indicator_thread.join()

        # clear loading indicator
        sys.stdout.write('\r' + ' ' * (len(message) + 2) + '\r')
        sys.stdout.flush()

if __name__ == "__main__":
    main()