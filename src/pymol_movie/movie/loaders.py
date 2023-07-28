from pymol import cmd
from pathlib import Path
import os


def load_trajectory(directory) -> None:
    """Load all pdb files in specified directory.

    Args:
        directory: String with filepath to directory
    """
    p = Path(directory)
    files = sorted(p.glob('*.pdb'), key=lambda x: int(os.path.splitext(x)[0].split('_')[-1]))
    for file in files: cmd.load(file, 'mov')

    print(f'loaded {cmd.count_states()} files')


class ObjectLoader:

    def __init__(self, directory: str):
        self.files = sorted(Path(directory).glob('*.pdb'), key=lambda x: int(os.path.splitext(x)[0].split('_')[-1]))
        self.current_state = 0

    def load_states(self, states):
        for i in range(states):
            self.current_state += 1
            cmd.load(self.files[self.current_state], 'mov')
