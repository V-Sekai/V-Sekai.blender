#!/usr/bin/env python3

from cog import BasePredictor, Input, Path, BaseModel, File
import os
directory = '/root/.config/blendersynth'
file_path = os.path.join(directory, 'config.ini')
os.makedirs(directory, exist_ok=True)
open(file_path, 'w').close()
import blendersynth as bsyn
import numpy as np

class Output(BaseModel):
    response: Path

class Predictor(BasePredictor):
    def setup(self):
        pass

    def predict(self, input_scene: Path = Input(description="Input scene")) -> Output:
        bsyn.run_this_script(debug=False)

        bsyn.render.set_resolution(1024, 1024)
        bsyn.render.set_cycles_samples(10)

        floor = bsyn.Mesh.from_primitive('plane', scale=35) # Create floor
        N = 10 # Number of objects
        R = 3 # Radius of circle
        np.random.seed(6)
        objects = []
        for i in range(N):
            object = bsyn.Mesh.from_primitive(['cone', 'sphere', 'cube'][np.random.randint(3)],
                                    scale=np.random.uniform(0.3, 1.0),
                                    location=(np.sin(i / N * 2 * np.pi) * R, np.cos(i / N * 2 * np.pi) * R, 0) # place in a circle
                                            )
            object.set_minimum_to('Z', 0)
            objects.append(object)
        light = bsyn.Light.create('POINT', location=(1, 0, 0), intensity=1000.)

        comp = bsyn.Compositor()
        bounding_box_visual = comp.get_bounding_box_visual()
        keypoints_visual = comp.get_keypoints_visual(marker='x')
        axis_visual = comp.get_axes_visual()
        combined_visual = comp.stack_visuals(bounding_box_visual, keypoints_visual, axis_visual)

        comp.define_output('Image', directory='pose')
        comp.define_output(combined_visual, file_name='visual', directory='pose')

        bounding_boxes = bsyn.annotations.bounding_boxes(objects)

        keypoints = bsyn.annotations.keypoints.project_keypoints([obj.centroid() for obj in objects])

        axes = bsyn.annotations.get_multiple_axes(objects)

        overlay_kwargs = dict(BBox=bounding_boxes, Keypoints=keypoints, Axes=axes)
        comp.render(overlay_kwargs=overlay_kwargs)
        return Output(image=Path('pose/Image0001.png'))


if __name__ == "__main__":
    predictor = Predictor()
    predictor.setup()
    result = predictor.predict("thirdparty/capturing_pose.blend")

