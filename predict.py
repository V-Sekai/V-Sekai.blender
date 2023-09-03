import bpy
from cog import BasePredictor, Input, Path, BaseModel

class Output(BaseModel):
    response: Path

class Predictor(BasePredictor):
    def setup(self):
        pass

    def predict(self, input_scene: Path = Input(description="Input scene")) -> Output:
        bpy.ops.wm.open_mainfile(filepath=str(input_scene))
        bpy.context.scene.render.resolution_x = 1024
        bpy.context.scene.render.resolution_y = 1024
        bpy.context.scene.cycles.samples = 10

        monkey = bpy.data.objects.get('Monkey')
        cube = bpy.data.objects.get('Cube')

        # Create Compositor Nodes
        bpy.context.scene.use_nodes = True
        tree = bpy.context.scene.node_tree
        links = tree.links
        nodes = tree.nodes
        for node in nodes:
            nodes.remove(node)

        render_layers = nodes.new('CompositorNodeRLayers')
        output = nodes.new('CompositorNodeComposite')

        # Connect Nodes
        links.new(render_layers.outputs[0], output.inputs[0])

        # Render Image
        bpy.ops.render.render()

        image_path = bpy.context.scene.render.filepath + "rendered_image.png"

        return Output(response=Path(image_path))

if __name__ == "__main__":
    predictor = Predictor()
    predictor.setup()
    result = predictor.predict(Path("thirdparty/capturing_pose.blend"))
