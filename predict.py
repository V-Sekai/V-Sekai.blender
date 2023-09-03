#!/usr/bin/env python3

from cog import BasePredictor, Input, Path, BaseModel, File
import blendersynth as bsyn

class Output(BaseModel):
    response: Path

class Predictor(BasePredictor):
    def setup(self):
        pass

    def predict(self, input_scene: Path = Input(description="Input scene")) -> Output:
        bsyn.run_this_script(debug = False)
        bsyn.load_blend(str(image_path))  # load from scene
        bsyn.render.set_resolution(1024, 1024)
        bsyn.render.set_cycles_samples(10)

        monkey = bsyn.Mesh.from_scene('Monkey')
        cube = bsyn.Mesh.from_scene('Cube')

        comp = bsyn.Compositor()
        bounding_box_visual = comp.get_bounding_box_visual()
        keypoints_visual = comp.get_keypoints_visual(marker='x')  # Create a visual of keypoints
        axis_visual = comp.get_axes_visual()
        combined_visual = comp.stack_visuals(bounding_box_visual, keypoints_visual, axis_visual)

        comp.define_output('Image', directory='pose')
        comp.define_output(combined_visual, file_name='visual', directory='pose')

        objects = [monkey, cube]
        bounding_boxes = bsyn.annotations.bounding_boxes(objects)

        keypoints = bsyn.annotations.keypoints.project_keypoints([obj.centroid() for obj in objects])

        axes = bsyn.annotations.get_multiple_axes(objects)

        overlay_kwargs = dict(BBox=bounding_boxes, Keypoints=keypoints, Axes=axes)
        comp.render(overlay_kwargs=overlay_kwargs)
        image_path = bsyn.render.get_output_path('Image', file_name='rendered_image.png')

        return Output(image=Path(image_path))

if __name__ == "__main__":
    predictor = Predictor()
    predictor.setup()
    result = predictor.predict("thirdparty/capturing_pose.blend")

