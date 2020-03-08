import pytest

from constants import BAND_ID
from metadata_parser import MetadataParser


def test_get_mean_angles(S2A_metadata_file, angle_keys):
    m_parser = MetadataParser(S2A_metadata_file)
    for band_id in BAND_ID:
        angles = m_parser.get_mean_angles(band_id.value)
        assert set(angles.keys()) == angle_keys
        for angle in angles.values():
            assert isinstance(angle, float)


def test_get_platform(S2A_metadata_file, S2B_metadata_file):
    _test_get_platform(S2A_metadata_file, 'S2A')
    _test_get_platform(S2B_metadata_file, 'S2B')


def _test_get_platform(metadata_file, expected_platform):
    m_parser = MetadataParser(metadata_file)
    platform = m_parser.get_platform()
    assert platform == expected_platform
