import glob
import json
import sys
import urllib.request

import fakeyou
import ffmpeg
import openai

SYSTEM = """Your job is to create a slide presentation for a video. \
In this presentation you must include a speech for the current slide and a \
description for the background image. You need to make it as story-like as \
possible. The format of the output must be in JSON. You have to output a list \
of objects. Each object will contain a key for the speech called "text" and a \
key for the image description called "image".

For example for a slide presentation about the new iphone you could output \
something like:

```
[
  {
    "text": "Hello. Today we will discuss about the new iphone",
    "image": "Image of a phone on a business desk with a black background"
  },
  {
    "text": "Apple is going to release this new iphone this summer",
    "image": "A group of happy people with phones in their hand"
  },
  {
    "text": "Thank you for watching my presentation",
    "image": "A thank you message on white background"
  }
]
```

Make sure to output only JSON text. Do not output any extra comments.
"""
SPEAKER = "TM:cpwrmn5kwh97"


def create_slides():
    prompt = sys.stdin.read()

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": SYSTEM,
            },
            {"role": "user", "content": prompt},
        ],
    )

    presentation = json.loads(response.choices[0].message.content)

    for index, slide in enumerate(presentation):
        print(slide["text"])
        print(slide["image"])
        print()

        response = openai.Image.create(prompt=slide["image"], n=1, size="1024x1024")
        image_url = response["data"][0]["url"]

        urllib.request.urlretrieve(image_url, f"slide_{index}.png")

        fakeyou.FakeYou().say(slide["text"], SPEAKER).save(f"slide_{index}.wav")


def create_video():
    image_files = sorted(glob.glob("slide_*.png"))
    audio_files = sorted(glob.glob("slide_*.wav"))

    if len(image_files) != len(audio_files):
        raise ValueError("Number of image and audio files must be the same")

    input_streams = []
    for image_file, audio_file in zip(image_files, audio_files):
        input_streams.append(ffmpeg.input(image_file))
        input_streams.append(ffmpeg.input(audio_file))

    ffmpeg.concat(*input_streams, v=1, a=1).output("output.mp4").run()


def main():
    create_slides()
    create_video()
