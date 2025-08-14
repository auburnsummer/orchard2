from django.test import Client

def test_index_page_loads(bridge_client: Client):
    resp = bridge_client.get("/")
    assert resp.status_code == 200
    assert resp.json()['props'] == {}