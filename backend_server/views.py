import json
import datetime


def login(request) -> bytes:
    """
    Handle authentication request.
    """
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
            return json.dumps({"status": 200, "message": "Success", "data": {"token": token, "user_data": {"username": result[1], "email": result[3], "first_name": result[6], "last_name": result[5]}}}).encode()


def get_user(request, pk: int):
    """
    Get user from database, from argument PK -> user id.
    """
    cursor = request.client.database_connection.cursor()
    query = "SELECT * FROM User WHERE id = %s"
    cursor.execute(query, (pk,))
    result = cursor.fetchone()
    cursor.close()
    if result is not None:
        return {"u": result[1], "e": result[3], "fn": result[6], "ln": result[5]}
    else:
        return {"u": f"deleted_user_{pk}", "e": "null", "fn": "null", "ln": "null"}

def get_user_from_username(request, username: str):
    """
    Get user from database, from argument username -> string username.
    """
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
    """
    GET tasks associated to user. [PROTECTED VIEW]
    """
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
    """
    POST > set task to completed status. [PROTECTED VIEW]
    POST data must contain is_completed key BOOL, and task_id key INT
    """
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
    """
    POST > Delete task. [PROTECTED VIEW]
    POST data must contain task_id key INT
    """
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
    """
    POST > Delete tasks. [PROTECTED VIEW]
    POST data must contain task_ids key List
    """
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
    """
    POST > Create task. [PROTECTED VIEW]
    POST data must contain :
    - name String
    - tag String
    - description String
    - start_date String
    - deadline String
    - user String
    - public BOOL
    - importance Int
    """
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
    """
    POST > Create User.
    POST data must contain :
    - username String
    - password String (MD5)
    - email String
    - first_name String
    - last_name String
    """
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

def task_details(request) -> bytes:
    """
    POST > task_details > Get all the details from tasks. [PROTECTED]
    POST data must contain task_ids List
    """
    if request.method == "POST":
        user_id = request.user.data[0]
        try:
            task_ids = request.data
        except AttributeError:
            return json.dumps({"status": 400, "message": "Bad request"}).encode()

        cursor = request.client.database_connection.cursor()
        query = "SELECT * FROM Task WHERE id IN ({})".format(','.join(['%s'] * len(task_ids)))
        cursor.execute(query, (task_ids))
        result = cursor.fetchall()
        cursor.close()
        for i in result:
            if i is not None:
                if i[6] != user_id and i[7] != user_id:
                    return json.dumps({"status": 403, "message": "Forbidden"}).encode()
        message = {"status": 200, "data": []}
        users = {}
        result.reverse()
        found_ids = []
        for i in result:
            if i is not None:
                if i[6] not in users:
                    users[i[6]] = get_user(request, i[6])
                if i[7] not in users:
                    users[i[7]] = get_user(request, i[7])
                found_ids.append(i[0])
                message["data"].append({"id": i[0], "name": i[1], "tag": i[2], "creation_date": str(i[3]), "start_date": str(i[4]), "deadline": str(i[5]), "user": users[i[6]], "creator": users[i[7]], "importance": i[9], "is_complete": i[10], "description": i[11]})

        if len(task_ids) != len(found_ids):
            for task_id in task_ids:
                if task_id not in found_ids:
                    message["data"].append({"id": task_id, "not_found": True})
        return json.dumps(message).encode()

def fetch_requests(request) -> bytes:
    """
    GET number of friends and friend requests from user. [PROTECTED]
    """
    if request.method == "GET":
        user_id = request.user.data[0]
        try:
            cursor = request.client.database_connection.cursor()
            query = f"SELECT * FROM friendships WHERE user2_id = {user_id} AND status = '0'"
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            request_num = len(result)
            cursor = request.client.database_connection.cursor()
            query = f"SELECT * FROM friendships WHERE (user1_id = {user_id} OR user2_id = {user_id}) AND status = '1'"
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            number_of_friends = len(result)

            # result = ["1", "2", "3"] TESTING IF THERE WERE 3 PENDING REQUESTS
            return json.dumps({"status": 200, "data": {"request_num": request_num, "number_of_friends": number_of_friends}}).encode()
        except:
            return json.dumps({"status": 400, "message": "Could get data from database"}).encode()

