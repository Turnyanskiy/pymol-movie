"""Program entry point."""
import sys
from typing import cast

from .cli import parsers
from .movie import loaders, movie


def main() -> None:
    """Entry Function."""
    args = parsers.parse_args(sys.argv[1:])

    yaml_dict: dict = cast(dict, parsers.parse_yaml(args.yaml_filepath))

    print(yaml_dict)

    # Loads all objects
    for pymol_object in yaml_dict["setup"]["objects"]:
        loaders.ObjectLoader(
            pymol_object["directory"], pymol_object["name"]
        ).load_up_to_state(pymol_object["states"])

    # Creates scenes
    movie_maker = movie.MovieMaker()
    for scene in yaml_dict["scenes"]:
        movie_maker.setup_scene(scene)

    # Produce movie
    movie_maker.produce_movie(yaml_dict["produce"])


if __name__ == "__main__":
    main()
