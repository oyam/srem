import os
import tempfile

import pytest
import rasterio

from apply_srem import apply_srem


def test_apply_srem(S2A_raster_files,
                    S2A_metadata_file,
                    S2B_raster_files,
                    S2B_metadata_file):
    _test_apply_srem(S2A_raster_files, S2A_metadata_file)
    _test_apply_srem(S2B_raster_files, S2B_metadata_file)


def _test_apply_srem(input_raster_files, metadata_file):
    for input_raster_file in input_raster_files:
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_raster_file = os.path.join(tmp_dir, 'boa.tif')
            apply_srem(
                input_raster_file=input_raster_file,
                metadata_file=metadata_file,
                output_raster_file=output_raster_file)
            assert os.path.exists(output_raster_file)
            with rasterio.open(input_raster_file) as src_ds, \
                 rasterio.open(output_raster_file) as dst_ds:
                assert src_ds.count == dst_ds.count
                assert src_ds.width == dst_ds.width
                assert src_ds.height == dst_ds.height
                assert src_ds.dtypes == dst_ds.dtypes
                assert src_ds.crs == dst_ds.crs
                assert src_ds.transform == dst_ds.transform
