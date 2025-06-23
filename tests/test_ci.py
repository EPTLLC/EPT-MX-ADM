"""
Simple CI test to verify testing infrastructure works in GitHub Actions
"""
import sys
import os


def test_ci_environment():
    """Test that CI environment is properly set up"""
    # Check Python version
    assert sys.version_info >= (3, 10)
    
    # Check that we can import basic modules
    import json
    import datetime
    import pathlib
    
    # Basic assertions
    assert 1 + 1 == 2
    assert "test" == "test"
    assert len("hello") == 5


def test_project_files_exist():
    """Test that essential project files exist"""
    project_root = os.path.dirname(os.path.dirname(__file__))
    
    essential_files = [
        'app.py',
        'requirements.txt',
        'README.md',
        'config',
        'utils',
        'modules',
        'blueprints'
    ]
    
    for file_path in essential_files:
        full_path = os.path.join(project_root, file_path)
        assert os.path.exists(full_path), f"Missing essential file/directory: {file_path}"


def test_python_imports():
    """Test that we can import Python standard library modules"""
    try:
        import json
        import os
        import sys
        import datetime
        import pathlib
        import urllib
        import http
        
        # Test basic functionality
        data = {"test": "value"}
        json_str = json.dumps(data)
        parsed = json.loads(json_str)
        assert parsed["test"] == "value"
        
    except ImportError as e:
        assert False, f"Failed to import standard library module: {e}"


def test_flask_can_be_imported():
    """Test that Flask can be imported (main dependency)"""
    try:
        import flask
        assert hasattr(flask, 'Flask')
        assert hasattr(flask, 'request')
        assert hasattr(flask, 'session')
    except ImportError:
        assert False, "Cannot import Flask - check requirements.txt" 