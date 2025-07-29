import requests
import json

PROJECT_ID = "teamf-ae838"

class FirestoreAPI:
    def __init__(self, project_id, collection):
        self.base_url = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/(default)/documents"
        self.collection = collection 

    #User API

    def add_user(self, username, password_hash, salt_b64):
        """Add a new user with a hashed password and salt (base64 encoded)"""
        url = f"{self.base_url}/{self.collection}"
        data = {
            "fields": {
                "username": {"stringValue": username},
                "password": {"stringValue": password_hash},
                "salt": {"stringValue": salt_b64}
            }
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            doc_path = response.json()["name"]
            doc_id = doc_path.split("/")[-1]
            return doc_id
        else:
            print("Add user failed:", response.content)
            return None

    def get_user_by_username(self, username):
        """Fetch a user by their username"""
        url = f"{self.base_url}/{self.collection}?pageSize=100"
        response = requests.get(url)
        if response.status_code == 200:
            for user_doc in response.json().get("documents", []):
                fields = user_doc["fields"]
                if "username" in fields and fields["username"]["stringValue"] == username:
                    return {
                        "doc_id": user_doc["name"].split("/")[-1],
                        "username": fields["username"]["stringValue"],
                        "password": fields.get("password", {}).get("stringValue", ""),
                        "salt": fields.get("salt", {}).get("stringValue", "")
                    }
            return None  # Not found
        else:
            print("Fetch user failed:", response.content)
            return None
    #Task API

    def add_task(self, user_id, task_title, task_date="", task_time=""):
        url = f"{self.base_url}/{self.collection}"
        data = {
            "fields": {
                "user_id": {"stringValue": user_id},  # Add user association here
                "title": {"stringValue": task_title},
                "completed": {"booleanValue": False},
                "date": {"stringValue": task_date},
                "time": {"stringValue": task_time}
            }
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            doc_path = response.json()["name"]
            doc_id = doc_path.split("/")[-1]
            return doc_id
        else:
            print("Add task failed:", response.content)
            return None

    def get_tasks(self, user_id):
        # Use Firestore REST API's structuredQuery to filter by user_id
        url = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents:runQuery"
        query = {
            "structuredQuery": {
                "from": [{"collectionId": self.collection}],
                "where": {
                    "fieldFilter": {
                        "field": {"fieldPath": "user_id"},
                        "op": "EQUAL",
                        "value": {"stringValue": user_id}
                    }
                }
            }
        }
        response = requests.post(url, json=query)
        if response.status_code == 200:
            tasks = []
            for doc in response.json():
                if "document" in doc:
                    fields = doc["document"]["fields"]
                    title = fields["title"]["stringValue"]
                    date = fields.get("date", {}).get("stringValue", "")
                    time = fields.get("time", {}).get("stringValue", "")
                    doc_id = doc["document"]["name"].split("/")[-1]
                    tasks.append({"title": title, "date": date, "time": time, "doc_id": doc_id})
            return tasks
        else:
            print("Fetch tasks failed:", response.content)
            return []
        
    def update_task(self, doc_id, completed, user_id, task_title=None, task_date=None, task_time=None):
        url = f"{self.base_url}/{self.collection}/{doc_id}"

        fields = {}
        if completed is not None:
            fields["completed"] = {"booleanValue": completed}
        if user_id is not None:
            fields["user_id"] = {"stringValue": user_id}
        if task_title is not None:
            fields["title"] = {"stringValue": task_title}
        if task_date is not None:
            fields["date"] = {"stringValue": task_date}
        if task_time is not None:
            fields["time"] = {"stringValue": task_time}

        if not fields:
            print("No updates provided.")
            return False

        data = {"fields": fields}
        response = requests.patch(url, json=data)

        if response.status_code == 200:
            print("task uipdated on database...")
            return True
        else:
            print("Edit task failed:", response.content)
            return False


    def delete_task(self, doc_id):
        url = f"{self.base_url}/{self.collection}/{doc_id}"
        response = requests.delete(url)
        return response.status_code == 200
