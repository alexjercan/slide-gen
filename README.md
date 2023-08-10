# Slide Gen

CLI tool that can be used to generate a video using ChatGPT, DALLE-2 and FakeYou.

### Requirements

To run the application you will need `ffmpeg` and `poetry` installed. Also make
sure to export your api key.

```console
sudo apt install ffmpeg
curl -sSL https://install.python-poetry.org | python3 -
```

### Quickstart

Install the dependencies and run the tool with a custom prompt.

```console
poetry install
echo "Please create a presentation about sunflowers." | poetry run slide-gen
```

### Speaker

You can also change the speaker of the video using the `--speaker` flag with a
string taken from the [FakeYou](https://fakeyou.com/) website.
