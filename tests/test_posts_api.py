from flask import Flask
import json
from app import create_app

def test_patch_route():
    testapp = create_app()
    client = testapp.test_client()
    url = '/api/posts/1'

    mock_request_headers = {
        'x-access-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNzAzMjU4OTAyfQ.6Vvo4L69tp1UZb447fTUWjXOOsY-AMD8rUfNsTah5hY',
        'Content-Type': 'application/json'
    }

    mock_request_data = {
	'authorIds': [3,4],
    'text': 'This is some text for the blog post...',
    'tags': ['travel', 'hotel']
    }

    response = client.patch(url, data=json.dumps(mock_request_data), headers=mock_request_headers)
    assert response.status_code == 200

def test_get_route():
    testapp = create_app()
    client = testapp.test_client()
    url = '/api/posts'

    mock_request_headers = {
        'Content-Type': 'application/json'
    }

    mock_request_data = {
    'authorIds': '1,2,3,4',
	'sortBy': 'popularity',
	'direction': 'desc'
    }

    response = client.get(url, data=json.dumps(mock_request_data), headers=mock_request_headers)
    assert response.status_code == 200