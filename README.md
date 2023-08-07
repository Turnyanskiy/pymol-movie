# `pymol-movie`

## Usage
```
cd src
python3 __main__.py [<path_to_yaml>]
```

## Creating Config .yaml
To create a movie a .yaml configuration file is used. The file describes the objects, produce setings and individual scenes of the pymol movie.

### Top level
|           |                                |
| --------- | ------------------------------ |
| `setup`   | Movie setup configuration      |
| `scenes`  | A list of scenes               |
| `produce` | Movie production configuration |

### Setup
|           |                                |
| --------- | ------------------------------ |
| `objects` | A list of pymol objects        |

A sample setup:
```
setup:
  objects:
  - ...
```
#### Objects
|             |                                                                                                           |
| ----------- | --------------------------------------------------------------------------------------------------------- |
| `name`      | Pymol editor name for object. This name is also used to refer to this object in the .yaml configuration.  |
| `directory` | Filepath to directory containing all states of the object. Recommended to use absolute file path as relative filepath depends on the working direction of the script rather than location of the .yaml. To order the states files must be labeled by number 1,2,3...                                       |
| `states`    | The number of states to load from the object directory.                                                   |

A sample object:
```
setup:
  objects:
  - name: isaac
    directory: ./example_trajectories/simple_translate
    states: 200 
```

### Scenes
|           |                                                                                                                                      |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `scene`   | Scene name. (The example uses a number but this is not required. Scenes are loaded and linked in the order they appear in the .yaml) |
| `frame`   | Starting frame for the scene.                                                                                                        |
| `objects` | List of objets in the scene configuration.                                                                                           |
| `camera`  | Camera movement configuration.                                                                                                       |


A sample scene:
```

```



