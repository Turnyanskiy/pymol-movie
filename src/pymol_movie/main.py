"""Program entry point."""
from .cli import parsers
from .movie import movie, loaders
from typing import cast


def main() -> None:
    """Entry Function."""
    args = parsers.parse_args()

    object_loader = loaders.ObjectLoader(args.directory, "mov")
    yaml_dict: dict = cast(dict, parsers.parse_yaml(args.yaml_filepath))

    print(yaml_dict)

    for scene in yaml_dict["scenes"]:
        movie.setup_scene(scene, object_loader)
    movie.produce_movie(yaml_dict["setup"])


if __name__ == "__main__":
    main()
