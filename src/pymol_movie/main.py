from pymol import cmd

from .cli import parsers
from .movie import movie, loaders


def main() -> None:
    args = parsers.parse_args()

    object_loader = loaders.ObjectLoader(args.directory)
    yaml_dict = parsers.parse_yaml(args.yaml_filepath)

    print(yaml_dict)

    for scene in yaml_dict.get('scenes'):
        movie.setup_scene(scene, object_loader)

    movie.produce_movie(yaml_dict.get('setup'))


if __name__ == '__main__':
    main()
