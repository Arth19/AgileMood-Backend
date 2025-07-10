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

# app/core/auth_utils.py
def ensure_is_team_manager(team: Union[Team, Dict[str, Any]], user: UserInDB):
    # 1️⃣ captura manager_id se for objeto ORM
    if hasattr(team, "manager_id"):
        manager_id = team.manager_id
    # 2️⃣ se for wrapper dict, pega do campo interno "team_data"
    elif "team_data" in team and hasattr(team["team_data"], "manager_id"):
        manager_id = team["team_data"].manager_id
    # 3️⃣ último fallback p/ dicts planos (caso mude no futuro)
    else:
        manager_id = team.get("manager_id")

    if _normalize(manager_id) != _normalize(user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para acessar esse time.",
        )

def ensure_is_team_member_or_manager(team: Union[Team, Dict[str, Any]], user: UserInDB):
    """Garantir que o usuário gerencia ou participa do time."""
    # 1️⃣ captura dados quando for objeto ORM
    if hasattr(team, "manager_id"):
        manager_id = getattr(team, "manager_id", None)
        members = getattr(team, "members", [])
    # 2️⃣ se for wrapper dict, pega do campo interno "team_data"
    elif isinstance(team, dict) and "team_data" in team:
        team_data = team["team_data"]
        # evita AttributeError quando team_data for ORM
        manager_id = getattr(team_data, "manager_id", None)
        if manager_id is None and isinstance(team_data, dict):
            manager_id = team_data.get("manager_id")
        members = team.get("members", [])
    else:
        manager_id = team.get("manager_id") if isinstance(team, dict) else None
        members = team.get("members", []) if isinstance(team, dict) else []

    member_ids = { _normalize(getattr(m, "id", None)) for m in members if getattr(m, "id", None) is not None }
    user_id_norm = _normalize(user.id)

    if user_id_norm != _normalize(manager_id) and user_id_norm not in member_ids:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para acessar esse time.",
        )