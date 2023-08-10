"""Test moviemaker."""
import pytest

from pymol_movie.movie.loaders import ObjectLoader
from pymol_movie.movie.movie import MovieMaker


class TestMovieMaker:
    movie_maker = MovieMaker()
    ObjectLoader("./tests/samples/object_trajs/example_object_1", "luke").load_up_to_state(200)
    ObjectLoader("./tests/samples/object_trajs/example_object_2", "isaac").load_up_to_state(190)

    @pytest.mark.parametrize(
        ("scene_dict", "expected_out"),
        [
            (
                {
                    "scene": 1,
                    "frame": 1,
                    "objects": [
                        {
                            "name": "luke",
                            "state": 1,
                            "actions": [
                                {
                                    "representation": {
                                        "selection": "chain B",
                                        "representation": "cartoon",
                                    }
                                },
                                {"color": {"selection": "chain A", "color": "red"}},
                            ],
                        },
                        {
                            "name": "isaac",
                            "state": 1,
                            "actions": [
                                {"reentation": {"selection": "all", "representation": "sticks"}}
                            ],
                        },
                    ],
                    "camera": [{"turn": {"axis": "y", "angle": 90}}],
                },
                'The choice "reentation" is not recognized.\n',
            ),
            (
                {
                    "scene": 2,
                    "frame": 51,
                    "objects": [
                        {
                            "name": "luke",
                            "state": 101,
                            "actions": [
                                {
                                    "representation": {
                                        "selection": "chain C",
                                        "representation": "sticks",
                                    }
                                },
                                {"color": {"selection": "chain C", "color": "pink"}},
                            ],
                        },
                        {
                            "name": "isaac",
                            "state": 150,
                            "actions": [
                                {
                                    "representation": {
                                        "selection": "all",
                                        "representation": "cartoon",
                                    }
                                }
                            ],
                        },
                    ],
                    "camera": [{"orient": {"selection": "Chain A"}}],
                },
                "",
            ),
            (
                {
                    "scene": 3,
                    "frame": 101,
                    "objects": [
                        {
                            "name": "luke",
                            "state": 50,
                            "actions": [
                                {
                                    "representation": {
                                        "selection": "all",
                                        "representation": "cartoon",
                                    }
                                },
                                {"color": {"selection": "chain C", "color": "green"}},
                            ],
                        },
                        {
                            "name": "isaac",
                            "state": 75,
                            "actions": [
                                {
                                    "representation": {
                                        "selection": "chain c",
                                        "representation": "sticks",
                                    }
                                },
                                {"translate": {"selection": "chain A", "vector": [0, 10, 0]}},
                            ],
                        },
                    ],
                    "camera": [
                        {"turn": {"axis": "y", "angle": 90}},
                        {"mve": {"axis": "x", "magnitude": 50}},
                    ],
                },
                'The choice "mve" is not recognized.\n',
            ),
        ],
    )
    def test_setup_scene(
        self, scene_dict: dict, expected_out: str, capsys: pytest.CaptureFixture
    ) -> None:
        TestMovieMaker.movie_maker.setup_scene(scene_dict)
        out, _ = capsys.readouterr()
        assert out == expected_out

    # def test_produce_movie(self, produce_dict):
    #    TestMovieMaker.movie_maker.produce_scene(produce_dict)
