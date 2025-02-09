from pydantic import BaseModel, conint
from datetime import datetime
from typing import Optional

class EmotionRecord(BaseModel):
    id: str
    user_id: str  # ID do usuário que registrou o sentimento
    emotion_id: str  # ID da emoção registrada
    intensity: int  # Intensidade entre 1 e 5
    timestamp: datetime = datetime.now()  # Data e hora do registro
    notes: Optional[str] = None  # Notas adicionais (opcional)

    class Config:
        from_attributes = True