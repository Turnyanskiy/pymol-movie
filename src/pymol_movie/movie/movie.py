from typing import Union
from pymol import cmd

from .loaders import ObjectLoader

def produce_movie(setup_dict: dict[str, Union[str, float]]) -> None:
    if not (filename := setup_dict.get('filename')) or not isinstance(filename, str):
        print('setup: filename has either not been specified or is not a string. A default filename of \
"pymol_movie.pse" will be used.')
        filename = 'pymol_movie.pse'

    if not (mode := setup_dict.get('mode')) or mode not in ('normal', 'fast', 'ray'):
        print('setup: mode has either not been specified or is not one of 3 possible strings: \
("normal", "fast", "ray"). The default mode "normal" will be used.')
        mode = 'normal'

    # if not (width := setup_dict.get('width')) or not width > 0:
    #     print('setup; width has either not been specified or is not >0. A default width of 1264 will be used.')
    #     width = 1264

    # if not (height := setup_dict.get('height')) or not height > 0L
    #     print('setup; height has either not been specified or is not >0. A default height of 720 will be used.')
    #     height = 720

    # if not (framerate := setup_dict.get('framerate')):
    #     print('setup: frame rate has either not been specified or... A default framerate of 30 will be used.')
    #     framerate = 30

    if not (quality := setup_dict.get('quality')) or not quality >= 0 or not quality <= 100:
        print('setup: quality has either not been specified or is not within the bounds of 0-100. A default quality of \
50 will be used.')
        quality = 50

    cmd.save('issac.pse')

    cmd.movie.produce(filename, mode, quality=quality)


def setup_scene(scene_dict: dict, object_loader: ObjectLoader) -> None:
    """"""
    # scene_dict = clean_scene_dict(scene_dict)

    cmd.scene(key=str(scene_dict.get('scene')), action='store')
    cmd.madd(f'1x{scene_dict.get("frames")}')

    scene_total_states = scene_dict.get('frames') // scene_dict.get('frames_per_state')

    object_loader.load_states(scene_total_states)

    cmd.mview('store', state=1, object='mov')
    cmd.mview('store', scene_dict.get('frames') // 2, state=cmd.count_states(), object='mov')
    for action in scene_dict.get('actions'):
        choice = list(action.keys())[0]
        details = list(action.values())[0]

        if choice == 'move':
            cmd.mdo(details.get('frame'), f'move {details.get("axis")}, {details.get("distance")}')
        elif choice == 'zoom':
            cmd.mdo(details.get('frame'), f'zoom {details.get("selection")}, animate={details.get("time")}')
        elif choice == 'set_view':
            cmd.mdo(details.get('frame'), f'set_view {details.get("view_matrix")}')
        elif choice == 'pause':
            cmd.madd(f'{details.get("state")}x{details.get("frames")}')
