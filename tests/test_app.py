from urllib.parse import quote


def test_get_activities(client):
    # Arrange: client fixture

    # Act
    resp = client.get("/activities")

    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_success(client):
    # Arrange
    activity = "Chess Club"
    email = "tester1@mergington.edu"

    # Act
    resp = client.post(f"/activities/{quote(activity)}/signup?email={quote(email)}")

    # Assert
    assert resp.status_code == 200
    assert email in client.get("/activities").json()[activity]["participants"]


def test_duplicate_signup_returns_400(client):
    # Arrange
    activity = "Chess Club"
    email = "tester2@mergington.edu"

    # Act
    first = client.post(f"/activities/{quote(activity)}/signup?email={quote(email)}")
    second = client.post(f"/activities/{quote(activity)}/signup?email={quote(email)}")

    # Assert
    assert first.status_code == 200
    assert second.status_code == 400
    assert "already signed up" in second.json().get("detail", "").lower()


def test_signup_unknown_activity_returns_404(client):
    # Arrange
    activity = "Nonexistent Club"
    email = "noone@mergington.edu"

    # Act
    resp = client.post(f"/activities/{quote(activity)}/signup?email={quote(email)}")

    # Assert
    assert resp.status_code == 404


def test_unregister_success(client):
    # Arrange
    activity = "Chess Club"
    email = "tester3@mergington.edu"
    client.post(f"/activities/{quote(activity)}/signup?email={quote(email)}")

    # Act
    resp = client.delete(f"/activities/{quote(activity)}/signup?email={quote(email)}")

    # Assert
    assert resp.status_code == 200
    assert email not in client.get("/activities").json()[activity]["participants"]


def test_unregister_missing_participant_returns_404(client):
    # Arrange
    activity = "Chess Club"
    email = "not-registered@mergington.edu"

    # Act
    resp = client.delete(f"/activities/{quote(activity)}/signup?email={quote(email)}")

    # Assert
    assert resp.status_code == 404
