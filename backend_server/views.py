import json
import datetime


def login(request) -> bytes:
    if request.method == "POST":
        try:
            username = request.data["username"]
            password = request.data["password"]
            if username == "" or password == "":
                return json.dumps({"status": 400, "message": "Form is invalid"}).encode()
            else:
                pass
        except KeyError:
            return json.dumps({"status": 400, "message": "Form is invalid"}).encode()
        if not request.client.check_username(username):  # Basically check if the username doesn't exist
            return json.dumps({"status": 401, "message": "Username doesn't exist"}).encode()
        result = request.client.check_username_and_password(username, password)
        if not result:  # Basically check if password is not valid
            return json.dumps({"status": 401, "message": "Password is invalid"}).encode()
        else:
            # The token contains the username, and date and be encrypted with the secret key.
            # token : username + "," + md5_password + "," + time Encrypted secret key
            token = request.client.generate_token(username, password).decode()
            return json.dumps({"status": 200, "message": "Success", "data": {"token": token, "user_data": {"username": result[1], "email": result[3]}}}).encode()


def get_user(request, pk: int, friend=False):
    cursor = request.client.database_connection.cursor()
    query = "SELECT * FROM User WHERE id = %s"
    cursor.execute(query, (pk,))
    result = cursor.fetchone()
    cursor.close()
    if result is not None:
        if not friend:
            return {"u": result[1], "e": result[3]}
        else:
            return {"u": result[1], "e": result[3], "fn": result[6], "ln": result[5]}
    else:
        if friend:
            return {"u": f"deleted_user_{pk}", "e": "null", "fn": "null", "ln": "null"}
        else:
            return {"u": f"deleted_user_{pk}", "e": "null"}

def get_user_from_username(request, username: str):
    cursor = request.client.database_connection.cursor()
    query = "SELECT * FROM User WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    cursor.close()
    if result is not None:
        return result[0]
    else:
        return None


def tasks(request) -> bytes:
    if request.method == "GET":
        user_id = request.user.data[0]
        cursor = request.client.database_connection.cursor()
        query = "SELECT * FROM Task WHERE user_id = %s OR created_by = %s"
        cursor.execute(query, (user_id, user_id,))
        result = cursor.fetchall()
        cursor.close()
        message = {"status": 200, "data": []}
        users = {}
        result.reverse()
        for i in result:
            if i[6] not in users:
                users[i[6]] = get_user(request, i[6])
            if i[7] not in users:
                users[i[7]] = get_user(request, i[7])
            if i[6] == user_id:
                is_owner = True
            else:
                is_owner = False
            message["data"].append({"id": i[0], "N": i[1], "T": i[2], "SD": str(i[4]), "DL": str(i[5]), "ow": users[i[6]], "io": is_owner, "pu": i[8], "im": i[9], "IC": i[10]})
        return json.dumps(message).encode()


def set_completed(request) -> bytes:
    if request.method == "POST":
        user_id = request.user.data[0]
        try:
            task_id = request.data["task_id"]
            is_completed = request.data["is_completed"]
        except KeyError:
            return json.dumps({"status": 400, "message": "Request is invalid"}).encode()
        cursor = request.client.database_connection.cursor()
        query = "SELECT * FROM Task WHERE id = %s"
        cursor.execute(query, (task_id, ))
        result = cursor.fetchone()
        cursor.close()
        if result is None:
            return json.dumps({"status": 404, "message": "Not found", "data": {"task_id": task_id}}).encode()
        if result[6] != user_id and result[7] != user_id:
            return json.dumps({"status": 403, "message": "Forbidden"}).encode()
        cursor = request.client.database_connection.cursor()
        query = "UPDATE Task SET is_completed = %s WHERE id = %s"
        cursor.execute(query, (is_completed, task_id,))
        request.client.database_connection.commit()
        cursor.close()
        return json.dumps({"status": 200, "message": "Success", "data": {"task_id": task_id, "is_completed": is_completed}}).encode()


def delete_task(request) -> bytes:
    if request.method == "POST":
        user_id = request.user.data[0]
        try:
            task_id = request.data["task_id"]
        except KeyError:
            return json.dumps({"status": 400, "message": "Request is invalid"}).encode()
        cursor = request.client.database_connection.cursor()
        query = "SELECT * FROM Task WHERE id = %s"
        cursor.execute(query, (task_id,))
        result = cursor.fetchone()
        cursor.close()
        if result is None:
            return json.dumps({"status": 404, "message": "Task not found", "data": {"task_id": task_id}}).encode()
        if result[6] != user_id and result[7] != user_id:
            return json.dumps({"status": 403, "message": "Forbidden"}).encode()
        try:
            cursor = request.client.database_connection.cursor()
            query = "DELETE FROM Task WHERE id = %s"
            cursor.execute(query, (task_id,))
            request.client.database_connection.commit()
            cursor.close()
        except:
            pass
        return json.dumps({"status": 200, "message": "Success", "data": {"task_id": task_id, "is_deleted": True}}).encode()


