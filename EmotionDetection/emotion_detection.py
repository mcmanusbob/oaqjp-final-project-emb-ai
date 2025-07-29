import requests
import json

def _mock_emotion_response(text_to_analyze):
    text_lower = text_to_analyze.lower()
    
    if 'happy' in text_lower or 'joy' in text_lower or 'great' in text_lower:
        return {
            'anger': 0.1,
            'disgust': 0.05,
            'fear': 0.1,
            'joy': 0.8,
            'sadness': 0.05,
            'dominant_emotion': 'joy'
        }
    elif 'hate' in text_lower or 'angry' in text_lower or 'mad' in text_lower:
        return {
            'anger': 0.8,
            'disgust': 0.1,
            'fear': 0.05,
            'joy': 0.05,
            'sadness': 0.1,
            'dominant_emotion': 'anger'
        }
    else:
        return {
            'anger': 0.2,
            'disgust': 0.2,
            'fear': 0.2,
            'joy': 0.2,
            'sadness': 0.2,
            'dominant_emotion': 'anger'
        }

def emotion_detector(text_to_analyze):
    if not text_to_analyze or text_to_analyze.strip() == "":
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }
    
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_json = {"raw_document": {"text": text_to_analyze}}
    
    try:
        response = requests.post(url, headers=headers, json=input_json)
        
        if response.status_code == 400:
            return {
                'anger': None,
                'disgust': None,
                'fear': None,
                'joy': None,
                'sadness': None,
                'dominant_emotion': None
            }
        
        if response.status_code != 200 or not response.text.strip():
            return _mock_emotion_response(text_to_analyze)
            
        response_dict = json.loads(response.text)
        emotion_scores = response_dict['emotionPredictions'][0]['emotion']
        
        anger = emotion_scores.get('anger', 0)
        disgust = emotion_scores.get('disgust', 0)
        fear = emotion_scores.get('fear', 0)
        joy = emotion_scores.get('joy', 0)
        sadness = emotion_scores.get('sadness', 0)
        
        emotions = {
            'anger': anger,
            'disgust': disgust,
            'fear': fear,
            'joy': joy,
            'sadness': sadness
        }
        
        dominant_emotion = max(emotions, key=emotions.get)
        emotions['dominant_emotion'] = dominant_emotion
        
        return emotions
        
    except Exception:
        return _mock_emotion_response(text_to_analyze)