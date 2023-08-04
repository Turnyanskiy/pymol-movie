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
        loaded_states: The previous loaded trajectory state.
        name: Name of loaded object.
    """

    def __init__(self, directory: str, name: str) -> None:
        """Initialize the instance and globs pdb trajectory files from directory.

        Args:
            directory: Filepath to directory containing pdb trajectory files.
            name: Name of loaded object.
        """
        self._files = sorted(
            Path(directory).glob("*.pdb"),
            key=lambda x: int(os.path.splitext(x)[0].split("_")[-1]),
        )
        self.loaded_states = 0
        self.name = name

    def load_states(self, states: int) -> None:
        """Load number of states specified.

        Args:
            states: The number of states to load.
        """
        for _ in range(states):
            self.loaded_states += 1
            cmd.load(self._files[self.loaded_states], self.name)

    def load_up_to_state(self, state: int) -> None:
        """Load up to the state specified.

        Load up to the state specified. If state specified is lower than the state already loaded then function
        is ignored.

        Args:
            state: The state to load to. (Inclusive)
        """
        states_to_load = max(0, state - self.loaded_states)
        for _ in range(states_to_load):
            self.loaded_states += 1
            cmd.load(self._files[self.loaded_states], self.name)
