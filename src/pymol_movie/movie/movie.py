"""Functions for movie setup and production."""
from typing import Union
from pymol import cmd

from .loaders import ObjectLoader

from typing import Any
from typing import Dict


def produce_movie(setup_dict: Dict[str, Any]) -> None:
    """Produce PyMol movie.

    Check for valid dict values. If not valid set default. Saves the movie.

    Args:
        setup_dict: Nested dictionary containing setup information.
    """
    if not (filename := setup_dict.get("filename")) or not isinstance(filename, str):
        print(
            'setup: filename has either not been specified or is not a string. A default filename of \
"pymol_movie.pse" will be used.'
        )
        filename = "pymol_movie.pse"

    if not (mode := setup_dict.get("mode")) or mode not in ("normal", "fast", "ray"):
        print(
            'setup: mode has either not been specified or is not one of 3 possible strings: \
("normal", "fast", "ray"). The default mode "normal" will be used.'
        )
        mode = "normal"

    if not (width := setup_dict.get("width")) or not width > 0:
        print(
            "setup; width has either not been specified or is not >0. A default width of 1264 will be used."
        )
        width = 1264

    if not (height := setup_dict.get("height")) or not height > 0:
        print(
            "setup; height has either not been specified or is not >0. A default height of 720 will be used."
        )
        height = 720

    # if not (framerate := setup_dict.get('framerate')):
    #     print('setup: frame rate has either not been specified or... A default framerate of 30 will be used.')
    #     framerate = 30

    if (
        not (quality := setup_dict.get("quality"))
        or not quality >= 0
        or not quality <= 100
    ):
        print(
            "setup: quality has either not been specified or is not within the bounds of 0-100. A default quality of \
50 will be used."
        )
        quality = 50

    cmd.save(f"{filename}.pse")

    # cmd.movie.produce(f'{filename}.mpg', mode, 1, 200, 0, 'convert', quality=quality, width=width, height=height)


def setup_scene(scene_dict: Dict[str, Any], object_loader: ObjectLoader) -> None:
    """Set PyMol movie scene.

    Create new scene and add needed frames. Perform actions.

    Args:
        scene_dict: Nested dictionary containing scene information.
        object_loader: ObjectLoader object for the object in scene.
    """
    # scene_dict = clean_scene_dict(scene_dict)

    cmd.scene(key=str(scene_dict["scene"]), action="store")
    cmd.madd(f'1x{scene_dict["frames"]}')

    scene_total_states = scene_dict["frames"] // scene_dict["frames_per_state"]

    object_loader.load_states(scene_total_states)

    cmd.mview("store", state=1, object=f"{object_loader.name}")
    cmd.mview(
        "store",
        scene_dict["frames"] // 2,
        state=cmd.count_states(),
        object=f"{object_loader.name}",
    )

    for action in scene_dict["actions"]:
        choice = list(action.keys())[0]
        details = list(action.values())[0]

        if choice == "move":
            cmd.mdo(
                details["frame"],
                f'move {details["axis"]}, {details["distance"]}',
            )
        elif choice == "zoom":
            cmd.mdo(
                details.get("frame"),
                f'zoom {details["selection"]}, animate={details["time"]}',
            )
        elif choice == "set_view":
            cmd.mdo(details["frame"], f'set_view {details["view_matrix"]}')
        # elif choice == 'pause':
        #    cmd.madd(f'{details.get("state")}x{details.get("frames")}')
        elif choice == "roll":
            cmd.movie.roll(
                details["frame"],
                details["end"],
                details["loop"],
                details["axis"],
            )
        elif choice == "rock":
            cmd.movie.rock(
                details["frame"],
                details["end"],
                details["angle"],
                details["phase"],
                details["loop"],
                details["axis"],
            )
