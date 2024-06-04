from src.app.app import Application
from src.scene import Scene

def main():
    app = Application(width=1000, height=800, title="Rendering Engine")
    
    scene = Scene(app, "./assets/scene1.mini")
    app.add_scene(scene)
    app.load_scene(scene.sceneID)
    app.run()


if __name__ == "__main__":
    main()
