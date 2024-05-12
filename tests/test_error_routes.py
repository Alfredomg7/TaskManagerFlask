import pytest

def test_404_error_page(client):
    """Test that the custom 404 error page is displayed when an invalid URL is accessed."""
    response = client.get('/no-valid-route')
    assert response.status_code == 404
    assert '404 - Oops! Page Not Found' in response.get_data(as_text=True)

def test_505_error_page(client):
    """Test that the custom 500 error page is displayed when an internal server error occurs"""
    response = client.get('/500-error')
    print(response.data)
    assert response.status_code == 500
    assert '500 - Internal Server Error' in response.get_data(as_text=True)