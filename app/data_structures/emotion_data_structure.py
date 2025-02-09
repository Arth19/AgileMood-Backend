
class Emotion:
    def __init__(self, name: str):
        self.name: str = name

    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name


emotion_list: [Emotion] = [
    Emotion("Happy"),
    Emotion("Neutral"),
    Emotion("Sad"),
]


def is_valid_emotion(emotion_name: str) -> bool:
    return emotion_name in list(map(lambda x: x.get_name(), emotion_list))


def get_valid_emotion() -> dict[str, [str]]:
    return {"emotions": list(map(lambda x: x.get_name(), emotion_list))}
