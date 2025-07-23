import numpy as np

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