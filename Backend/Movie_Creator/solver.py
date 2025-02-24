import json
import os
import openai

from Backend.Api.export_file import aws_uploader
from Backend.Movie_Assembler.create_movie import create_movie
from core import core


class solver:
    def __init__(self, problem):
        self.problem = problem
        self.link = ''
        os.environ[
            "OPENAI_API_KEY"] = 'OPENAI_API_KEY REDACTED FOR SECURITY PURPOSES'
        openai.api_key = os.environ["OPENAI_API_KEY"]

    def upload(self):
        core_instance = core(self.problem, openai.api_key)
        video_inputs = core_instance.start()
        mov = create_movie(openai.api_key)
        movie_name = mov.create_video_from_inputs(video_inputs)
        mov.create_video_from_inputs(video_inputs, movie_name)
        self.link = aws_uploader().upload(file_path=movie_name)
        return self.to_json()

    def to_json(self):
        return json.dumps({'url': self.link})
