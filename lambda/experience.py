# experience.py

SCENES = [
    {
        "id": 1,
        "speech": (
            "Perfecto... "
            "Antes de continuar quiero pedirles algo... "
            "Tómense de las manos... "
            "No hablen todavía... "
            "Solo mírense durante treinta segundos... "
            "Cuando estén listos, digan continuar."
        )
    },
    {
        "id": 2,
        "speech": (
            "Muy bien. "
            "Ahora quiero que se abracen durante veinte segundos. "
            "No digan nada. "
            "Solo disfruten el momento. "
            "Cuando terminen, digan continuar."
        )
    },
        {
        "id": 3,
        "speech": (
            "Excelente. "
            "Ahora mírense a los ojos y sonrían. "
            "Cuando estén listos, digan continuar."
        )
    },
    {
        "id": 4,
        "speech": "Ahora quiero hacerles una pregunta."
    }
]


def get_scene(scene_id):
    for scene in SCENES:
        if scene["id"] == scene_id:
            return scene

    return None