def friends(request) -> bytes:
    """
    GET all friends from user. [PROTECTED]
    """
    if request.method == "GET":
        user_id = request.user.data[0]
        try:
            cursor = request.client.database_connection.cursor()
            query = f"SELECT * FROM friendships WHERE (user1_id = {user_id} OR user2_id = {user_id}) AND status = '1'"
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            message = {"status": 200, "data": {"friends": []}}
            for i in result:
                if i[1] == user_id:
                    friend = get_user(request, i[2])
                    friend["request_id"] = i[0]
                    message["data"]["friends"].append(friend)
                else:
                    friend = get_user(request, i[1])
                    friend["request_id"] = i[0]
                    message["data"]["friends"].append(friend)
            return json.dumps(message).encode()
        except:
            return json.dumps({"status": 400, "message": "Could get data from database"}).encode()

def friend_request(request) -> bytes:
    """
    GET all friend requests from user. [PROTECTED]

    POST create friend request to user with username [PROTECTED]
    contains keys :
    - username String
    """
    if request.method == "GET":
        user_id = request.user.data[0]
        try:
            cursor = request.client.database_connection.cursor()
            query = f"SELECT * FROM friendships WHERE user2_id = {user_id} AND status = '0'"
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            message = {"status": 200, "data": {"friend_requests": [], "pending_requests": []}}
            for i in result:
                if i[1] == user_id:
                    friend_request = get_user(request, i[2])
                else:
                    friend_request = get_user(request, i[1])
                friend_request["request_id"] = i[0]
                message["data"]["friend_requests"].append(friend_request)
            cursor = request.client.database_connection.cursor()
            query = f"SELECT * FROM friendships WHERE user1_id = {user_id} AND status = '0'"
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            for i in result:
                if i[1] == user_id:
                    friend_request = get_user(request, i[2])
                else:
                    friend_request = get_user(request, i[1])
                friend_request["request_id"] = i[0]
                message["data"]["pending_requests"].append(friend_request)
            return json.dumps(message).encode()
        except:
            return json.dumps({"status": 400, "message": "Could get data from database"}).encode()
    elif request.method == "POST":
        user_id = request.user.data[0]
        try:
            username = request.data["username"]
        except KeyError:
            return json.dumps({"status": 400, "message": "Bad request"}).encode()
        friend_id = get_user_from_username(request, username)
        if friend_id is not None:
            if friend_id != user_id:
                cursor = request.client.database_connection.cursor()
                query = f"SELECT * FROM friendships WHERE user1_id = {user_id} OR user2_id = {user_id}"
                cursor.execute(query)
                result = cursor.fetchall()
                cursor.close()
                for i in result:
                    if i[1] == friend_id or i[2] == friend_id:
                        if i[3] == 1:
                            return json.dumps({"status": 400, "message": "You are already friends with this user !"}).encode()
                        else:
                            if i[2] == user_id:
                                cursor = request.client.database_connection.cursor()
                                query = f"UPDATE friendships SET status = '1' WHERE friendships_id = {i[0]}"
                                cursor.execute(query)
                                request.client.database_connection.commit()
                                cursor.close()
                                return json.dumps({"status": 200, "message": "Friend request accepted !"}).encode()
                            else:
                                return json.dumps({"status": 400, "message": "A friend request is already pending with this user !"}).encode()
                # CREATE FRIEND REQUEST
                cursor = request.client.database_connection.cursor()
                query = f"INSERT INTO friendships (user1_id, user2_id, status) VALUES (%s, %s, %s)"
                cursor.execute(query, (user_id, friend_id, 0))
                request.client.database_connection.commit()
                cursor.close()
                return json.dumps({"status": 200, "message": "Friend request sent !"}).encode()
            else:
                return json.dumps({"status": 400, "message": "You cannot send a friend request to yourself !"}).encode()
        else:
            return json.dumps({"status": 404, "message": "No user was found with matching username"}).encode()

