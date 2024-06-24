import unittest
from unittest.mock import patch
from src.main import app
from fastapi.testclient import TestClient
from src.models import FetchMessagesResponse, Report

# Initialize the test client
client = TestClient(app)


# Define the test cases
class TestMain(unittest.TestCase):
    # Test the /usage endpoint when all requests succeed
    @patch('httpx.get')
    def test_get_usage_returns_correct_response_when_all_requests_succeed(self, mock_get):
        # Mock the responses for the httpx.get calls
        mock_get.side_effect = [
            FetchMessagesResponse(messages=[{"id": "1", "timestamp": "2022-01-01T00:00:00Z", "report_id": "1"}]),
            Report(name="Report 1", credit_cost=1.0)
        ]

        # Make a request to the /usage endpoint and check the response
        response = client.get("/usage")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"usage": [
            {"message_id": "1", "timestamp": "2022-01-01T00:00:00Z", "credits_used": 1.0, "report_name": "Report 1"}]})

    # Test the /usage endpoint when the report request fails with a 404 error
    @patch('httpx.get')
    def test_get_usage_returns_correct_response_when_report_request_fails_with_404(self, mock_get):
        # Mock the responses for the httpx.get calls
        mock_get.side_effect = [
            FetchMessagesResponse(messages=[{"id": "1", "timestamp": "2022-01-01T00:00:00Z", "report_id": "1"}]),
            Exception("Not Found")
        ]

        # Make a request to the /usage endpoint and check the response
        response = client.get("/usage")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                         {"usage": [{"message_id": "1", "timestamp": "2022-01-01T00:00:00Z", "credits_used": 0.0}]})

    # Test the /usage endpoint when the messages request fails
    @patch('httpx.get')
    def test_get_usage_returns_500_when_messages_request_fails(self, mock_get):
        # Mock the response for the httpx.get call
        mock_get.side_effect = Exception("Internal Server Error")

        # Make a request to the /usage endpoint and check the response
        response = client.get("/usage")

        self.assertEqual(response.status_code, 500)


# Run the tests
if __name__ == '__main__':
    unittest.main()
