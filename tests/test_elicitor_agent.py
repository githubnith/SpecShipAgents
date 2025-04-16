import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import json

# Add parent directory to path to import agents
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.elicitor_agent import (
    DevelopmentDetails,
    RequirementDetails,
    elicitor_agent
)
from pydantic_ai import Agent

class TestDevelopmentDetails(unittest.TestCase):
    def test_development_details_creation(self):
        """Test creating DevelopmentDetails with valid data"""
        details = DevelopmentDetails(
            is_new_build=True,
            requires_be_build=True,
            requires_mobile=False,
            requires_shared_services=True
        )
        self.assertTrue(details.is_new_build)
        self.assertTrue(details.requires_be_build)
        self.assertFalse(details.requires_mobile)
        self.assertTrue(details.requires_shared_services)

    def test_development_details_validation(self):
        """Test that DevelopmentDetails validates boolean fields"""
        with self.assertRaises(ValueError):
            DevelopmentDetails(
                is_new_build="not a boolean",  # Should be boolean
                requires_be_build=True,
                requires_mobile=False,
                requires_shared_services=True
            )

class TestRequirementDetails(unittest.TestCase):
    def setUp(self):
        """Set up test data"""
        self.valid_dev_details = DevelopmentDetails(
            is_new_build=True,
            requires_be_build=True,
            requires_mobile=False,
            requires_shared_services=True
        )
        
        self.valid_data = {
            "response": "All details collected successfully",
            "specific_requirement": "Add payment gateway to mobile app",
            "lob_design_approval": {"approver": "John Doe", "evidence": "Email dated 2025-04-16"},
            "lob_senior_approval": {"approver": "Jane Smith", "evidence": "Meeting minutes"},
            "test_cases": ["Test payment success", "Test payment failure", "Test timeout"],
            "development_details": self.valid_dev_details,
            "business_value": "Increase revenue by 20% through mobile payments",
            "success_definition": "Successful integration with payment gateway",
            "success_metrics": ["Transaction success rate", "Payment volume", "User adoption"],
            "target_date": "01-05-2025",
            "date_implications": "Delay in revenue generation",
            "impacted_applications": ["Mobile App", "Payment Service"],
            "all_details_given": True
        }

    def test_requirement_details_creation(self):
        """Test creating RequirementDetails with valid data"""
        details = RequirementDetails(**self.valid_data)
        self.assertEqual(details.specific_requirement, "Add payment gateway to mobile app")
        self.assertEqual(len(details.test_cases), 3)
        self.assertTrue(details.all_details_given)

    def test_requirement_details_missing_fields(self):
        """Test that RequirementDetails requires all fields"""
        invalid_data = self.valid_data.copy()
        del invalid_data["specific_requirement"]
        with self.assertRaises(ValueError):
            RequirementDetails(**invalid_data)

    def test_requirement_details_invalid_list(self):
        """Test that list fields validate correctly"""
        invalid_data = self.valid_data.copy()
        invalid_data["success_metrics"] = "not a list"
        with self.assertRaises(ValueError):
            RequirementDetails(**invalid_data)

    def test_requirement_details_invalid_dict(self):
        """Test that dictionary fields validate correctly"""
        invalid_data = self.valid_data.copy()
        invalid_data["lob_design_approval"] = "not a dict"
        with self.assertRaises(ValueError):
            RequirementDetails(**invalid_data)

class TestElicitorAgent(unittest.TestCase):
    def setUp(self):
        """Set up test data and mock the model"""
        self.mock_model = MagicMock()
        self.mock_get_model = patch('agents.elicitor_agent.get_model', return_value=self.mock_model).start()

    def tearDown(self):
        """Clean up patches"""
        patch.stopall()

    def test_agent_creation(self):
        """Test that the elicitor agent is created correctly"""
        self.assertIsNotNone(elicitor_agent)
        self.assertIsInstance(elicitor_agent, Agent)

    def test_agent_system_prompt(self):
        """Test that the system prompt contains key validation rules"""
        from agents.elicitor_agent import system_prompt
        prompt = system_prompt.lower()
        self.assertIn("never make assumptions", prompt)
        self.assertIn("what exactly needs to be done", prompt)
        self.assertIn("new build or an enhancement", prompt)

if __name__ == '__main__':
    unittest.main()
