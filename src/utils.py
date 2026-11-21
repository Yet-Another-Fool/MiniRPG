

def clamp(n: int | float, mini: int | float, maxi: int | float):
    if n <= mini:
        return mini
    if n >= maxi:
        return maxi
    return n