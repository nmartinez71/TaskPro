import requests
import json

PROJECT_ID = "teamf-ae838"

class FirestoreAPI:
    def __init__(self, project_id, collection):
        self.base_url = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/(default)/documents"
        self.collection = collection 

    def add_task(self, task_title, task_date="", task_time=""):
        url = f"{self.base_url}/{self.collection}"
        data = {
            "fields": {
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
        
    def update_task(self, doc_id, task_title=None, task_date=None, task_time=None):
        url = f"{self.base_url}/{self.collection}/{doc_id}"

        fields = {}
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

    def get_tasks(self):
        url = f"{self.base_url}/{self.collection}"
        response = requests.get(url)
        if response.status_code == 200:
            tasks = []
            for task in response.json().get("documents", []):
                fields = task["fields"]
                title = fields["title"]["stringValue"]
                date = fields.get("date", {}).get("stringValue", "")
                time = fields.get("time", {}).get("stringValue", "")
                doc_id = task["name"].split("/")[-1]
                tasks.append({"title": title, "date": date, "time": time, "doc_id": doc_id})
            return tasks
        else:
            print("Fetch tasks failed:", response.content)
            return []


    def delete_task(self, doc_id):
        url = f"{self.base_url}/{self.collection}/{doc_id}"
        response = requests.delete(url)
        return response.status_code == 200
