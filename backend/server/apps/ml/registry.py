from apps.endpoints.models import Endpoint
from apps.endpoints.models import MLAlgorithm
from apps.endpoints.models import MLAlgorithmStatus

# registry is basically a class with dictionary mapping the mlalgorithm object id to algorithm object
# adding to the registry also updates the database
class MLRegistry:
    def __init__(self):
        self.endpoints = {}

    def add_algorithm(self, endpoint_name, algorithm_object, algorithm_name, algorithm_status, algorithm_version, owner, algorithm_description, algorithm_code):

        # creates an endpoint object
        endpoint, _ = Endpoint.objects.get_or_create(name=endpoint_name, owner=owner)

        # creates an mlalgorithm object
        database_object, algorithm_created = MLAlgorithm.objects.get_or_create(
            name=algorithm_name,
            description=algorithm_description,
            code=algorithm_code,
            version=algorithm_version,
            owner=owner,
            parent_endpoint=endpoint
            )
        
        # create an mlalgorithmstatus object
        if algorithm_created:
            status = MLAlgorithmStatus(status=algorithm_status,
                                        created_by=owner,
                                        parent_mlalgorithm=database_object,
                                        active=True)
            status.save()
        
        # add model to registry
        self.endpoints[database_object.id] = algorithm_object