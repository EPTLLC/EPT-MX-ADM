"""
Simple tests to verify testing infrastructure works
"""
import pytest
import os
import sys


class TestBasicFunctionality:
    """Basic functionality tests"""
    
    def test_python_version(self):
        """Test Python version is 3.10+"""
        assert sys.version_info >= (3, 10)
    
    def test_project_structure(self):
        """Test basic project structure exists"""
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        
        # Check main files exist
        assert os.path.exists(os.path.join(base_path, 'app.py'))
        assert os.path.exists(os.path.join(base_path, 'requirements.txt'))
        assert os.path.exists(os.path.join(base_path, 'config'))
        assert os.path.exists(os.path.join(base_path, 'utils'))
        assert os.path.exists(os.path.join(base_path, 'modules'))
        assert os.path.exists(os.path.join(base_path, 'blueprints'))
    
    def test_import_main_app(self):
        """Test that main app can be imported"""
        try:
            from app import create_app
            assert callable(create_app)
        except ImportError as e:
            pytest.fail(f"Cannot import create_app: {e}")
    
    def test_config_import(self):
        """Test that config can be imported"""
        try:
            from config.settings import Config
            assert hasattr(Config, 'APP_NAME')
            assert hasattr(Config, 'APP_VERSION')
        except ImportError as e:
            pytest.fail(f"Cannot import Config: {e}")


class TestMathOperations:
    """Simple math tests to verify pytest works"""
    
    def test_addition(self):
        """Test basic addition"""
        assert 2 + 2 == 4
        assert 10 + 5 == 15
    
    def test_subtraction(self):
        """Test basic subtraction"""
        assert 10 - 5 == 5
        assert 0 - 1 == -1
    
    def test_multiplication(self):
        """Test basic multiplication"""
        assert 3 * 4 == 12
        assert 0 * 100 == 0
    
    def test_division(self):
        """Test basic division"""
        assert 10 / 2 == 5
        assert 15 / 3 == 5
    
    def test_division_by_zero(self):
        """Test division by zero raises exception"""
        with pytest.raises(ZeroDivisionError):
            10 / 0


class TestStringOperations:
    """String operation tests"""
    
    def test_string_concatenation(self):
        """Test string concatenation"""
        assert "Hello" + " " + "World" == "Hello World"
    
    def test_string_formatting(self):
        """Test string formatting"""
        name = "EPT-MX-ADM"
        version = "0.0.1-beta"
        result = f"{name} v{version}"
        assert result == "EPT-MX-ADM v0.0.1-beta"
    
    def test_string_methods(self):
        """Test string methods"""
        text = "  Hello World  "
        assert text.strip() == "Hello World"
        assert text.upper().strip() == "HELLO WORLD"
        assert text.lower().strip() == "hello world" 