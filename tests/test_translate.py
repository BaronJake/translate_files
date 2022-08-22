from unittest import TestCase
from mock import patch, MagicMock
from scripts import translate


class test_translate(TestCase):
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

    def test_error_response(self):
        """Should raise error if error in response from API"""
        pass

    def test_get_arguments(self):
        """Should get arguments from commandline"""
        pass

    def test_error_no_API_KEY(self):
        """Should raise error if API_KEY not set"""
        pass

    def test_txt_file_translation(self):
        """Should read text from txt file and run translation"""
        pass

    def test_po_file_translation(self):
        """Should read text from po files and run translation"""
        pass
