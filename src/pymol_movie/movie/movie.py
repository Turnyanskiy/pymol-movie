"""Functions for movie setup and production."""
from pymol import cmd

from .loaders import ObjectLoader

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
    def _clean_setup_dict(setup_dict: Dict[str, Any]):
        """Clean a setup dictionary.

        Checks for valid dict values. If not valid sets a default.

        Args:
            setup_dict: Nested dictionary containing setup information.
        """
        if not (filename := setup_dict.get("filename")) or not isinstance(
            filename, str
        ):
            print(
                'setup: filename has either not been specified or is not a string. A default filename of \
    "pymol_movie" will be used.'
            )
            setup_dict["filename"] = "pymol_movie"

        if not (mode := setup_dict.get("mode")) or mode not in (
            "normal",
            "fast",
            "ray",
        ):
            print(
                'setup: mode has either not been specified or is not one of 3 possible strings: \
    ("normal", "fast", "ray"). The default mode "normal" will be used.'
            )
            setup_dict["mode"] = "normal"

        if not (width := setup_dict.get("width")) or not width > 0:
            print(
                "setup; width has either not been specified or is not >0. A default width of 1264 will be used."
            )
            setup_dict["width"] = 1264

        if not (height := setup_dict.get("height")) or not height > 0:
            print(
                "setup; height has either not been specified or is not >0. A default height of 720 will be used."
            )
            setup_dict["height"] = 720

        if not setup_dict.get("framerate"):
            print(
                "setup: frame rate has either not been specified or... A default frame rate of 30 will be used."
            )
            setup_dict["framerate"] = 30

        if (
            not (quality := setup_dict.get("quality"))
            or not quality >= 0
            or not quality <= 100
        ):
            print(
                "setup: quality has either not been specified or is not within the bounds of 0-100. A default quality of \
    50 will be used."
            )
            setup_dict["quality"] = 50
        if not setup_dict.get("produce"):
            setup_dict["produce"] = "pse"

    def produce_movie(self, setup_dict: Dict[str, Any]) -> None:
        """Save PyMol movie.

        Args:
            setup_dict: Nested dictionary containing setup information.
        """
        self._clean_setup_dict(setup_dict)

        cmd.mset(f'1x{setup_dict["frames"]}')

        cmd.set("movie_loop", 0)

        for (scene, frame, state) in self._loaded_scenes:
            cmd.mview("store", frame, scene=scene, state=state)

        if setup_dict["produce"] == "mpg":
            cmd.movie.produce(
                f'{setup_dict["filename"]}.mpg',
                preserve=0,
                encoder="ffmpeg",
                quality=setup_dict["quality"],
                width=setup_dict["width"],
                height=setup_dict["height"],
            )
        else:
            cmd.save(f'{setup_dict["filename"]}.pse')

    def setup_scene(
        self, scene_dict: Dict[str, Any], object_loader: ObjectLoader
    ) -> None:
        """Set PyMol movie scene.

        Create new scene and add needed frames. Perform actions.

        Args:
            scene_dict: Nested dictionary containing scene information.
            object_loader: ObjectLoader object for the object in scene.
        """
        object_loader.load_up_to_state(scene_dict["state"])

        cmd.scene(key=str(scene_dict["scene"]), action="store")
        cmd.show_as(scene_dict["representation"], "all")

        if action_dict := scene_dict.get("actions"):
            self._setup_actions(action_dict)

        self._loaded_scenes.append(
            (str(scene_dict["scene"]), scene_dict["frame"], scene_dict["state"])
        )

    def _setup_actions(self, action_dicts: List[dict]) -> None:
        """Set actions for movie scene.

        Args:
            action_dicts: A list of dictionaries containing action information.
        """
        for action in action_dicts:
            choice = list(action.keys())[0]
            details = list(action.values())[0]

            # Camera actions
            if choice == "rotate":
                cmd.turn(details["axis"], details["angle"])
            elif choice == "move":
                cmd.move(details["axis"], details["magnitude"])
            elif choice == "zoom":
                cmd.zoom(details["selection"], animate=-1)
            elif choice == "orient":
                cmd.orient(details["selection"])

            elif choice == "color":
                cmd.color(details["color"], details["selection"])
