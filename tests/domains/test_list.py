import pytest

# this test is written to pass when 2 domains are running per test-machines-up.sh
def test_list_default(client):
    rv = client.get("/domains")
    assert b'Test' in rv.data
