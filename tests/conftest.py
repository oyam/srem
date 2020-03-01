import numpy as np
import pytest

import srem


TEST_WIDTH = 1000
TEST_HEIGHT = 1000


@pytest.fixture
def toa_reflectance():
    return np.random.rand(TEST_HEIGHT, TEST_WIDTH)


@pytest.fixture
def wavelengths():
    # unit is micrometer
    return [0.4430, 0.4820, 0.5615, 0.6545, 0.8650, 1.6085, 2.2005]


@pytest.fixture
def angle_degs_float():
    angle_degs = {
        'solar_azimuth_angle_deg': 158.1,
        'solar_zenith_angle_deg': 53.1,
        'sensor_azimuth_angle_deg': 258.3,
        'sensor_zenith_angle_deg': 16.9
    }
    return angle_degs


@pytest.fixture
def angle_degs_array(angle_degs_float):
    angle_degs = {}
    for k, v in angle_degs_float.items():
        angle_degs[k] = v * np.ones((TEST_HEIGHT, TEST_WIDTH)) + np.random.rand(TEST_HEIGHT, TEST_WIDTH)
    return angle_degs


@pytest.fixture
def invalid_angle_degs_array(angle_degs_float):
    angle_degs = {}
    for k, v in angle_degs_float.items():
        angle_degs[k] = v * np.ones((TEST_HEIGHT + 1, TEST_WIDTH + 1)) + np.random.rand(TEST_HEIGHT + 1, TEST_WIDTH + 1)
    return angle_degs


@pytest.fixture
def angle_rads_float(angle_degs_float):
    angle_rads = {}
    for k, v in angle_degs_float.items():
        key = k.replace('_deg', '')
        angle_rads[key] = np.deg2rad(v)
    return angle_rads


@pytest.fixture
def angle_rads_array(angle_degs_array):
    angle_rads = {}
    for k, v in angle_degs_array.items():
        key = k.replace('_deg', '')
        angle_rads[key] = np.deg2rad(v)
    return angle_rads


@pytest.fixture
def rayleigh_optical_depths(wavelengths):
    return [srem._calc_rayleigh_optical_depth(w) for w in wavelengths]
