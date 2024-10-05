from enum import Enum

class Significances(Enum):
    consumer_grade = "Consumer Grade"
    industrial_grade = "Industrial Grade"
    mil_spec_grade = "Mil-Spec Grade"
    restricted = "Restricted"
    classified = "Classified"
    covert = "Covert"
    
significances_grade = {
    "Consumer Grade": 0,
    "Industrial Grade": 1,
    "Mil-Spec Grade": 2,
    "Restricted": 3,
    "Classified": 4,
    "Covert": 5
}