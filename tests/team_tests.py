from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app
from app.models.user_model import UserInDB
from app.utils.constants import Role
from app.routers.authentication import create_access_token

client = TestClient(app)

manager_user = UserInDB(id=1, name="Manager", email="manager@example.com", disabled=False, role=Role.MANAGER, hashed_password="x")
employee_user = UserInDB(id=2, name="Employee", email="employee@example.com", disabled=False, role=Role.EMPLOYEE, hashed_password="x")
outsider_user = UserInDB(id=3, name="Other", email="other@example.com", disabled=False, role=Role.EMPLOYEE, hashed_password="x")

mock_team = {
    "team_data": MagicMock(id=1, manager_id=1),
    "members": [MagicMock(id=2)],
    "emotions_reports": []
}


def test_employee_can_get_team():
    token = create_access_token({"sub": employee_user.email})
    with patch("app.crud.user_crud.get_user_by_email", return_value=employee_user), \
         patch("app.routers.team_router.team_crud.get_team_by_id", return_value=mock_team), \
         patch("app.routers.team_router.emotion_crud.get_emotions_by_team", return_value=[]):
        response = client.get("/teams/1", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200


def test_outsider_cannot_get_team():
    token = create_access_token({"sub": outsider_user.email})
    with patch("app.crud.user_crud.get_user_by_email", return_value=outsider_user), \
         patch("app.routers.team_router.team_crud.get_team_by_id", return_value=mock_team):
        response = client.get("/teams/1", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 403


def test_employee_can_get_team_emotions():
    token = create_access_token({"sub": employee_user.email})
    with patch("app.crud.user_crud.get_user_by_email", return_value=employee_user), \
         patch("app.routers.team_router.team_crud.get_team_by_id", return_value=mock_team), \
         patch("app.routers.team_router.emotion_crud.get_emotions_by_team", return_value=[]):
        response = client.get("/teams/1/emotions", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
