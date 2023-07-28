import argparse
from typing import Optional
import yaml


def parse_args() -> argparse.Namespace:
    """Parse args.

    Returns:
        A argparse namespace object.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('directory')
    parser.add_argument('yaml_filepath')

    return parser.parse_args()


def parse_yaml(yaml_filepath) -> Optional[dict]:
    with open(yaml_filepath) as yaml_file:
        return yaml.load(yaml_file, yaml.Loader)
