from fastapi import HTTPException, status
from app.models.team_model import Team
from app.models.user_model import UserInDB

def ensure_is_team_manager(team: Team, user: UserInDB):
    """403 se o usuário não for o gestor do time."""
    if team.manager_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para operar neste time.",
        )
