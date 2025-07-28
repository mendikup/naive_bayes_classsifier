import numpy as np

"""
Recursively converts NumPy objects into regular Python types.

What it does:
- If the input is a dictionary, it converts all values inside it.
- If it's a list, it converts each item in the list.
- If it's a NumPy array, it turns it into a regular list and continues.
- If it's a NumPy number (like np.int64 or np.float32), it converts it to a regular int or float.
- If it's already a regular Python object, it returns it as is.

Useful when you want to serialize or print data structures that contain NumPy types.
"""

def convert_numpy_object_to_numbers(obj):
    if isinstance(obj, dict):
        return {k: convert_numpy_object_to_numbers(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_object_to_numbers(i) for i in obj]
    elif isinstance(obj, np.ndarray):
        return convert_numpy_object_to_numbers(obj.tolist())
    elif isinstance(obj, (np.integer, np.floating)):
        return obj.item()
    else:
        return obj