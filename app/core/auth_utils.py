# app/core/auth_utils.py
from decimal import Decimal
from typing import Any, Dict, Union
from fastapi import HTTPException, status
from app.models.team_model import Team
from app.models.user_model import UserInDB

def _normalize(value: Any) -> str:
    """Converte id para string para comparação segura."""
    if isinstance(value, Decimal):
        value = int(value)
    return str(value)

def ensure_is_team_manager(team: Union[Team, Dict[str, Any]], user: UserInDB):
    # aceita objeto ou dict
    manager_id = team.manager_id if hasattr(team, "manager_id") else team.get("manager_id")

    if _normalize(manager_id) != _normalize(user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para acessar esse time.",
        )
