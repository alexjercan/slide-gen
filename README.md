# Slide Gen

CLI tool that can be used to generate a video using ChatGPT, DALLE-2 and FakeYou.

### Quickstart

Install the dependencies and run the tool with a custom prompt.

```console
poetry shell
poetry install
echo "Please create a presentation about sunflowers." | poetry run slide-gen
```

### Speaker

You can also change the speaker of the video using the `--speaker` flag with a
string taken from the [FakeYou](https://fakeyou.com/) website.