def delete_tasks(request) -> bytes:
    if request.method == "POST":
        user_id = request.user.data[0]
        try:
            task_ids = request.data["task_ids"]
        except KeyError:
            return json.dumps({"status": 400, "message": "Request is invalid"}).encode()
        list_of_ids = ",".join(map(str, task_ids))
        cursor = request.client.database_connection.cursor()
        query = f"SELECT * FROM Task WHERE id IN ({list_of_ids})"
        cursor.execute(query)
        result = cursor.fetchall()
        found_ids = []
        cursor.close()
        for i in result:
            found_ids.append(i[0])
            if i[6] != user_id and i[7] != user_id:
                return json.dumps({"status": 403, "message": "Forbidden"}).encode()
        cursor = request.client.database_connection.cursor()
        query = f"DELETE FROM Task WHERE id IN ({list_of_ids});"
        cursor.execute(query)
        request.client.database_connection.commit()
        cursor.close()
        message = {"status": 200, "message": "Success", "data": {"task_ids": task_ids, "tasks": []}}
        for task_id in task_ids:
            if task_id not in found_ids:
                message["data"]["tasks"].append({"id": task_id, "status": 404})
            else:
                message["data"]["tasks"].append({"id": task_id, "status": 200})
        return json.dumps(message).encode()


def create_task(request) -> bytes:
    if request.method == "POST":
        user_id = request.user.data[0]  # User id that creates the task
        try:
            name = request.data["name"]
            tag = request.data["tag"]
            description = request.data["description"]
            start_date = request.data["start_date"]
            deadline = request.data["deadline"]
            if deadline == "None":
                deadline = None
            user = request.data["user"]
            public = request.data["public"]
            importance = request.data["importance"]
        except KeyError:
            return json.dumps({"status": 400, "message": "Bad request"}).encode()
        if len(name) > 20:
            return json.dumps({"status": 401, "message": "Length of name cannot be longer than 20 characters!"}).encode()
        if description is not None and len(description) > 500:
            return json.dumps({"status": 401, "message": "Length of description cannot be longer than 500 characters!"}).encode()
        if len(tag) > 20:
            return json.dumps({"status": 401, "message": "Length of tag cannot be longer than 20 characters!"}).encode()
        task_user_id = get_user_from_username(request, user)
        if task_user_id is None:
            return json.dumps({"status": 404, "message": "The specified user doesn't exist."}).encode()
        if task_user_id == user_id:
            is_owner = True
        else:
            is_owner = False
        cursor = request.client.database_connection.cursor()
        query = f"INSERT INTO Task (name, tag, date_created, start_date, deadline, user_id, created_by, public, importance, is_completed, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        creation_date = str(datetime.datetime.now())
        cursor.execute(query, (name, tag, creation_date, start_date, deadline, task_user_id, user_id, public, importance, False, description))
        request.client.database_connection.commit()
        task_id = cursor.lastrowid
        cursor.close()
        return json.dumps({"status": 200, "message": "Ok", "data": {"is_created": True, "task": {"id": task_id, "N": name, "T": tag, "SD": start_date, "ow": {"u": user, "e": "null"}, "io": is_owner, "pu": public, "IC": False, "DL": deadline}}}).encode()

def create_user(request) -> bytes:
    if request.method == "POST":
        try:
            username = request.data["username"]
            password = request.data["password"]
            email = request.data["email"]
            first_name = request.data["first_name"]
            last_name = request.data["last_name"]
        except KeyError:
            return json.dumps({"status": 400, "message": "Bad request"}).encode()
        if len(username) < 4:
            return json.dumps({"status": 401, "message": "Length of username should be at least 4 characters !"}).encode()
        special_characters = """!@#${}[]`%^&*()-+?=,<>/ "'"""
        if any(c in special_characters for c in username):
            return json.dumps({"status": 401, "message": "Username cannot contain special characters or spaces !"}).encode()
        elif len(username) > 40:
            return json.dumps({"status": 401, "message": "Length of username cannot exceed 40 characters !"}).encode()
        # DON'T FORGET TO : Check if email is valid [...]
        if request.client.check_username(username):
            return json.dumps({"status": 401, "message": f"Account with username : '{username}' already exists !"}).encode()
        if request.client.check_email(email):
            return json.dumps({"status": 401, "message": f"Account with email : '{email}' already exists !"}).encode()
        cursor = request.client.database_connection.cursor()
        query = f"INSERT INTO User (username, password, email, first_name, last_name) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (username, password, email, first_name, last_name))
        request.client.database_connection.commit()
        cursor.close()
        return json.dumps({"status": 200, "message": "Ok", "data": {"is_created": True}}).encode()

