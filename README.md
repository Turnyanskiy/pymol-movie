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

---

### setup
|           |                                |
| --------- | ------------------------------ |
| `objects` | A list of pymol objects        |

A sample setup:
```
setup:
  objects:
  - ...
```
#### setup:objects
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

---

### scenes
|           |                                                                                                                                      |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `scene`   | Scene name. (The example uses a number but this is not required. Scenes are loaded and linked in the order they appear in the .yaml) |
| `frame`   | Starting frame for the scene.                                                                                                        |
| `objects` | List of objets in the scene configuration.                                                                                           |
| `camera`  | Camera movement configuration.                                                                                                       |


A sample scene:
```
scenes:
  - scene: 1
    frame: 1
    objects:
    -  ...
    camera:
    -  ...
```

#### scenes:objects
|             |                                                                                                           |
| ----------- | --------------------------------------------------------------------------------------------------------- |
| `name`      | Pymol editor name for object.                                                                             |
| `states`    | State of object in this scene.                                                                            |
| `actions`   | List of actions to perform on object in this scene                                                        |

A sample object:
```
scenes:
  - scene: 1
    frame: 1
    objects:
    - name: isaac
      state: 1
      actions:
      -  ... 
    camera:
    -  ...
```

#### scenes:objects:actions
|                  |                                                                                                                             |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------- |
| `translate`      | `selection` selection of the object, `vector`  vector to translate. Written in the form `[0,0,0]`                           |
| `rotate`         | `selection` selection of the object, `axis`  axis to perform roration, `angle` rotation in degrees, maximum rotation of 180 |
| `representation` | `selection` selection of the object, `representation` the representation                                                    |
| `color`          | `selection` selection of the object, `color` the color                                                                      |

A sample action:
```
scenes:
  - scene: 1
    frame: 1
    objects:
      - name: isaac
        state: 1
        actions:
          - translate:
              selection: chain A
              vector: [1, 0, 0]
          - rotate;
              selection: chain C
              axis: x
              angle: 90
          - representation:
              selection: all
              representation: cartoon
          - color:
              selection: all
              color: red
    camera:
      - ...
```

### scenes:camera 
|                |                                                                            |
| ------------- | --------------------------------------------------------------------------- |
| `move`        | `axis` axis to perform movement, `magnitude` float of magnitude of movement |
| `turn`        | `axis` axis to perform rotation, `angle` rotation in degrees                |
| `zoom`        | `selection` zoom selection                                                  |
| `orient`      | `selection` orient selection                                                |


A sample camera:
```
scenes:
  - scene: 1
    frame: 1
    objects:
      - name: isaac
        state: 1
        actions:
          - ...
    camera:
      - move:
          axis: x
          magnitude: 1
      - turn:
          axis: y
          angle: 90
      - zoom:
          selection: isaac and chain A
      - orient:
          selection: all
```




