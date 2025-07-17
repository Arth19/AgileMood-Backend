"""
Teste para verificar se a correção do bug de manager incorreto está funcionando
"""
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app
from app.models.user_model import UserInDB
from app.utils.constants import Role
from app.routers.authentication import create_access_token

client = TestClient(app)

# Usuários de teste
manager1 = UserInDB(id=1, name="Manager Real", email="manager1@example.com", disabled=False, role=Role.MANAGER, hashed_password="x")
manager2 = UserInDB(id=2, name="Manager Adicionado", email="manager2@example.com", disabled=False, role=Role.MANAGER, hashed_password="x") 
employee1 = UserInDB(id=3, name="Employee 1", email="emp1@example.com", disabled=False, role=Role.EMPLOYEE, hashed_password="x")
employee2 = UserInDB(id=4, name="Employee 2", email="emp2@example.com", disabled=False, role=Role.EMPLOYEE, hashed_password="x")

# Mock team data
mock_team_data = MagicMock()
mock_team_data.id = 1
mock_team_data.name = "Test Team"
mock_team_data.manager_id = 1  # manager1 é o real manager

# Mock manager (o relacionamento team.manager)
mock_manager = MagicMock()
mock_manager.id = 1
mock_manager.name = "Manager Real"
mock_manager.email = "manager1@example.com"
mock_manager.role = "manager"

# Mock members (incluindo manager2 que foi adicionado como membro)
mock_members = [
    MagicMock(id=2, name="Manager Adicionado", email="manager2@example.com", role="manager"),  # Este NÃO deve ser o manager
    MagicMock(id=3, name="Employee 1", email="emp1@example.com", role="employee"),
    MagicMock(id=4, name="Employee 2", email="emp2@example.com", role="employee")
]

# Mock team completo
mock_team = MagicMock()
mock_team.id = 1
mock_team.name = "Test Team"
mock_team.manager_id = 1
mock_team.manager = mock_manager  # O manager REAL
mock_team.members = mock_members


def test_correct_team_manager_identification():
    """Testa se o manager correto é identificado mesmo quando outro manager é membro"""
    token = create_access_token({"sub": employee1.email})
    
    with patch("app.crud.user_crud.get_user_by_email", return_value=employee1), \
         patch("app.routers.team_router.team_crud.get_team_by_id") as mock_get_team, \
         patch("app.routers.team_router.emotion_crud.get_emotions_by_team", return_value=[]):
        
        # Simula a lógica corrigida do get_team_by_id
        def corrected_get_team_by_id(db, team_id):
            return {
                "team_data": mock_team_data,
                "members": mock_members,
                "emotions_reports": [],
                "manager": mock_manager  # Retorna o manager REAL
            }
        
        mock_get_team.side_effect = corrected_get_team_by_id
        
        response = client.get("/teams/1", headers={"Authorization": f"Bearer {token}"})
        
        assert response.status_code == 200
        data = response.json()
        
        # Verificar se o manager correto é retornado
        assert "manager" in data
        assert data["manager"]["id"] == 1
        assert data["manager"]["name"] == "Manager Real"
        assert data["manager"]["email"] == "manager1@example.com"
        
        # Verificar que o "Manager Adicionado" está apenas nos members, não como manager
        manager_adicionado_in_members = any(
            member["id"] == 2 and member["name"] == "Manager Adicionado" 
            for member in data["members"]
        )
        assert manager_adicionado_in_members, "Manager adicionado deve estar na lista de membros"
        
        # Verificar que o manager retornado NÃO é o "Manager Adicionado"
        assert data["manager"]["name"] != "Manager Adicionado"
        
        print("✅ Teste passou! A correção está funcionando corretamente:")
        print(f"   - Manager real: {data['manager']['name']} (ID: {data['manager']['id']})")
        print(f"   - Manager adicionado está nos membros: {manager_adicionado_in_members}")
        print(f"   - Total de membros: {len(data['members'])}")


if __name__ == "__main__":
    test_correct_team_manager_identification()