def cancel_friend_request(request) -> bytes:
    """
    POST Cancel friend request [PROTECTED]
    Takes keys:
     - request_id > friendships ID int
    """
    if request.method == "POST":
        user_id = request.user.data[0]
        request_id = request.data["request_id"]
        cursor = request.client.database_connection.cursor()
        query = "SELECT * FROM friendships WHERE friendships_id = %s AND status = '0'"
        cursor.execute(query, (request_id,))
        result = cursor.fetchone()
        cursor.close()
        if result is not None:
            if result[1] == user_id:
                cursor = request.client.database_connection.cursor()
                query = f"DELETE FROM friendships WHERE friendships_id = {result[0]}"
                cursor.execute(query)
                request.client.database_connection.commit()
                cursor.close()
                return json.dumps({"status": 200, "message": "Cancelled friend request."}).encode()
            else:
                return json.dumps({"status": 403, "message": "You are not allowed to perform this action"}).encode()
        else:
            return json.dumps({"status": 404, "message": "Friend request is no longer available"}).encode()

def accept_friend_request(request) -> bytes:
    """
    POST accept friend request [PROTECTED]
    Takes keys:
       - request_id > friendships ID int
    """
    if request.method == "POST":
        user_id = request.user.data[0]
        request_id = request.data["request_id"]
        cursor = request.client.database_connection.cursor()
        query = "SELECT * FROM friendships WHERE friendships_id = %s AND status = '0'"
        cursor.execute(query, (request_id,))
        result = cursor.fetchone()
        cursor.close()
        if result is not None:
            if result[2] == user_id:
                cursor = request.client.database_connection.cursor()
                query = f"UPDATE friendships SET status = '1' WHERE friendships_id = {result[0]}"
                cursor.execute(query)
                request.client.database_connection.commit()
                cursor.close()
                return json.dumps({"status": 200, "message": "Friend request accepted !"}).encode()
            else:
                return json.dumps({"status": 403, "message": "You are not allowed to perform this action"}).encode()
        else:
            return json.dumps({"status": 404, "message": "Friend request is no longer available"}).encode()


def deny_friend_request(request) -> bytes:
    """
    POST deny friend request [PROTECTED]
    Takes keys:
        - request_id > friendships ID int
    """
    if request.method == "POST":
        user_id = request.user.data[0]
        request_id = request.data["request_id"]
        cursor = request.client.database_connection.cursor()
        query = "SELECT * FROM friendships WHERE friendships_id = %s AND status = '0'"
        cursor.execute(query, (request_id,))
        result = cursor.fetchone()
        cursor.close()
        if result is not None:
            if result[2] == user_id:
                cursor = request.client.database_connection.cursor()
                query = f"DELETE FROM friendships WHERE friendships_id = {result[0]}"
                cursor.execute(query)
                request.client.database_connection.commit()
                cursor.close()
                return json.dumps({"status": 200, "message": "Denied friend request."}).encode()
            else:
                return json.dumps({"status": 403, "message": "You are not allowed to perform this action"}).encode()
        else:
            return json.dumps({"status": 404, "message": "Friend request is no longer available"}).encode()

def remove_friend(request) -> bytes:
    """
    POST remove friend [PROTECTED]
    Takes keys:
    - request_id > friendships ID int
    """
    if request.method == "POST":
        user_id = request.user.data[0]
        request_id = request.data["request_id"]
        cursor = request.client.database_connection.cursor()
        query = "SELECT * FROM friendships WHERE friendships_id = %s AND status = '1'"
        cursor.execute(query, (request_id,))
        result = cursor.fetchone()
        cursor.close()
        if result is not None:
            if result[2] == user_id or result[1] == user_id:
                cursor = request.client.database_connection.cursor()
                query = f"DELETE FROM friendships WHERE friendships_id = {result[0]}"
                cursor.execute(query)
                request.client.database_connection.commit()
                cursor.close()
                return json.dumps({"status": 200, "message": "Removed friend"}).encode()
            else:
                return json.dumps({"status": 403, "message": "You are not allowed to perform this action"}).encode()
        else:
            return json.dumps({"status": 404, "message": "You are not friends with this user"}).encode()