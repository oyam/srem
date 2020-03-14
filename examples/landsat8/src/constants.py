from enum import auto, Enum


class OLI_BAND_ID(Enum):
    B1 = auto()
    B2 = auto()
    B3 = auto()
    B4 = auto()
    B5 = auto()
    B6 = auto()
    B7 = auto()
    B8 = auto()
    B9 = auto()


# unit is micrometer.
# See https://landsat.gsfc.nasa.gov/preliminary-spectral-response-of-the-operational-land-imager-in-band-band-average-relative-spectral-response/
OLI_WAVELENGTHS = {
    1: 0.44296,
    2: 0.48204,
    3: 0.56141,
    4: 0.65459,
    5: 0.86467,
    6: 1.60886,
    7: 2.20073,
    8: 0.58950,
    9: 1.37343
}


REFLECTANCE_SCALING_FACTOR = 10000
