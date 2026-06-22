import pytest
from unittest.mock import patch, MagicMock
from deck_cli.fetcher import fetch_brand_data

MOCK_API_RESPONSE = {
    "name": "Stripe",
    "description": "Stripe is a financial infrastructure platform for businesses.",
    "logo": "https://logo.context.dev/stripe.com",
    "colors": {"primary": "#635BFF", "secondary": "#0A2540", "text": "#FFFFFF"},
    "socials": {
        "linkedin": "https://linkedin.com/company/stripe",
        "twitter": "https://twitter.com/stripe"
    },
    "category": "Fintech",
}

@patch("deck_cli.fetcher.requests.get")
def test_fetch_brand_data_success(mock_get):
    mock_resp = MagicMock()
    mock_resp.json.return_value = MOCK_API_RESPONSE
    mock_resp.raise_for_status.return_value = None
    mock_get.return_value = mock_resp

    result = fetch_brand_data("stripe.com", "fake_api_key")

    assert result["company_name"] == "Stripe"
    assert result["primary_color"] == "#635BFF"
    assert result["logo_url"] == "https://logo.context.dev/stripe.com"
    assert result["industry"] == "Fintech"
    assert result["website_url"] == "https://stripe.com"

@patch("deck_cli.fetcher.requests.get")
def test_fetch_brand_data_missing_fields(mock_get):
    mock_resp = MagicMock()
    mock_resp.json.return_value = {}  # Empty response, should use defaults
    mock_resp.raise_for_status.return_value = None
    mock_get.return_value = mock_resp

    result = fetch_brand_data("unknown.com", "fake_api_key")

    assert result["company_name"] == "Unknown"
    assert result["primary_color"] == "#1a1a2e"  # fallback default
