"""Test parsers."""
import pytest

from pymol_movie.cli.parsers import parse_args, parse_yaml


@pytest.mark.parametrize(
    "filepath", ["./test/test/test", "./pymol/issac/luke" "./instadeep/internship"]
)
def test_parse_args(filepath: str) -> None:
    assert parse_args([filepath]).yaml_filepath == filepath


@pytest.mark.parametrize(
    ("filepath", "example_dict"),
    [
        (
            "./tests/samples/yamls/example_setup.yaml",
            {
                "setup": {
                    "objects": [
                        {"name": "luke", "directory": "./luke/test", "states": 200},
                        {"name": "isaac", "directory": "./isaac/test", "states": 190},
                    ]
                }
            },
        ),
        (
            "./tests/samples/yamls/example_produce.yaml",
            {
                "produce": {
                    "filename": "test",
                    "mode": "normal",
                    "width": 1920,
                    "height": 1080,
                    "framerate": 30,
                    "quality": 100,
                    "frames": 300,
                    "produce": "pse",
                }
            },
        ),
        (
            "./tests/samples/yamls/example_scenes.yaml",
            {
                "scenes": [
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
                                    {
                                        "representation": {
                                            "selection": "all",
                                            "representation": "sticks",
                                        }
                                    }
                                ],
                            },
                        ],
                        "camera": [{"turn": {"axis": "y", "angle": 90}}],
                    },
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
                                    {
                                        "color": {
                                            "selection": "chain C",
                                            "color": "pink",
                                        }
                                    },
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
                                    {
                                        "color": {
                                            "selection": "chain C",
                                            "color": "green",
                                        }
                                    },
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
                                    {
                                        "translate": {
                                            "selection": "chain A",
                                            "vector": [0, 10, 0],
                                        }
                                    },
                                ],
                            },
                        ],
                        "camera": [
                            {"turn": {"axis": "y", "angle": 90}},
                            {"move": {"axis": "x", "magnitude": 50}},
                        ],
                    },
                    {
                        "scene": 4,
                        "frame": 151,
                        "objects": [
                            {
                                "name": "luke",
                                "state": 20,
                                "actions": [
                                    {
                                        "representation": {
                                            "selection": "chain A",
                                            "representation": "sticks",
                                        }
                                    },
                                    {
                                        "rotate": {
                                            "axis": "x",
                                            "angle": 90,
                                            "selection": "all",
                                        }
                                    },
                                ],
                            },
                            {
                                "name": "isaac",
                                "state": 40,
                                "actions": [
                                    {
                                        "representation": {
                                            "selection": "all",
                                            "representation": "cartoon",
                                        }
                                    },
                                    {"color": {"selection": "all", "color": "yellow"}},
                                ],
                            },
                        ],
                        "camera": [
                            {"turn": {"axis": "x", "angle": 180}},
                            {"move": {"axis": "x", "magnitude": -10}},
                        ],
                    },
                    {
                        "scene": 5,
                        "frame": 200,
                        "objects": [
                            {
                                "name": "luke",
                                "state": 100,
                                "actions": [
                                    {
                                        "representation": {
                                            "selection": "all",
                                            "representation": "cartoon",
                                        }
                                    }
                                ],
                            },
                            {
                                "name": "isaac",
                                "state": 190,
                                "actions": [
                                    {
                                        "representation": {
                                            "selection": "chain A",
                                            "representation": "sticks",
                                        }
                                    }
                                ],
                            },
                        ],
                        "camera": [{"zoom": {"selection": "all"}}],
                    },
                    {
                        "scene": 6,
                        "frame": 250,
                        "objects": [
                            {
                                "name": "isaac",
                                "state": 100,
                                "actions": [
                                    {"surface_sticks": {"selection": "chain C"}}
                                ],
                            }
                        ],
                        "camera": [{"zoom": {"selection": "chain C"}}],
                    },
                    {
                        "scene": 7,
                        "frame": 300,
                        "objects": [
                            {
                                "name": "luke",
                                "state": 1,
                                "actions": [
                                    {
                                        "representation": {
                                            "selection": "all",
                                            "representation": "cartoon",
                                        }
                                    }
                                ],
                            },
                            {
                                "name": "isaac",
                                "state": 1,
                                "actions": [
                                    {
                                        "representation": {
                                            "selection": "all",
                                            "representation": "sticks",
                                        }
                                    }
                                ],
                            },
                        ],
                    },
                ]
            },
        ),
    ],
)
def test_parse_yaml(filepath: str, example_dict: dict) -> None:
    assert parse_yaml(filepath) == example_dict
