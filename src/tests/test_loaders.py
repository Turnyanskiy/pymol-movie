"""Test Loaders."""
import pytest

from pymol_movie.movie.loaders import ObjectLoader, load_trajectory


def test_load_trajectory(capsys: pytest.CaptureFixture) -> None:
    load_trajectory("./tests/samples/object_trajs/example_object_1", "test_load_trajectory")
    out, _ = capsys.readouterr()
    assert out == "loaded 245 files\n"


def test_object_loader_load_states() -> None:
    object_loader = ObjectLoader(
        "./tests/samples/object_trajs/example_object_1", "test_object_loader_load_states"
    )
    object_loader.load_states(100)
    assert object_loader.loaded_states == 100


def test_object_loader_load_up_to_state() -> None:
    object_loader = ObjectLoader(
        "./tests/samples/object_trajs/example_object_1", "test_object_loader_load_up_to_state"
    )
    object_loader.load_up_to_state(10)
    object_loader.load_up_to_state(50)
    assert object_loader.loaded_states == 50
