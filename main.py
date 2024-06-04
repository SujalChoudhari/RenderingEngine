from src.app.app import Application


def main():
    objects = {
        "line": {"type": "line", "origin": (-5, 2, 0), "destination": (-3, 1,0)},
        "cube": {"type": "cube", "position": (0, 0, 0), "size": (1, 1, 1)},
        "light": {
            "type": "light",
            "position": (-10, 10, 10),
            "ambient": (.4, .4, .3),
            "diffuse": (1, 1, 1),
            "specular": (0.1, 0.1, 0.1),
        },
        "sphere": {
            "type": "sphere",
            "position": (0, 5, -1),
            "radius": 1,
            "slices": 15,
            "stacks": 15,
        },
        "cylinder": {
            "type": "cylinder",
            "position": (-10, 5, -1),
            "radius": 1,
            "height": 5,
            "sides": 15,
        }

    }
    app = Application(width=1000, height=800, title="Rendering Engine")
    app.initialize_objects(objects)
    app.run()


if __name__ == "__main__":
    main()
