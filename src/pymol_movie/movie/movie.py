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
        self._loaded_scenes = 0
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
    "pymol_movie.pse" will be used.'
            )
            setup_dict["filename"] = "pymol_movie.pse"

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
                "setup: frame rate has either not been specified or... A default framerate of 30 will be used."
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

    def produce_movie(self, setup_dict: Dict[str, Any]) -> None:
        """Save PyMol movie.

        Args:
            setup_dict: Nested dictionary containing setup information.
        """
        self._clean_setup_dict(setup_dict)

        cmd.set("movie_fps", setup_dict["framerate"])
        cmd.set("scene_loop")
        cmd.mdo(1, "scene auto, next")
        cmd.rewind()
        cmd.save(f'{setup_dict["filename"]}.pse')

        # cmd.movie.produce(f'{filename}.mpg', mode, 1, 200, 0, 'convert', quality=quality, width=width, height=height)

    def setup_scene(self, scene_dict: Dict[str, Any], object_loader: ObjectLoader):
        """Set PyMol movie scene.

        Create new scene and add needed frames. Perform actions.

        Args:
            scene_dict: Nested dictionary containing scene information.
            object_loader: ObjectLoader object for the object in scene.
        """
        # scene_dict = clean_scene_dict(scene_dict)

        cmd.scene(key=f"{self._loaded_scenes + 1}", action="store")
        cmd.madd(f'1x{scene_dict["frames"]}')

        scene_total_states = scene_dict["frames"] // scene_dict["frames_per_state"]

        cmd.mview(
            "store",
            first=self._loaded_frames + 1,
            state=object_loader.loaded_states,
            object=f"{object_loader.name}",
        )
        object_loader.load_states(scene_total_states)
        cmd.mview(
            "store",
            scene_dict["frames"] // 2,
            state=cmd.count_states(),
            object=f"{object_loader.name}",
        )

        self._setup_actions(scene_dict["actions"])

        cmd.mdo(
            self._loaded_frames,
            f"mdo {self._loaded_frames + 1}: scene {self._loaded_scenes + 1}",
        )

        self._loaded_frames += scene_dict["frames"]
        self._loaded_scenes += 1

    def _setup_actions(self, action_dicts: List[dict]):
        """Set actions for movie scene.

        Args:
            action_dicts: A list of dictionaries containing action information.
        """
        for action in action_dicts:
            choice = list(action.keys())[0]
            details = list(action.values())[0]

            if choice == "move":
                cmd.mdo(
                    self._loaded_frames + details["frame"],
                    f'move {details["axis"]}, {details["distance"]}',
                )
            elif choice == "zoom":
                cmd.mdo(
                    self._loaded_frames + details.get("frame"),
                    f'zoom {details["selection"]}, animate={details["time"]}',
                )
            elif choice == "set_view":
                cmd.mdo(
                    self._loaded_frames + details["frame"],
                    f'set_view {details["view_matrix"]}',
                )
            # elif choice == 'pause':
            #    cmd.madd(f'{details.get("state")}x{details.get("frames")}')
            elif choice == "roll":
                cmd.movie.roll(
                    self._loaded_frames + details["frame"],
                    details["end"],
                    details["loop"],
                    details["axis"],
                )
            elif choice == "rock":
                cmd.movie.rock(
                    self._loaded_frames + details["frame"],
                    details["end"],
                    details["angle"],
                    details["phase"],
                    details["loop"],
                    details["axis"],
                )
