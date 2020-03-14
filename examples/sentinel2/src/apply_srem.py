import argparse
import os

import rasterio
import srem

from metadata_parser import MetadataParser
from constants import (
    BAND_ID,
    WAVELENGTHS,
    REFLECTANCE_SCALING_FACTOR
)


def apply_srem(input_raster_file: str,
               metadata_file: str,
               output_raster_file: str) -> None:
    out_dir = os.path.join(os.path.dirname(output_raster_file))
    os.makedirs(out_dir, exist_ok=True)
    m_parser = MetadataParser(metadata_file)
    band_id = BAND_ID[os.path.splitext(input_raster_file)[0][-3:]].value
    platform = m_parser.get_platform()
    wavelength = WAVELENGTHS[platform][band_id]
    angles = m_parser.get_mean_angles(band_id)

    with rasterio.open(input_raster_file) as src:
        toa_reflectance = src.read(1) / REFLECTANCE_SCALING_FACTOR
        profile = src.profile
        nodata_mask = (toa_reflectance == 0)

    surface_reflectance = srem.srem(
        toa_reflectance=toa_reflectance,
        wavelength=wavelength,
        **angles)
    scaled_surface_reflectance = \
        surface_reflectance * REFLECTANCE_SCALING_FACTOR
    # crop values less than 1 for defining 1 as minimum value.
    scaled_surface_reflectance[scaled_surface_reflectance < 1] = 1
    scaled_surface_reflectance[nodata_mask] = 0

    profile.update(
        driver='GTiff',
        compress='deflate',
        nodata=0)
    with rasterio.open(output_raster_file, 'w', **profile) as dst:
        dst.write(
            scaled_surface_reflectance.astype(profile['dtype']),
            indexes=1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_raster_file', required=True,
                        help='Path to input raster file')
    parser.add_argument('-m', '--metadata_file', required=True,
                        help='Path to metadata file')
    parser.add_argument('-o', '--output_raster_file', required=True,
                        help='Path to output raster file. GeoTiff format '
                             'is used in this example.')
    args = parser.parse_args()

    apply_srem(
        input_raster_file=args.input_raster_file,
        metadata_file=args.metadata_file,
        output_raster_file=args.output_raster_file)
