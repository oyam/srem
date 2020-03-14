import glob
import os
import subprocess

import numpy as np
import pytest
import rasterio
from rasterio.windows import Window

from constants import OLI_WAVELENGTHS
import utils


TEST_ENDPOINT = 's3://landsat-pds/c1/L8/013/032/LC08_L1TP_013032_20200222_20200225_01_T1/'
TEST_WINDOW = Window(256, 256, 256, 256)


@pytest.fixture(scope='session')
def raster_files(tmpdir_factory):
    tmpdir = tmpdir_factory.mktemp('data')
    cmd = (f'aws s3 sync {TEST_ENDPOINT} {str(tmpdir)} '
            '--exclude "*" --include "*B[1-9].TIF"')
    subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL)
    file_paths = sorted(glob.glob(os.path.join(tmpdir, '*B[1-9].TIF')))
    return file_paths


@pytest.fixture(scope='session')
def metadata_file(tmpdir_factory):
    tmpdir = tmpdir_factory.mktemp('data')
    cmd = (f'aws s3 sync {TEST_ENDPOINT} {str(tmpdir)} '
            '--exclude "*" --include "*MTL.json"')
    subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL)
    file_path = glob.glob(os.path.join(tmpdir, '*MTL.json'))[0]
    return file_path


@pytest.fixture(scope='session')
def angle_file(tmpdir_factory):
    tmpdir = tmpdir_factory.mktemp('data')
    cmd = (f'aws s3 sync {TEST_ENDPOINT} {str(tmpdir)} '
            '--exclude "*" --include "*ANG.txt"')
    subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL)
    file_path = glob.glob(os.path.join(tmpdir, '*ANG.txt'))[0]
    return file_path


@pytest.fixture
def cropped_data(raster_files):
    with rasterio.open(raster_files[0]) as src:
        return src.read(window=TEST_WINDOW)


@pytest.fixture
def cropped_angle(raster_files, angle_file, tmpdir):
    raster_file = raster_files[0]
    band_id = utils.get_band_id(raster_file)
    solar_angle_file, sensor_angle_file = \
        utils.get_pixel_angle_files(angle_file, band_id, tmpdir)
    with rasterio.open(solar_angle_file) as src:
        solar_angle_array = src.read(window=TEST_WINDOW)
    with rasterio.open(sensor_angle_file) as src:
        sensor_angle_array = src.read(window=TEST_WINDOW)
    return np.concatenate([solar_angle_array, sensor_angle_array])


@pytest.fixture
def input_srem_worker(cropped_data, cropped_angle):
    data = np.concatenate([cropped_data, cropped_angle])
    input = {
        'data': data,
        'window': TEST_WINDOW,
        'ij': 0,
        'global_args': {
            'wavelength': OLI_WAVELENGTHS[1],
            'dtype': 'int16',
        }
    }
    return input
