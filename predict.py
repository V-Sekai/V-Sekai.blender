#!/usr/bin/env python3

from cog import BasePredictor, Input, Path, BaseModel, File

class Output(BaseModel):
    response: str

class Predictor(BasePredictor):
    def setup(self):
        pass

    def predict(self, prompt: str = Input(description="Prompt")) -> Output:
        return Output(response=prompt + " Pong!")

if __name__ == "__main__":
    predictor = Predictor()
    predictor.setup()
    result = predictor.predict("Ping!")
