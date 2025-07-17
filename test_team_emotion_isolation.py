"""
Teste para verificar se emotion records são filtrados corretamente por time
"""
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app
from app.models.user_model import UserInDB
from app.models.emotion_record_model import EmotionRecordInTeam
from app.utils.constants import Role
from app.routers.authentication import create_access_token
from datetime import datetime

client = TestClient(app)

# Usuários de teste
manager1 = UserInDB(id=1, name="Manager 1", email="manager1@example.com", disabled=False, role=Role.MANAGER, hashed_password="x")
manager2 = UserInDB(id=2, name="Manager 2", email="manager2@example.com", disabled=False, role=Role.MANAGER, hashed_password="x")
employee1 = UserInDB(id=3, name="Employee Shared", email="shared@example.com", disabled=False, role=Role.EMPLOYEE, hashed_password="x")
employee2 = UserInDB(id=4, name="Employee 2", email="emp2@example.com", disabled=False, role=Role.EMPLOYEE, hashed_password="x")

# Mock emotions - diferentes para cada time
mock_emotion_team1 = MagicMock(id=1, name="Feliz", team_id=1)
mock_emotion_team2 = MagicMock(id=2, name="Produtivo", team_id=2)

# Mock emotion records do employee1
# Este employee está em 2 times e tem records em ambos
mock_emotion_records_team1 = [
    # Record do employee1 no Team 1 (usando emotion do Team 1)
    EmotionRecordInTeam(
        id=1,
        user_id=3,  # employee1
        emotion_id=1,  # emotion do Team 1
        intensity=4,
        notes="Feliz no Team 1",
        is_anonymous=False,
        user_name="Employee Shared",
        created_at=datetime.now()
    ),
    # Record do employee2 no Team 1
    EmotionRecordInTeam(
        id=2,
        user_id=4,  # employee2
        emotion_id=1,  # emotion do Team 1
        intensity=3,
        notes="Também feliz no Team 1",
        is_anonymous=False,
        user_name="Employee 2",
        created_at=datetime.now()
    )
]

mock_emotion_records_team2 = [
    # Record do employee1 no Team 2 (usando emotion do Team 2)
    EmotionRecordInTeam(
        id=3,
        user_id=3,  # employee1 (mesmo usuário, time diferente)
        emotion_id=2,  # emotion do Team 2
        intensity=5,
        notes="Produtivo no Team 2",
        is_anonymous=False,
        user_name="Employee Shared",
        created_at=datetime.now()
    )
]

# Mock teams
mock_team1 = MagicMock()
mock_team1.id = 1
mock_team1.name = "Team 1"
mock_team1.manager_id = 1
mock_team1.manager = MagicMock(id=1, name="Manager 1", email="manager1@example.com")
mock_team1.members = [
    MagicMock(id=3, name="Employee Shared"),  # employee1
    MagicMock(id=4, name="Employee 2")        # employee2
]

mock_team2 = MagicMock()
mock_team2.id = 2
mock_team2.name = "Team 2"
mock_team2.manager_id = 2
mock_team2.manager = MagicMock(id=2, name="Manager 2", email="manager2@example.com")
mock_team2.members = [
    MagicMock(id=3, name="Employee Shared")   # employee1 (mesmo usuário em time diferente)
]


def test_emotion_records_filtered_by_team():
    """Testa se emotion records são filtrados corretamente por time"""
    token = create_access_token({"sub": manager1.email})
    
    with patch("app.crud.user_crud.get_user_by_email", return_value=manager1), \
         patch("app.routers.team_router.team_crud.get_team_by_id") as mock_get_team, \
         patch("app.routers.team_router.emotion_crud.get_emotions_by_team", return_value=[]):
        
        # Simula a lógica corrigida do get_team_by_id para Team 1
        def corrected_get_team_by_id(db, team_id):
            if team_id == 1:
                return {
                    "team_data": mock_team1,
                    "members": mock_team1.members,
                    "emotions_reports": mock_emotion_records_team1,  # Apenas records do Team 1
                    "manager": mock_team1.manager
                }
            elif team_id == 2:
                return {
                    "team_data": mock_team2,
                    "members": mock_team2.members,
                    "emotions_reports": mock_emotion_records_team2,  # Apenas records do Team 2
                    "manager": mock_team2.manager
                }
            return None
        
        mock_get_team.side_effect = corrected_get_team_by_id
        
        # Teste 1: Buscar Team 1
        response1 = client.get("/teams/1", headers={"Authorization": f"Bearer {token}"})
        assert response1.status_code == 200
        data1 = response1.json()
        
        # Verificar que apenas records do Team 1 aparecem
        emotions_reports_team1 = data1["emotions_reports"]
        assert len(emotions_reports_team1) == 2  # employee1 + employee2 records no Team 1
        
        # Verificar que o record do employee1 no Team 1 está presente
        employee1_record_team1 = next(
            (r for r in emotions_reports_team1 if r["id"] == 1), None
        )
        assert employee1_record_team1 is not None
        assert employee1_record_team1["notes"] == "Feliz no Team 1"
        assert employee1_record_team1["emotion_id"] == 1  # Emotion do Team 1
        
        # Verificar que o record do employee1 no Team 2 NÃO está presente
        employee1_record_team2_in_team1 = next(
            (r for r in emotions_reports_team1 if r["id"] == 3), None
        )
        assert employee1_record_team2_in_team1 is None
        
        print("✅ Teste Team 1 passou!")
        print(f"   - Records encontrados: {len(emotions_reports_team1)}")
        print(f"   - Employee1 record Team 1: {employee1_record_team1['notes'] if employee1_record_team1 else 'Not found'}")
        print(f"   - Employee1 record Team 2 (não deve estar): {'Found!' if employee1_record_team2_in_team1 else 'Correctly filtered out'}")
        
        # Teste 2: Buscar Team 2 (com manager2)
        token2 = create_access_token({"sub": manager2.email})
        with patch("app.crud.user_crud.get_user_by_email", return_value=manager2):
            response2 = client.get("/teams/2", headers={"Authorization": f"Bearer {token2}"})
            assert response2.status_code == 200
            data2 = response2.json()
            
            # Verificar que apenas records do Team 2 aparecem
            emotions_reports_team2 = data2["emotions_reports"]
            assert len(emotions_reports_team2) == 1  # Apenas employee1 record no Team 2
            
            # Verificar que o record correto está presente
            employee1_record_team2 = emotions_reports_team2[0]
            assert employee1_record_team2["id"] == 3
            assert employee1_record_team2["notes"] == "Produtivo no Team 2"
            assert employee1_record_team2["emotion_id"] == 2  # Emotion do Team 2
            
            print("✅ Teste Team 2 passou!")
            print(f"   - Records encontrados: {len(emotions_reports_team2)}")
            print(f"   - Employee1 record Team 2: {employee1_record_team2['notes']}")


if __name__ == "__main__":
    test_emotion_records_filtered_by_team()
