import requests
import json

PROJECT_ID = "teamf-ae838"
BASE_URL = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents"
COLLECTION = "todos"

class FirestoreAPI:
    def __init__(self, project_id, collection):
        self.base_url = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/(default)/documents"
        self.collection = collection 

    def add_task(self, task_title):
        url = f"{self.base_url}/{self.collection}"
        data = {
            "fields": {
                "title": {"stringValue": task_title},
                "completed": {"booleanValue": False}
            }
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return True
        else:
            print("Add task failed:", response.content)
            return False

    def get_tasks(self):
        url = f"{self.base_url}/{self.collection}"
        response = requests.get(url)
        if response.status_code == 200:
            tasks = []
            for task in response.json().get("documents", []):
                fields = task["fields"]
                title = fields["title"]["stringValue"]
                doc_id = task["name"].split("/")[-1]
                tasks.append({"title": title, "doc_id": doc_id})
            return tasks
        else:
            print("Fetch tasks failed:", response.content)
            return []

    def delete_task(self, doc_id):
        url = f"{self.base_url}/{self.collection}/{doc_id}"
        response = requests.delete(url)
        return response.status_code == 200
