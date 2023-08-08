"""Functions for movie setup and production."""
from pymol import cmd

from typing import Any, Dict, List


class MovieMaker:
    """Create a PyMol movie from dictionaries.

    Attributes:
        _loaded_scenes: Stores total number of loaded scenes.
        _loaded_frames: Stores total number of loaded frames.
    """

    def __init__(self):
        """Initialize the instance."""
        self._loaded_scenes = []
        self._loaded_frames = 0

    @staticmethod
    def _clean_produce_dict(produce_dict: Dict[str, Any]):
        """Clean a setup dictionary.

        Checks for valid dict values. If not valid sets a default.

        Args:
            produce_dict: Nested dictionary containing setup information.
        """
        if not (filename := produce_dict.get("filename")) or not isinstance(
            filename, str
        ):
            print(
                'setup: filename has either not been specified or is not a string. A default filename of \
    "pymol_movie" will be used.'
            )
            produce_dict["filename"] = "pymol_movie"

        if not (mode := produce_dict.get("mode")) or mode not in (
            "normal",
            "fast",
            "ray",
        ):
            print(
                'setup: mode has either not been specified or is not one of 3 possible strings: \
    ("normal", "fast", "ray"). The default mode "normal" will be used.'
            )
            produce_dict["mode"] = "normal"

        if not (width := produce_dict.get("width")) or not width > 0:
            print(
                "setup; width has either not been specified or is not >0. A default width of 1264 will be used."
            )
            produce_dict["width"] = 1264

        if not (height := produce_dict.get("height")) or not height > 0:
            print(
                "setup; height has either not been specified or is not >0. A default height of 720 will be used."
            )
            produce_dict["height"] = 720

        if not produce_dict.get("framerate"):
            print(
                "setup: frame rate has either not been specified or... A default frame rate of 30 will be used."
            )
            produce_dict["framerate"] = 30

        if (
            not (quality := produce_dict.get("quality"))
            or not quality >= 0
            or not quality <= 100
        ):
            print(
                "setup: quality has either not been specified or is not within the bounds of 0-100. A default quality of \
    50 will be used."
            )
            produce_dict["quality"] = 50
        if not produce_dict.get("produce"):
            produce_dict["produce"] = "pse"

    def produce_movie(self, produce_dict: Dict[str, Any]) -> None:
        """Save PyMol movie.

        Args:
            produce_dict: Nested dictionary containing produce movie information.
        """
        cmd.mset(f'1x{produce_dict["frames"]}')

        cmd.set("movie_loop", 0)

        for (scene, frame, name, state) in self._loaded_scenes:
            cmd.mview("store", frame, scene=scene, object=name, state=state)

        if (produce := produce_dict.get("produce")) and produce == "mpg":
            self._clean_produce_dict(produce_dict)
            cmd.movie.produce(
                f'{produce_dict["filename"]}.mpg',
                preserve=0,
                encoder="ffmpeg",
                quality=produce_dict["quality"],
                width=produce_dict["width"],
                height=produce_dict["height"],
            )
        else:
            cmd.save(f'{produce_dict["filename"]}.pse')

    def setup_scene(self, scene_dict: Dict[str, Any]) -> None:
        """Set PyMol movie scene.

        Create new scene. Setup camera and object actions.

        Args:
            scene_dict: Nested dictionary containing scene information.
        """
        cmd.scene(key=str(scene_dict["scene"]), action="store")

        # Setup objects
        for object_dict in scene_dict["objects"]:

            if actions := object_dict.get("actions"):
                self._setup_model(object_dict["name"], actions)

            self._loaded_scenes.append(
                (
                    str(scene_dict["scene"]),
                    scene_dict["frame"],
                    object_dict["name"],
                    object_dict["state"],
                )
            )

        # Setup camera
        if camera_dict := scene_dict.get("camera"):
            self._setup_camera(camera_dict)

        self._loaded_scenes.append(
            (str(scene_dict["scene"]), scene_dict["frame"], "", 0)
        )

    def _setup_camera(self, camera_dicts: List[dict]) -> None:
        """Set camera actions for movie scene.

        Args:
            camera_dicts: A list of dictionaries containing camera action information.
        """
        for camera_action in camera_dicts:
            choice = list(camera_action.keys())[0]
            details = list(camera_action.values())[0]

            # Camera actions
            if choice == "turn":
                cmd.turn(details["axis"], details["angle"])
            elif choice == "move":
                cmd.move(details["axis"], details["magnitude"])
            elif choice == "zoom":
                cmd.zoom(details["selection"], animate=-1)
            elif choice == "orient":
                cmd.orient(details["selection"])

    def _setup_model(self, name: str, action_dicts: List[dict]) -> None:
        """Set model actions for movie scene.

        Args:
            name: Name of the model to perform actions.
            action_dicts: A list of dictionaries containing camera action information.
        """
        for action in action_dicts:
            choice = list(action.keys())[0]
            details = list(action.values())[0]

            # Basic model actions
            if choice == "color":
                cmd.color(details["color"], f'{name} and {details["selection"]}')
            elif choice == "representation":
                cmd.show_as(
                    details["representation"], f'{name} and {details["selection"]}'
                )
            elif choice == "rotate":
                cmd.rotate(
                    details["axis"],
                    details["angle"],
                    f'{name} and {details["selection"]}',
                )
            elif choice == "translate":
                cmd.translate(details["vector"], f'{name} and {details["selection"]}')

            # Presets
            elif choice == "surface_sticks":
                cmd.hide(selection=f"{name}")
                cmd.show("surface", f'{name} and {details["selection"]}')
                cmd.show("sticks", f'{name} and {details["selection"]}')
                cmd.set("transparency", 0.5, f'{name} and {details["selection"]}')
