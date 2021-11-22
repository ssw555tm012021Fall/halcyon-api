import enum

class Event_State(enum.Enum):
    completed = 'completed'
    cancel = 'cancel'

class Event_Category(enum.Enum):
    guided_meditation = 'guided_meditation'
    meditation = 'meditation'
    water = 'water'
    break_category = 'break'

