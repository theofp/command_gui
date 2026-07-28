# Some default validators for use with dynamic entries
import re
from typing import List, Union, Dict, Any

# Validators will return a tuple of (bool, value) where bool is the validation result and value is the validated value to be stored in memory

def length_validator(value : Union[str,int,float], boundaries : List[int] = [100,1000]):
# value can only ever really be a string as of now
    if type(value) == str:
        value = list(value)
    if type(value) == int:
        value = list(str(value))
    if type(value) == float:
        value = list(str(int(value)))

    if len(value) < boundaries[0]:
        return False, None
    if len(value) > boundaries[1]:
        return False, None
    return True, value

def path_validator(path : str, is_absolute : bool = True):

    if is_absolute:
        pattern = r"^(/[^/\0]+)+/?$"
    else:
        pattern = r"^(?:\./|\.\./|/)?([^/\0]+(/)?)*$"

    if re.match(pattern, path):
        return True, path
    return False, None

def value_validator(value : str, min_value : Union[int,float], max_value : Union[int,float]):

    if type(value) == str:
        value = int(value)
    if value < min_value:
        return False, None
    if value > max_value:
        return False, None
    return True, value

def dictionary_validator(dictionary : Dict, key : Any):

    if key in dictionary.keys():
        return True, dictionary[key]
    return False, None

def list_validator(value : Any, list : List):
    
    if value in list:
        return True, value
    return False, None

