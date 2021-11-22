from sqlalchemy_cockroachdb import run_transaction

# from data.db import session, sessionmaker
from data.sound import Sound
from server import db


def get_file_by_id(file_id):
    sound_file = db.session.query(Sound).filter(Sound.id == file_id).first()
    sound_map = {}
    sound_map['id'] = sound_file.id
    sound_map['name'] = sound_file.name
    sound_map['description'] = sound_file.description
    sound_map['length'] = sound_file.length
    sound_map['credit'] = sound_file.credit
    sound_map['audio'] = sound_file.url
    sound_map['picture'] = sound_file.picture
    return sound_map

def get_files(sound_type):
    files = db.session.query(Sound).filter(Sound.type == sound_type).all()
    file_list = []
    for sound_file in files:
        sound_map = {}
        sound_map['id'] = sound_file.id
        sound_map['name'] = sound_file.name
        sound_map['description'] = sound_file.description
        sound_map['length'] = sound_file.length
        sound_map['credit'] = sound_file.credit
        sound_map['audio'] = sound_file.url
        sound_map['picture'] = sound_file.picture
        file_list.append(sound_map)
    return file_list



