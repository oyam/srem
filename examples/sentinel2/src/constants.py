from enum import Enum


class BAND_ID(Enum):
    B01 = 0
    B02 = 1
    B03 = 2
    B04 = 3
    B05 = 4
    B06 = 5
    B07 = 6
    B08 = 7
    B8A = 8
    B09 = 9
    B10 = 10
    B11 = 11
    B12 = 12


# unit is micrometer.
# See https://sentinel.esa.int/web/sentinel/missions/sentinel-2/instrument-payload/resolution-and-swath
WAVELENGTHS = {
    'S2A': [
        0.4427,
        0.4924,
        0.5598,
        0.6646,
        0.7045,
        0.7405,
        0.7828,
        0.8328,
        0.8647,
        0.9451,
        1.3735,
        1.6137,
        2.2024,
    ],
    'S2B': [
        0.4422,
        0.4921,
        0.5590,
        0.6649,
        0.7038,
        0.7391,
        0.7797,
        0.8329,
        0.8640,
        0.9432,
        1.3769,
        1.6104,
        2.1857,
    ],
}


REFLECTANCE_SCALING_FACTOR = 10000
