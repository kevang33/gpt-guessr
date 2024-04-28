# GPTGuessr

## Can LLM's play GeoGuessr?

This repository contains a single script which passes screenshots of the game [GeoGuessr](https://www.geoguessr.com/) into the [GPT-4 Vision API](https://platform.openai.com/docs/guides/vision) as a fun test of it's performance. I was able to achieve a score of 23811/25000 on No Moving, providing two images per round. 

## How to use

1. Clone the repo `git clone https://github.com/kevang33/gpt-guessr.git`
2. cd into the repo `cd gpt-guessr`
3. Install dependencies `pip install -r requirements.txt`
4. With a game of GeoGuessr open, Run `python gptguessr.py`. It is recommended to use a second monitor for the GeoGuessr window.
5. After a short delay, the first screenshot will be taken. Another short delay will follow before the second screenshot: it is recommended to turn around during this time to provide the model with more information on where you are
6. Use the prediction to make your guess!

## Video Coming Soon!
