"""PDB trajectory loader class/function."""
from pymol import cmd
from pathlib import Path
import os


def load_trajectory(directory) -> None:
    """Load all pdb files in specified directory.

    Args:
        directory: String with filepath to directory
    """
    p = Path(directory)
    files = sorted(
        p.glob("*.pdb"), key=lambda x: int(os.path.splitext(x)[0].split("_")[-1])
    )
    for file in files:
        cmd.load(file, "mov")

    print(f"loaded {cmd.count_states()} files")


class ObjectLoader:
    """Load Object trajectory from pdb files.

    Attributes:
        _files: Sorted iterable of trajectory pdb files.
        _current_state: The previous loaded trajectory state.
        name: Name of loaded object.
    """

    def __init__(self, directory: str, name: str):
        """Initialize the instance based and globs pdb trajectory files from directory.

        Args:
            directory: Filepath to directory containing pdb trajectory files.
            name: Name of loaded object.
        """
        self._files = sorted(
            Path(directory).glob("*.pdb"),
            key=lambda x: int(os.path.splitext(x)[0].split("_")[-1]),
        )
        self._current_state = 0
        self.name = name

    def load_states(self, states):
        """Load number of states specified.

        Args:
            states: The number of states to load.
        """
        for i in range(states):
            self._current_state += 1
            cmd.load(self._files[self._current_state], self.name)
