import json


class JsonDb:
    def __init__(self):
        self.db_path = "db.json"

    def get_db(self):
        content = open(self.db_path, encoding="utf-8").read()
        return json.loads(content)
