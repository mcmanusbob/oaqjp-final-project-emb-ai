from flask import Flask, render_template, request
import sys
import os

# Had to use AI to help with the path and accessing the Local Server
sys.path.append(os.path.join(os.path.dirname(__file__), 'oaqjp-final-project-emb-ai'))

from EmotionDetection import emotion_detector

app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')

@app.route("/")
def render_index_page():
    return render_template('index.html')

@app.route("/emotionDetector")
def emotion_detector_route():
    text_to_analyze = request.args.get('textToAnalyze')
    
    if not text_to_analyze:
        return "Invalid text! Please try again!"
    
    response = emotion_detector(text_to_analyze)
    
    if response is None or response.get('dominant_emotion') is None:
        return "Invalid text! Please try again!"
    
    formatted_response = (
        f"For the given statement, the system response is "
        f"'anger': {response['anger']}, "
        f"'disgust': {response['disgust']}, "
        f"'fear': {response['fear']}, "
        f"'joy': {response['joy']} and "
        f"'sadness': {response['sadness']}. "
        f"The dominant emotion is <b>{response['dominant_emotion']}</b>."
    )
    
    return formatted_response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)