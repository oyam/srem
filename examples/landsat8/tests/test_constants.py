import pytest

from constants import OLI_BAND_ID, OLI_WAVELENGTHS


def test_num_wavelengths():
    assert len(OLI_WAVELENGTHS) == len(OLI_BAND_ID)
