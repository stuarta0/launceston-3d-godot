# City of Launceston Godot Project

![Skyline in Godot](https://raw.githubusercontent.com/stuarta0/launceston-3d/main/docs/skyline.jpg)

A Godot 3.2.2 project to view the City of Launceston 3D scan dataset in real time using LOD.

The dataset contains 142 tiles; each having dimensions of 200m x 200m.

## Getting Started

This repo contains the skeleton Godot project to view the City of Launceston 3D dataset. Once cloned, use 

```python3 scripts/import_dataset.py```

This will clone the asset repo into a `dataset` folder within this project (***warning: the asset repo is almost 6 GB***). After that, it'll generate Godot scene files to position the tiles in the correct layout.

The LOD scenes use the LOD addon by Hugo Locurcio: https://github.com/godot-extended-libraries/godot-lod

> If you don't want to create scenes using the LOD addon, simply change `USE_LOD = False` at the start of `scripts\import_dataset.py` **before** importing the dataset.

Scene structure:

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

The asset repo can be found here: https://github.com/stuarta0/launceston-3d

## License

MIT