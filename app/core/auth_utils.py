from typing import Any, Dict, Union
from fastapi import HTTPException, status
from app.models.team_model import Team
from app.models.user_model import UserInDB

def ensure_is_team_manager(team: Union[Team, Dict[str, Any]], user: UserInDB):
    """Raise 403 if the current user is not the team manager."""
    # Extrai manager_id seja de objeto ou de dict
    manager_id = team.manager_id if hasattr(team, "manager_id") else team.get("manager_id")

    if manager_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para acessar esse time.",
        )
