import json
import datetime


def login(request) -> bytes:
    if request.method == "POST":
        try:
            # TAS CHANGER CA
            username = request.data["username"]
            password = request.data["password"]
            if username == "" or password == "":
                return json.dumps({"status": 400, "message": "Form is invalid"}).encode()
            else:
                pass
        except KeyError:
            return json.dumps({"status": 400, "message": "Form is invalid"}).encode()
        if not request.client.check_username(username):  # Basically check if the username or email doesn't exist
            return json.dumps({"status": 401, "message": "Username or email doesn't exist"}).encode()
        result = request.client.check_username_and_password(username, password)
        if not result:  # Basically check if password is not valid
            return json.dumps({"status": 401, "message": "Password is invalid"}).encode()
        else:
            # The token contains the username, and date and be encrypted with the secret key.
            # token : username + "," + md5_password + "," + time Encrypted secret key
            token = request.client.generate_token(username, password).decode()
            return json.dumps({"status": 200, "message": "Success", "data": {"token": token, "user_data": {"username": result[1], "email": result[3]}}}).encode()


def get_user(request, pk: int):
    cursor = request.client.database_connection.cursor()
    query = "SELECT * FROM User WHERE id = %s"
    cursor.execute(query, (pk,))
    result = cursor.fetchone()
    cursor.close()
    return {"username": result[1], "email": result[3]}


def tasks(request) -> bytes:
    if request.method == "GET":
        user_id = request.user.data[0]
        cursor = request.client.database_connection.cursor()
        query = "SELECT * FROM Task WHERE user_id = %s OR created_by = %s"
        cursor.execute(query, (user_id, user_id,))
        result = cursor.fetchall()
        cursor.close()
        message = {"status": 200, "message": "Success", "data": []}
        users = {}
        for i in result:
            if i[6] not in users:
                users[i[6]] = get_user(request, i[6])
            if i[7] not in users:
                users[i[7]] = get_user(request, i[7])
            if i[6] == user_id:
                is_owner = True
            else:
                is_owner = False
            message["data"].append({"id": i[0], "name": i[1], "tag": i[2], "date_created": str(i[3]), "start_date": str(i[4]), "deadline": str(i[5]), "owner": users[i[6]], "is_owner": is_owner, "created_by": users[i[7]], "public": i[8], "important": i[9], "is_completed": i[10]})
        return json.dumps(message).encode()


def create_task(request) -> bytes:
    if request.method == "POST":
        user_id = request.user.data[0]  # User id that creates the task
        try:
            name = request.data["name"]
        except KeyError:
            return json.dumps({"status": 400, "message": "Request is invalid"}).encode()
        cursor = request.client.database_connection.cursor()
        query = f"INSERT INTO Task (name, tag, date_created, start_date, deadline, user_id, created_by, public, importance, is_completed) VALUES('{name}','University','2023-12-17 12:56:00','2023-12-12 15:56:00','2023-12-26 16:00:00','{user_id}','{user_id}',true,1, FALSE)"
        cursor.execute(query)
        request.client.database_connection.commit()
        cursor.close()
        return json.dumps({"status": 200, "message": "Ok", "data": {"is_created": True}}).encode()
