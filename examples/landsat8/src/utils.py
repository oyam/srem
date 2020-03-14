import glob
import os
from typing import Any, Dict, List, Tuple
import subprocess

import numpy as np
from rasterio.windows import Window
import srem

from constants import OLI_BAND_ID, REFLECTANCE_SCALING_FACTOR


def get_band_id(path: str) -> int:
    band_name = os.path.splitext(os.path.basename(path))[0].split('_')[-1]
    band_id = OLI_BAND_ID[band_name].value
    return band_id


def get_pixel_angle_files(angle_file: str,
                          band_id: int,
                          output_dir: str) -> Tuple[str, str]:
    cwd = os.getcwd()
    angle_file = os.path.abspath(angle_file)
    os.chdir(output_dir)
    cmd = f'l8_angles {angle_file} BOTH 1 -b {band_id}'
    subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL)
    solar_angle_file = glob.glob(os.path.join(output_dir, f'*solar_B0{band_id}.img'))[0]
    sensor_angle_file = glob.glob(os.path.join(output_dir, f'*sensor_B0{band_id}.img'))[0]
    os.chdir(cwd)
    return solar_angle_file, sensor_angle_file


def srem_worker(data: List[np.ndarray],
                window: Window,
                ij: int,
                global_args: Dict[Any, Any]) -> np.ndarray:
    nodata_mask = (data[0] == 0)
    surface_reflectance = srem.srem(
        toa_reflectance=data[0],
        wavelength=global_args['wavelength'],
        solar_azimuth_angle_deg=data[1] / 100.,
        solar_zenith_angle_deg=data[2] / 100.,
        sensor_azimuth_angle_deg=data[3] / 100.,
        sensor_zenith_angle_deg=data[4] / 100.,
    )
    # surface reflectance is scaled in this example.
    scaled_sr = \
        surface_reflectance * REFLECTANCE_SCALING_FACTOR
    # crop values less than 1 for defining 1 as minimum value.
    scaled_sr[scaled_sr < 1] = 1
    scaled_sr[nodata_mask] = 0
    scaled_sr = scaled_sr.astype(global_args['dtype'])
    scaled_sr = np.expand_dims(scaled_sr, axis=0)
    return scaled_sr
