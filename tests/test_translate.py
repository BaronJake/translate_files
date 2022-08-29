"""Tests for translate script"""
from unittest import TestCase
from mock import patch, MagicMock
from scripts import translate


class TestTranslate(TestCase):
    """Tests for translate script"""

    @patch("scripts.translate.requests.post")
    def test_translate(self, mock_request):
        """Should call Google Translate API"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {"translations": [{"translatedText": "Igpay Atinlay"}]}
        }
        mock_request.return_value = mock_response
        with patch("scripts.translate.API_KEY", "fake_key"):
            translated_text = translate.translate_text("en", "zz", "Pig Latin")
        mock_request.assert_called_once()
        self.assertEqual(translated_text, "Igpay Atinlay")

    @patch("scripts.translate.requests.post")
    def test_error_response(self, mock_request):
        """Should raise error if error in response from API"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "error": {"code": 1234546, "message": "Cannot Compute!"}
        }
        mock_request.return_value = mock_response
        with patch("scripts.translate.API_KEY", "fake_key"):
            with self.assertRaises(ValueError):
                translate.translate_text("en", "zz", "Pig Latin")

    @patch("scripts.translate.requests.post")
    def test_error_status_code(self, mock_request):
        """Should raise error if Status code is not 200"""
        mock_response = MagicMock()
        mock_response.status_code = 403
        mock_response.json.return_value = {
            "data": {"translations": [{"translatedText": "Igpay Atinlay"}]}
        }
        mock_request.return_value = mock_response
        with patch("scripts.translate.API_KEY", "fake_key"):
            with self.assertRaises(ConnectionError):
                translate.translate_text("en", "zz", "Pig Latin")

    def test_error_no_key(self):
        """Should raise error if API_KEY not set"""
        with self.assertRaises(ValueError):
            translate.get_arguments()
