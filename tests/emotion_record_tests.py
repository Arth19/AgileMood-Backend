from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app
from app.models.user_model import UserInDB
from app.models.emotion_record_model import EmotionRecordInDb, IntensityEnum
from app.utils.constants import Role
from app.routers.authentication import create_access_token

client = TestClient(app)

logged_user = UserInDB(
    id=1,
    name="User",
    email="user@example.com",
    disabled=False,
    role=Role.EMPLOYEE,
    hashed_password="x",
)

mock_record = EmotionRecordInDb(
    id=1,
    user_id=1,
    emotion_id=2,
    intensity=IntensityEnum.THREE,
    notes="ok",
    is_anonymous=False,
)


def test_get_emotion_record_by_id():
    token = create_access_token({"sub": logged_user.email})
    with patch("app.crud.user_crud.get_user_by_email", return_value=logged_user), patch(
        "app.routers.emotion_record_router.emotion_record_crud.get_emotion_record_by_id",
        return_value=mock_record,
    ):
        response = client.get(
            "/emotion_record/id/1", headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        assert response.json()["id"] == 1


def test_get_emotion_record_by_id_not_found():
    token = create_access_token({"sub": logged_user.email})
    with patch("app.crud.user_crud.get_user_by_email", return_value=logged_user), patch(
        "app.routers.emotion_record_router.emotion_record_crud.get_emotion_record_by_id",
        return_value=None,
    ):
        response = client.get(
            "/emotion_record/id/1", headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404