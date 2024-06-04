import json


class Scene:
    def __init__(self, app, scene_path):
        with open(scene_path, "r") as f:
            str_data = f.read()
            json_data = json.loads(str_data)

        self.objects = json_data["objects"]
        self.app = app
        self.sceneID = -1

