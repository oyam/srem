import argparse
import os
import tempfile

import rasterio
import riomucho
from rio_toa import reflectance

from constants import OLI_WAVELENGTHS
import utils


def apply_srem(input_raster_file: str,
               metadata_file: str,
               angle_file: str,
               output_raster_file: str) -> None:
    out_dir = os.path.join(os.path.dirname(output_raster_file))
    os.makedirs(out_dir, exist_ok=True)
    band_id = utils.get_band_id(input_raster_file)
    wavelength = OLI_WAVELENGTHS[band_id]

    with tempfile.TemporaryDirectory() as tmp_dir:
        toa_file = os.path.join(tmp_dir, 'toa.tif')
        reflectance.calculate_landsat_reflectance(
            [input_raster_file],
            metadata_file,
            toa_file,
            rescale_factor=1.0,
            creation_options={},
            bands=[band_id],
            dst_dtype='float32',
            processes=1,
            pixel_sunangle=True,
            clip=True)
        solar_angle_file, sensor_angle_file = \
            utils.get_pixel_angle_files(angle_file, band_id, tmp_dir)

        with rasterio.open(input_raster_file) as src:
            options = src.profile
            options.update(nodata=0)
        with riomucho.RioMucho(
                [toa_file, solar_angle_file, sensor_angle_file],
                output_raster_file,
                utils.srem_worker,
                mode='array_read',
                global_args={
                    'wavelength': wavelength,
                    'dtype': options['dtype']},
                options=options) as rios:
            rios.run(4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_raster_file', required=True,
                        help='Path to input raster file')
    parser.add_argument('-m', '--metadata_file', required=True,
                        help='Path to metadata file')
    parser.add_argument('-a', '--angle_file', required=True,
                        help='Path to angle file')
    parser.add_argument('-o', '--output_raster_file', required=True,
                        help='Path to output raster file. GeoTiff format '
                             'is used in this example.')
    args = parser.parse_args()

    apply_srem(
        input_raster_file=args.input_raster_file,
        metadata_file=args.metadata_file,
        angle_file=args.angle_file,
        output_raster_file=args.output_raster_file)
