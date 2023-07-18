import ssl
import pywhisper
import openai
from flask import Flask, render_template, request
ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__, template_folder="templates", static_folder="static")
openai.api_key = "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"

@app.route("/", methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        if 'mp3file' in request.files:
            mp3file = request.files['mp3file']
            mp3file.save('audio/audio.mp3')
            return render_template("choice.html")
    return render_template("index.html")


@app.route("/transcribe")
def result():
    model = pywhisper.load_model("tiny.en")
    result = model.transcribe("audio/audio.mp3")
    return render_template("result.html", result=result["text"])

@app.route("/summarize")
def sumslight():
    return render_template("redirect.html")

@app.route("/summarize_res")
def summarize_transcript():
    # Preprocess the transcript
    model = pywhisper.load_model("tiny.en")
    result = model.transcribe("audio/audio.mp3")
    prompt = "Summarize the following transcript: " + result["text"] + "Start the summary with what the lecture was about and then summarize the important points."
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        temperature=0.3,
        n=1,
        stop=None,
    )
    summary = response.choices[0].text.strip()
    return render_template("result.html", result=summary)

if __name__ == "__main__":
    app.debug = True
    app.run()