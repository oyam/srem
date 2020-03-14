import glob
import os
import subprocess

import pytest

TEST_S2A_PRODUCT_URL = 's3://sentinel-s2-l1c/tiles/18/T/WL/2020/3/1/0/'
TEST_S2B_PRODUCT_URL = 's3://sentinel-s2-l1c/tiles/18/T/WL/2020/2/22/0/'


@pytest.fixture(scope='session')
def S2A_raster_files(tmpdir_factory):
    dst_dir = tmpdir_factory.mktemp('S2A')
    cmd = (f'aws s3 sync {TEST_S2A_PRODUCT_URL} {str(dst_dir)} '
            '--request-payer --exclude "*" --include "B*.jp2"')
    subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL)
    file_paths = glob.glob(os.path.join(dst_dir, 'B*.jp2'))
    return file_paths


@pytest.fixture(scope='session')
def S2B_raster_files(tmpdir_factory):
    dst_dir = tmpdir_factory.mktemp('S2B')
    cmd = (f'aws s3 sync {TEST_S2B_PRODUCT_URL} {str(dst_dir)} '
            '--request-payer --exclude "*" --include "B*.jp2"')
    subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL)
    file_paths = glob.glob(os.path.join(dst_dir, 'B*.jp2'))
    return file_paths


@pytest.fixture(scope='session')
def S2A_metadata_file(tmpdir_factory):
    dst_dir = tmpdir_factory.mktemp('S2A')
    cmd = (f'aws s3 sync {TEST_S2A_PRODUCT_URL} {str(dst_dir)} '
            '--request-payer --exclude "*" --include "metadata.xml"')
    subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL)
    file_path = os.path.join(dst_dir, 'metadata.xml')
    return file_path


@pytest.fixture(scope='session')
def S2B_metadata_file(tmpdir_factory):
    dst_dir = tmpdir_factory.mktemp('S2B')
    cmd = (f'aws s3 sync {TEST_S2B_PRODUCT_URL} {str(dst_dir)} '
            '--request-payer --exclude "*" --include "metadata.xml"')
    subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL)
    file_path = os.path.join(dst_dir, 'metadata.xml')
    return file_path


@pytest.fixture
def angle_keys():
    keys = set([
        'sensor_azimuth_angle_deg',
        'sensor_zenith_angle_deg',
        'solar_azimuth_angle_deg',
        'solar_zenith_angle_deg'])
    return keys
