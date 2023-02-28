import re
from typing import Tuple, Union


def valid_cpf(cpf: Union[int, str]) -> Tuple[bool, int]:
    """
    Validates if it's a valid cpf.

    If the type of the given value is already a integer, it's assumed valid.
    If it's a string, removes all the punctuation, and tries to 
    convert to a integer. 
    If it can converted it's assumed valid, if not, is invalid
    """
    
    if type(cpf) is int:
        return True, cpf

    try:
        cpf = re.sub(r'[^\w\s]', '', cpf)
        cpf = int(cpf)
        return True, cpf
    except:
        return False, cpf
