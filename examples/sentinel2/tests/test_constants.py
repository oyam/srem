import pytest

from constants import BAND_ID, WAVELENGTHS


@pytest.mark.parametrize(
    "platform, expected",
    (
        ['S2A', len(BAND_ID)],
        ['S2B', len(BAND_ID)]
    )
)
def test_num_wavelengths(platform, expected):
    len(WAVELENGTHS[platform]) == expected
