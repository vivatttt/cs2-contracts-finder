from dataclasses import dataclass

@dataclass
class Item:
    collection : str = ""
    sign : str = ""
    ext : str = ""
    target_name : str = ""
    price : int = 0
    ratio : int = 0