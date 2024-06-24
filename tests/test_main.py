import unittest
from unittest.mock import patch

import httpx
from fastapi.testclient import TestClient

# Assuming these imports are correct and the modules exist
from src.main import app
from src.models import FetchMessagesResponse, Report, Message

# Initialize the test client
client = TestClient(app)


class TestMain(unittest.TestCase):
    @patch('src.main.fetch_data')
    def test_get_usage_returns_correct_response_when_all_requests_succeed(self, mock_fetch_data):
        mock_message = Message(id=1, timestamp="2022-01-01T00:00:00Z", report_id="1", text="Hello, world!")
        # Mock the responses for the fetch_data calls
        mock_fetch_data.side_effect = [
            FetchMessagesResponse(messages=[mock_message]),
            Report(name="Report 1", credit_cost=1.0)
        ]

        response = client.get("/usage")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"usage": [
            {"message_id": 1, "timestamp": "2022-01-01T00:00:00Z", "credits_used": 1.0, "report_name": "Report 1"}]})

    @patch('src.main.fetch_data')
    def test_get_usage_returns_correct_response_when_report_request_fails_with_404(self, mock_fetch_data):
        mock_message = Message(id=1, timestamp="2022-01-01T00:00:00Z", report_id="1", text="Hello, world!")
        mock_fetch_data.side_effect = [
            FetchMessagesResponse(messages=[mock_message]),
            httpx.HTTPStatusError(response=httpx.Response(404, text="Not Found"), message="Not Found", request=None)
        ]

        response = client.get("/usage")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                         {"usage": [{"message_id": 1, "timestamp": "2022-01-01T00:00:00Z",
                                     "report_name": None, "credits_used": 1.0}]})

    @patch('src.main.fetch_data')  # Adjust this to match where your HTTP client is actually used
    def test_get_usage_returns_500_when_messages_request_fails(self, mock_fetch_data):
        mock_fetch_data.side_effect = Exception("Internal Server Error")

        response = client.get("/usage")

        self.assertEqual(response.status_code, 500)


if __name__ == '__main__':
    unittest.main()