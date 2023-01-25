def test_register(client, session):
    """
    회원가입 성공 테스트
    :param session:
    :param client:
    :return:
    """
    body = dict(email="abc@gmail.com", pw="hashpw123!")
    response = client.post("users/register", json=body)
    assert response.status_code == 400
    session.rollback()

    body = dict(email="abc@gmail.com", pw="hashpw")
    response = client.post("users/register", json=body)
    assert response.status_code == 400
    session.rollback()

    body = dict(email="xyz@gmail.com", pw="HHADF2")
    response = client.post("users/register", json=body)
    assert response.status_code == 400
    session.rollback()

    body = dict(email="aa1@gmail.com", pw="123123")
    response = client.post("users/register", json=body)
    assert response.status_code == 400
    session.rollback()

    body = dict(email="bb1@gmail.com", pw="aB2")
    response = client.post("users/register", json=body)
    assert response.status_code == 400
    session.rollback()

    body = dict(email="aa2@gmail.com", pw="ThisisPW00")
    response = client.post("users/register", json=body)
    assert response.status_code == 201