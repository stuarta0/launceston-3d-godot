# City of Launceston Godot Project

![Skyline in Godot](https://raw.githubusercontent.com/stuarta0/launceston-3d/main/docs/skyline.jpg)

A Godot 3.2.2 project to view the City of Launceston 3D scan dataset in real time using LOD.

This repository only contains the skeleton Godot project. The 3D tile assets can be found in the following repo (see *Getting Started* below for details): https://github.com/stuarta0/launceston-3d

The asset repo contains 142 tiles over 6 LOD levels, with each tile having dimensions of 200m x 200m. ***Warning: the asset repo is almost 5.8 GB***

## Getting Started

Once this repo is cloned, use the following command to fetch the 3D tile asset repo and create the Godot scenes: 

```python3 scripts/import_dataset.py```

This will clone the asset repo into a `dataset` folder within this project. After that, it'll generate Godot scene files to position the tiles in the correct layout.

This project uses the LOD addon by Hugo Locurcio: https://github.com/godot-extended-libraries/godot-lod

> If you don't want to create scenes using the LOD addon, simply change `USE_LOD = False` at the start of `scripts\import_dataset.py` **before** importing the dataset.

### Scene structure after import with LOD

* `dataset/`
  * `Tile_XXX_YYY.tscn`
    * LOD Root Node
      * Tile_XXX_YYY_L20-lod0 (<400m)
      * Tile_XXX_YYY_L17-lod1 (<800m)
      * Tile_XXX_YYY_L15-lod2 (<3km)
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