import os

import rasterio
import pytest

from constants import OLI_BAND_ID
import utils


def test_band_id(raster_files):
    for raster_file, expected_band in zip(raster_files, OLI_BAND_ID):
        band_id = utils.get_band_id(raster_file)
        assert band_id == expected_band.value


def test_pixel_angle_files(raster_files, angle_file, tmpdir):
    for raster_file in raster_files:
        with rasterio.open(raster_file) as src:
            expected_height = src.height
            expected_width = src.width
        band_id = utils.get_band_id(raster_file)
        angle_files = utils.get_pixel_angle_files(angle_file, band_id, tmpdir)
        assert len(angle_files) == 2
        for f in angle_files:
            assert os.path.exists(f)
            with rasterio.open(f) as src:
                assert src.height == expected_height
                assert src.width == expected_width


def test_srem_worker(input_srem_worker):
    output = utils.srem_worker(**input_srem_worker)
    assert output.shape == (1, *input_srem_worker['data'].shape[1:])
    assert str(output.dtype) == input_srem_worker['global_args']['dtype']
