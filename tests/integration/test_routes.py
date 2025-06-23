import pytest


class TestAuthRoutes:
    """Authentication routes integration tests"""
    
    def test_login_page_get(self, client):
        """Test GET request to login page"""
        response = client.get("/login")
        assert response.status_code == 200
    
    def test_logout(self, authenticated_session):
        """Test logout functionality"""
        response = authenticated_session.get("/logout")
        assert response.status_code == 302


class TestDashboardRoutes:
    """Dashboard routes integration tests"""
    
    def test_dashboard_requires_auth(self, client):
        """Test authentication requirement for dashboard"""
        response = client.get("/dashboard")
        assert response.status_code == 302
        assert "login" in response.location
