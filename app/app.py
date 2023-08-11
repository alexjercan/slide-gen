"""App"""
import os

from flask import Flask, render_template, request

from slide_gen import Args, pipeline

app = Flask(
    __name__,
    static_url_path="/videos",
    static_folder="../videos",
    template_folder="templates",
)
videos_path = os.path.join(app.root_path, "..", "videos")
os.makedirs(videos_path, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    api_key = request.form.get("api_key")
    prompt = request.form.get("prompt")

    args = Args(prompt, "Morgan Freeman", videos_path)
    path = pipeline(args, api_key)
    mp4_path = os.path.join(path, "video.mp4")

    response = f"""
    <h1>Video Generated</h1>
    <video width="1024" height="1024" controls>
        <source src="{mp4_path}" type="video/mp4">
    </video>
    """

    return response


class Video:
    def __init__(self, video):
        self.video = video

    @property
    def title(self):
        path = os.path.join(videos_path, self.video, "prompt.txt")
        with open(os.path.join(path), encoding="utf-8") as f:
            return f.read()

    @property
    def url(self):
        return os.path.join("videos", self.video, "video.mp4")


@app.route("/gallery")
def gallery():
    videos = []
    for video in os.listdir(videos_path):
        videos.append(Video(video))

    return render_template("gallery.html", videos=videos)
