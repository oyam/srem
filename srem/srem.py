from typing import List, Tuple, Union

import numpy as np


def srem(toa_reflectance: np.ndarray,
         wavelength: float,
         solar_azimuth_angle_deg: Union[float, np.ndarray],
         solar_zenith_angle_deg: Union[float, np.ndarray],
         sensor_azimuth_angle_deg: Union[float, np.ndarray],
         sensor_zenith_angle_deg: Union[float, np.ndarray]) -> np.ndarray:
    """Calculates surface reflectance

    See: https://www.mdpi.com/2072-4292/11/11/1344

    Args:
        toa_reflectance (numpy.ndarray): Top of atmosphere reflectance.
            Expected shape == (height, width)
        wavelength (float): Wavelength of toa_reflectance in micrometer.
        solar_azimuth_angle_deg (float or numpy.ndarray):
            Solar azimuth angle. Expected unit is degree. Height and width have
            to be same as those of toa_reflectance when using numpy.ndarray.
        solar_zenith_angle_deg (float or numpy.ndarray):
            Solar zenith angle. Expected unit is degree. Height and width have
            to be same as those of toa_reflectance when using numpy.ndarray.
        sensor_azimuth_angle_deg (float or numpy.ndarray):
            Sensor azimuth angle. Expected unit is degree. Height and width have
            to be same as those of toa_reflectance when using numpy.ndarray.
        sensor_zenith_angle_deg (float or numpy.ndarray):
            Sensor zenith angle. Expected unit is degree. Height and width have
            to be same as those of toa_reflectance when using numpy.ndarray.

    Returns:
        numpy.ndarray: Surface reflectance with same shape as toa_reflectance
    """
    if _has_invalid_angle(
            angles=[
                solar_azimuth_angle_deg,
                solar_zenith_angle_deg,
                sensor_azimuth_angle_deg,
                sensor_zenith_angle_deg],
            shape=toa_reflectance.shape):
        raise ValueError('An angle have to be float or numpy.ndarray that has same shape as toa_reflectance.')

    solar_azimuth_angle = np.deg2rad(solar_azimuth_angle_deg)
    solar_zenith_angle = np.deg2rad(solar_zenith_angle_deg)
    sensor_azimuth_angle = np.deg2rad(sensor_azimuth_angle_deg)
    sensor_zenith_angle = np.deg2rad(sensor_zenith_angle_deg)

    rayleigh_optical_depth = _calc_rayleigh_optical_depth(
        wavelength=wavelength)
    rayleigh_reflectance = _calc_rayleigh_reflectance(
        wavelength=wavelength,
        solar_azimuth_angle=solar_azimuth_angle,
        solar_zenith_angle=solar_zenith_angle,
        sensor_azimuth_angle=sensor_azimuth_angle,
        sensor_zenith_angle=sensor_zenith_angle,
        rayleigh_optical_depth=rayleigh_optical_depth)
    satm = _calc_satm(rayleigh_optical_depth=rayleigh_optical_depth)
    total_transmittance = _calc_total_transmittance(
        solar_zenith_angle=solar_zenith_angle,
        sensor_zenith_angle=sensor_zenith_angle,
        rayleigh_optical_depth=rayleigh_optical_depth)
    surface_reflectance = \
        (toa_reflectance - rayleigh_reflectance) \
        / ((toa_reflectance - rayleigh_reflectance) * satm + total_transmittance)

    return surface_reflectance


def _has_invalid_angle(angles: List[Union[float, np.ndarray]],
                       shape: Tuple[int, int]) -> bool:
    for angle in angles:
        if isinstance(angle, np.ndarray) and angle.shape != shape:
            return True
    return False


def _calc_rayleigh_optical_depth(wavelength: float) -> float:
    rayleigh_optical_depth = \
        0.008569 * (1 / (wavelength ** 4)) \
        * (1 + 0.0113 * (1 / (wavelength ** 2)) + 0.00013 * (1 / (wavelength ** 4)))
    return rayleigh_optical_depth


