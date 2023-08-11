# Slide Gen

CLI tool that can be used to generate a video using ChatGPT, DALLE-2 and
FakeYou. This repo also includes a demo webapp.

### Quickstart

You can easily run the web application with Docker and access it at
`localhost:5000`

```console
make docker-run
```

### CLI

To run the cli application locally you will need `ffmpeg` and `poetry`
installed. Also make sure to export your api key.

```console
sudo apt install ffmpeg
curl -sSL https://install.python-poetry.org | python3 -
export OPENAI_API_KEY=sk-...
poetry install
echo "Please create a presentation about sunflowers." | poetry run slide-gen
```

You can also change the speaker of the video using the `--speaker` flag with a
string taken from the [FakeYou](https://fakeyou.com/) website.
