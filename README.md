# City of Launceston Godot Project

A Godot 3.2 project to view the City of Launceston 3D scan dataset in real time using LOD.

![Skyline in Godot](https://raw.githubusercontent.com/stuarta0/launceston-3d/main/docs/skyline.jpg)

This repository only contains the skeleton Godot project. The 3D tile assets can be found in the following repo (see *Getting Started* below for details): https://github.com/stuarta0/launceston-3d

The asset repo contains 142 tiles over 6 LOD levels, with each tile having dimensions of 200m x 200m. ***Warning: the asset repo is ~5.8 GB***

## Getting Started

Once this repo is cloned, use the following command to fetch the 3D tile asset repo and create the Godot scenes: 

```python3 scripts/import_dataset.py```

This will clone the asset repo into a `dataset` folder within this project. After that, it'll generate Godot scene files to position the tiles in the correct layout.

This project uses both a custom LOD implementation and the LOD addon by Hugo Locurcio: https://github.com/godot-extended-libraries/godot-lod

It was found the addon implementation tanked performance as all the LOD meshes were loaded at runtime and only had their visiblity state changed. The custom implementation uses dynamic loading using `ResourceLoader.load_interactive()` (and subsequent `queue_free()`) to ensure only the required meshes remain in memory at any given time.

> If you want to disable LOD, simply change `USE_LOD = False` at the start of `scripts\import_dataset.py`. The import can be run multiple times as it'll only clone the asset repo once.

### Scene structure after import with custom LOD

* `dataset/`
  * `Tile_XXX_YYY.tscn`
    * LOD Root Node
      * placeholder (Tile_XXX_YYY_L15.gltf scene)
      * VisibilityEnabler (uses signals to unload tiles outside the camera view)
* `Master.tscn`
  * Root Node
    * Tiles
      * Tile_XXX_YYY Scene
      * ...

### Scene structure after import without LOD

* `dataset/`
  * `Tile_XXX_YYY.tscn`
    * Root Node
      * Tile_XXX_YYY_L20
* `Master.tscn`
  * Root Node
    * Tiles
      * Tile_XXX_YYY Scene
      * ...

## License

MIT