def _calc_rayleigh_reflectance(wavelength: float,
                               solar_azimuth_angle: Union[float, np.ndarray],
                               solar_zenith_angle: Union[float, np.ndarray],
                               sensor_azimuth_angle: Union[float, np.ndarray],
                               sensor_zenith_angle: Union[float, np.ndarray],
                               rayleigh_optical_depth: float) -> Union[float, np.ndarray]:
    rayleigh_phase = _calc_rayleigh_phase(
        solar_azimuth_angle=solar_azimuth_angle,
        solar_zenith_angle=solar_zenith_angle,
        sensor_azimuth_angle=sensor_azimuth_angle,
        sensor_zenith_angle=sensor_zenith_angle)
    us = np.cos(solar_zenith_angle)
    uv = np.cos(sensor_zenith_angle)
    air_mass = 1 / us + 1 / uv
    rayleigh_reflectance = \
        (rayleigh_phase * (1 - np.exp(-1 * air_mass * rayleigh_optical_depth))) \
        / (4 * (us + uv))
    return rayleigh_reflectance


def _calc_rayleigh_phase(solar_azimuth_angle: Union[float, np.ndarray],
                         solar_zenith_angle: Union[float, np.ndarray],
                         sensor_azimuth_angle: Union[float, np.ndarray],
                         sensor_zenith_angle: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    coef_a = 0.9587256
    coef_b = 1 - coef_a
    scattering_angle = _calc_scattering_angle(
        solar_azimuth_angle=solar_azimuth_angle,
        solar_zenith_angle=solar_zenith_angle,
        sensor_azimuth_angle=sensor_azimuth_angle,
        sensor_zenith_angle=sensor_zenith_angle)
    rayleigh_phase = 3 * coef_a * (1 + np.cos(scattering_angle) ** 2) / (4 + coef_b)
    return rayleigh_phase


def _calc_scattering_angle(solar_azimuth_angle: Union[float, np.ndarray],
                           solar_zenith_angle: Union[float, np.ndarray],
                           sensor_azimuth_angle: Union[float, np.ndarray],
                           sensor_zenith_angle: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    relative_azimuth_angle = _calc_relative_azimuth_angle(
        angle_1=solar_azimuth_angle,
        angle_2=sensor_azimuth_angle)
    scattering_angle = np.arccos(
        -1 * np.cos(sensor_zenith_angle) * np.cos(solar_zenith_angle)
        + np.sin(sensor_zenith_angle) * np.sin(solar_zenith_angle) * np.cos(relative_azimuth_angle))
    return scattering_angle


def _calc_relative_azimuth_angle(angle_1: Union[float, np.ndarray],
                                 angle_2: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    delta_phi = angle_1 - angle_2
    delta_phi = np.where(delta_phi > 2 * np.pi, delta_phi - 2 * np.pi, delta_phi)
    delta_phi = np.where(delta_phi < 0, delta_phi + 2 * np.pi, delta_phi)
    relative_azimuth_angle = np.abs(delta_phi - np.pi)
    return relative_azimuth_angle


def _calc_satm(rayleigh_optical_depth: float) -> float:
    satm = 0.92 * rayleigh_optical_depth * (np.exp(-1 * rayleigh_optical_depth))
    return satm


def _calc_total_transmittance(solar_zenith_angle: Union[float, np.ndarray],
                              sensor_zenith_angle: Union[float, np.ndarray],
                              rayleigh_optical_depth: float) -> Union[float, np.ndarray]:
    us = np.cos(solar_zenith_angle)
    uv = np.cos(sensor_zenith_angle)
    ts = np.exp(-1 * rayleigh_optical_depth / us) \
        + np.exp(-1 * rayleigh_optical_depth / us) * (np.exp(0.52 * rayleigh_optical_depth / us) - 1)
    tv = np.exp(-1 * rayleigh_optical_depth / uv) \
        + np.exp(-1 * rayleigh_optical_depth / uv) * (np.exp(0.52 * rayleigh_optical_depth / uv) - 1)
    total_transmittance = ts * tv
    return total_transmittance
