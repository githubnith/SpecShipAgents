import os
import sys
import unittest
from unittest.mock import patch

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import get_model
from pydantic_ai.models.openai import OpenAIModel

class TestUtils(unittest.TestCase):
    def setUp(self):
        # Clear any existing environment variables before each test
        if 'MODEL_CHOICE' in os.environ:
            del os.environ['MODEL_CHOICE']
        if 'BASE_URL' in os.environ:
            del os.environ['BASE_URL']
        if 'LLM_API_KEY' in os.environ:
            del os.environ['LLM_API_KEY']

    def test_get_model_default_values(self):
        """Test get_model with default environment values"""
        model = get_model()
        self.assertIsInstance(model, OpenAIModel)
        # We can only test that the model is created, but can't access internal attributes

    def test_get_model_custom_values(self):
        """Test get_model with custom environment values"""
        with patch.dict(os.environ, {
            'MODEL_CHOICE': 'gpt-4',
            'BASE_URL': 'https://custom.api.com/v1',
            'LLM_API_KEY': 'test-key'
        }):
            model = get_model()
            self.assertIsInstance(model, OpenAIModel)
            # We can only test that the model is created with the custom environment

    def test_get_model_partial_env_vars(self):
        """Test get_model with only some environment variables set"""
        with patch.dict(os.environ, {
            'MODEL_CHOICE': 'gpt-3.5-turbo',
            'LLM_API_KEY': 'another-key'
        }):
            model = get_model()
            self.assertIsInstance(model, OpenAIModel)
            # We can only test that the model is created with partial environment

if __name__ == '__main__':
    unittest.main()
