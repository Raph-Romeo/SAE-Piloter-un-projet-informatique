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
