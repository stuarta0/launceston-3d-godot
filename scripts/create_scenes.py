import os
import re
from collections import OrderedDict

project = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

class ExternalResource:
    def __init__(self, path, type, id):
        self.path = path
        self.type = type
        self.id = id
    
    def __str__(self):
        return f'[ext_resource path="{self.path}" type="{self.type}" id={self.id}]'


class ExternalScript(ExternalResource):
    def __init__(self, path, id):
        super().__init__(path, 'Script', id)


class ExternalScene(ExternalResource):
    def __init__(self, path, id):
        super().__init__(path, 'PackedScene', id)


class Node:
    def __init__(self, name, parent='.', instance=None, type=None, attributes=OrderedDict()):
        self.name = name
        self.parent = parent
        self.instance = instance
        self.type = type
        self.attributes = attributes

    def __str__(self):
        context = {
            'name': f'"{self.name}"'
        }
        if self.parent:
            if type(self.parent) == str:
                context['parent'] = f'"{self.parent}"'
            elif type(self.parent) == Node:
                context['parent'] = f'"{self.parent.name}"'
        if self.instance:
            context['instance'] = f'ExtResource( {self.instance.id} )'
        if self.type:
            context['type'] = f'"{self.type}"'

        content = ['[node {}]'.format(' '.join([f'{k}={v}' for k, v in context.items()])),]
        for k, v in self.attributes.items():
            if type(v) == bool:
                v = str(v).lower()
            content.append(f'{k} = {v}')
        return '\n'.join(content)


class Transform:
    def __init__(self, *matrix):
        self.matrix = matrix

    def __str__(self):
        return 'Transform( {} )'.format(', '.join(map(str, self.matrix)))


class Scene:
    def __init__(self, resources=[], nodes=[]):
        self.resources = resources
        self.nodes = nodes

    def __str__(self):
        content = [f'[gd_scene load_steps={len(self.resources) + 1} format=2]',]
        content.append('\n'.join(map(str, self.resources)))
        content += list(map(str, self.nodes))
        return '\n\n'.join(content)

def create():
    tile_root = Node('Tiles', type='Spatial')
    master = Scene(nodes=[
        Node('Spatial', parent=None, type='Spatial'),
        tile_root,
    ])

    tile_re = re.compile('^Tile_(\d{3})_(\d{3})$')
    for name in os.listdir(os.path.join(project, 'dataset', 'gltf', 'L20')):
        match = tile_re.match(name)
        if match:
            tile_x = int(match.group(1))
            tile_y = int(match.group(2))

            # create {path}.tscn
            # assumption: L20, L17 and L15 lods exist for every tile
            resources = [
                ExternalScript('res://addons/lod/lod_spatial.gd', 1),
                ExternalScene(f'res://dataset/gltf/L20/{name}/{name}_L20.gltf', 2),
                ExternalScene(f'res://dataset/gltf/L17/{name}/{name}_L17.gltf', 3),
                ExternalScene(f'res://dataset/gltf/L15/{name}/{name}_L15.gltf', 4),
            ]

            nodes = [
                Node(name, parent=None, type='Spatial', attributes=OrderedDict(
                    script = f'ExtResource( 1 )',
                    lod_0_max_distance = 400.0,
                    lod_1_max_distance = 800.0,
                    lod_2_max_distance = 3000.0,
                )),
                Node(f'{name}_L20-lod0', instance=resources[1], attributes=OrderedDict(
                    visible = False
                )),
                Node(f'{name}_L17-lod1', instance=resources[2], attributes=OrderedDict(
                    visible = False
                )),
                Node(f'{name}_L15-lod2', instance=resources[3]),
            ]

            scene = Scene(resources, nodes)
            scene_filepath = os.path.join(project, 'dataset', f'{name}.tscn')
            print(scene_filepath)
            with open(scene_filepath, 'w') as f:
                f.write(str(scene))

            tile_scene = ExternalScene(f'res://dataset/{name}.tscn', len(master.resources) + 1)
            master.resources.append(tile_scene)
            master.nodes.append(Node(name, parent=tile_root, instance=tile_scene, attributes=OrderedDict(
                transform = Transform(
                    1, 0, 0,
                    0, 1, 0,
                    0, 0, 1,
                    -900-(tile_x-6)*-200, 0, 1250-(tile_y-3)*200)
            )))

    master_filepath = os.path.join(project, 'Master.tscn')
    print(master_filepath)
    with open(master_filepath, 'w') as f:
        f.write(str(master))

if __name__ == "__main__": 
    create()