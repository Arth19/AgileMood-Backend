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
