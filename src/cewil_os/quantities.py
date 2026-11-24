def mm_to_m(value_mm: float) -> float:
    if value_mm < 0:
        raise ValueError("value_mm must be non-negative")
    return value_mm / 1000.0

def concrete_volume(length_m: float, width_m: float, depth_m: float) -> float:
    dimensions = (length_m, width_m, depth_m)
    if any(value < 0 for value in dimensions):
        raise ValueError("dimensions must be non-negative")
    return length_m * width_m * depth_m
