from import_export import resources
from .models import Task

class DataResource(resources.ModelResource):
    class Meta:
        model = Task