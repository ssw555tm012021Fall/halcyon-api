from sqlalchemy_cockroachdb import run_transaction

# from data.db import session, sessionmaker
from data.mood_activity import mood_activity
from server import db

def get_moods():
    moods = db.session.query(mood_activity).all()
    moods_list = []
    for mood in moods:
        mood_map = {}
        mood_map['id'] = mood.id
        mood_map['inputEmotion'] = mood.input_emotion
        mood_map['activity'] = mood.activity
        mood_map['outputEmotion'] = mood.output_emotion
        moods_list.append(mood_map)
    return moods_list



