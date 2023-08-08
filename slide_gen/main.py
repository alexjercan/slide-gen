"""Create a video from a slide presentation"""

import argparse
import os
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


def get_output_run(output):
    """Create a new folder inside the output directory for this run"""
    if not os.path.exists(output):
        os.mkdir(output)

    run = 0
    while os.path.exists(os.path.join(output, str(run))):
        run += 1

    run_path = os.path.join(output, str(run))
    os.mkdir(run_path)

    return run_path


def get_speaker(speaker):
    """Get the speaker model token from the speaker title"""
    try:
        voices = fakeyou.FakeYou().list_voices()
        index = voices.title.index(speaker)
        return voices.modelTokens[index]
    except ValueError:
        print("Speaker not found using default...")
        return SPEAKER


def create_slides(system, speaker, output):
    """Create the slides for the presentation"""
    prompt = sys.stdin.read()

    with open(
        os.path.join(output, "prompt.txt"), "w", encoding="utf-8"
    ) as file:
        file.write(prompt)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": system,
            },
            {"role": "user", "content": prompt},
        ],
    )

    presentation = json.loads(response.choices[0].message.content)

    with open(
        os.path.join(output, "presentation.json"), "w", encoding="utf-8"
    ) as file:
        json.dump(presentation, file, indent=2)

    for index, slide in enumerate(presentation):
        print(slide["text"])
        print(slide["image"])
        print()

        response = openai.Image.create(
            prompt=slide["image"], n=1, size="1024x1024"
        )
        image_url = response["data"][0]["url"]

        path = os.path.join(output, f"slide_{index}.png")
        urllib.request.urlretrieve(image_url, path)

        path = os.path.join(output, f"slide_{index}.wav")
        fakeyou.FakeYou().say(slide["text"], speaker).save(path)


def create_video(output):
    """Create the video from the slides"""
    image_files = sorted(glob.glob(os.path.join(output, "slide_*.png")))
    audio_files = sorted(glob.glob(os.path.join(output, "slide_*.wav")))

    if len(image_files) != len(audio_files):
        raise ValueError("Number of image and audio files must be the same")

    input_streams = []
    for image_file, audio_file in zip(image_files, audio_files):
        input_streams.append(ffmpeg.input(image_file))
        input_streams.append(ffmpeg.input(audio_file))

    ffmpeg.concat(*input_streams, v=1, a=1).output(
        os.path.join(output, "video.mp4")
    ).run()


def main():
    parser = argparse.ArgumentParser(
        description="Create a video from a slide presentation"
    )
    parser.add_argument(
        "--speaker",
        help="The speaker title to use for the presentation",
        default="Morgan Freeman",
        required=False,
    )
    parser.add_argument(
        "--output",
        help="The output directory to use for the files",
        default="videos",
        required=False,
    )

    args = parser.parse_args()

    speaker = get_speaker(args.speaker)
    output = get_output_run(args.output)

    create_slides(SYSTEM, speaker, output)
    create_video(output)
