from .BaseController import BaseController
from .ProjectController import ProjectController
from fastapi import UploadFile
from models.enums.ResponseEnums import ResponseSignal
import re
import os

class DataController(BaseController):
    def __init__(self):
        super().__init__()
        self.size_scale = 1048576

    def validate_updoaded_file(self, file: UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value
        
        if file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale:
            return False, ResponseSignal.FILE_SIZE_EXCEEDED.value
        
        return True, ResponseSignal.FILE_VALIDATION_SUCCESS.value
    
    def generate_unique_filepath(self, original_name: str , project_id: str):
        random_key = self.generate_random_string()
        project_path = ProjectController().ProjectPath(project_id = project_id)

        cleaned_file_name = self.get_clean_file_name(
            original_name = original_name
        )

        file_Path = os.path.join(
            project_path,
            random_key + "_" + cleaned_file_name
        )
        while os.path.exists(file_Path):
            random_key = self.generate_random_string()
            file_Path = os.path.join(
                project_path,
                random_key + "_" + cleaned_file_name
            )
        return file_Path , random_key + "_" + cleaned_file_name

    def get_clean_file_name(self, original_name: str):
        cleaned_name = re.sub(r'[^\w.]','',original_name.strip())
        cleaned_name = cleaned_name.replace(" " , "_")
        return cleaned_name