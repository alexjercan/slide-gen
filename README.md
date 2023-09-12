# Slide Gen

Web tool that can be used to generate a video using ChatGPT, DALLE-2 and
FakeYou.

### Quickstart

You can easily run the web application with Docker and access it at
`localhost:5000`. You will need to add an environment variable for the
`OPENAI_API_KEY`. To use better FakeYou queue you need to define
`FAKEYOU_USERNAME` and `FAKEYOU_PASSWORD`. However these are paid services.

```console
export OPENAI_API_KEY=sk-...
export FAKEYOU_USERNAME=...
export FAKEYOU_PASSWORD=...
make docker-run
```
