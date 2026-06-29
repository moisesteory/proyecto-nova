import random

QUESTIONS = [

    "¿Qué fue lo primero que te hizo enamorarte de tu pareja?",

    "¿Cuál ha sido uno de los momentos más felices que han vivido juntos?",

    "¿Qué es algo que admiras de tu pareja y pocas veces le dices?",

    "¿Qué sueño te gustaría cumplir juntos?",

    "¿Qué detalle reciente de tu pareja te hizo sentir amado?"
    
    "¿Como fue que se conocieron?"
]


def random_question():
    return random.choice(QUESTIONS)