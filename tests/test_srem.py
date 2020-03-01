import numpy as np
import pytest

import srem


def test_srem_with_float_angle(toa_reflectance, wavelengths, angle_degs_float):
    for wavelength in wavelengths:
        surface_reflectance = srem.srem(
            toa_reflectance, wavelength, **angle_degs_float
        )
        assert surface_reflectance.shape == toa_reflectance.shape
        assert surface_reflectance.dtype == toa_reflectance.dtype


def test_srem_with_valid_array_angle(toa_reflectance, wavelengths, angle_degs_array):
    for wavelength in wavelengths:
        surface_reflectance = srem.srem(
            toa_reflectance, wavelength, **angle_degs_array
        )
        assert surface_reflectance.shape == toa_reflectance.shape
        assert surface_reflectance.dtype == toa_reflectance.dtype


def test_srem_with_invalid_array_angle(toa_reflectance, wavelengths, invalid_angle_degs_array):
    with pytest.raises(ValueError):
        _ = srem.srem(
            toa_reflectance, wavelengths[0], **invalid_angle_degs_array
        )

def test_check_valid_angles(toa_reflectance, angle_degs_array):
    assert not srem._has_invalid_angle(angle_degs_array.values(), toa_reflectance.shape)


def test_check_invalid_angles(toa_reflectance, invalid_angle_degs_array):
    assert srem._has_invalid_angle(invalid_angle_degs_array.values(), toa_reflectance.shape)


def test_calc_rayleigh_optical_depth(wavelengths):
    for wavelength in wavelengths:
        rayleigh_optical_depth = srem._calc_rayleigh_optical_depth(wavelength)
        assert isinstance(rayleigh_optical_depth, float)
        assert rayleigh_optical_depth > 0


def test_calc_rayleigh_reflectance_with_float_angle(wavelengths, angle_rads_float, rayleigh_optical_depths):
    for wavelength, rayleigh_optical_depth in zip(wavelengths, rayleigh_optical_depths):
        rayleigh_reflectance = srem._calc_rayleigh_reflectance(
            wavelength=wavelength,
            rayleigh_optical_depth=rayleigh_optical_depth,
            **angle_rads_float)
        assert isinstance(rayleigh_reflectance, float)


def test_calc_rayleigh_reflectance_with_array_angle(wavelengths, angle_rads_array, rayleigh_optical_depths, toa_reflectance):
    for wavelength, rayleigh_optical_depth in zip(wavelengths, rayleigh_optical_depths):
        rayleigh_reflectance = srem._calc_rayleigh_reflectance(
            wavelength=wavelength,
            rayleigh_optical_depth=rayleigh_optical_depth,
            **angle_rads_array)
        assert isinstance(rayleigh_reflectance, np.ndarray)
        assert rayleigh_reflectance.shape == toa_reflectance.shape


def test_calc_rayleigh_phase_with_float_angle(angle_rads_float):
    rayleigh_phase = srem._calc_rayleigh_phase(**angle_rads_float)
    assert isinstance(rayleigh_phase, float)
    assert rayleigh_phase >= 0


def test_calc_rayleigh_phase_with_array_angle(angle_rads_array, toa_reflectance):
    rayleigh_phase = srem._calc_rayleigh_phase(**angle_rads_array)
    assert isinstance(rayleigh_phase, np.ndarray)
    assert rayleigh_phase.shape == toa_reflectance.shape
    assert rayleigh_phase.min() >= 0


def test_calc_scattering_angle_with_float_angle(angle_rads_float):
    scattering_angle = srem._calc_scattering_angle(**angle_rads_float)
    assert isinstance(scattering_angle, float)
    assert 0 <= scattering_angle <= np.pi


def test_calc_scattering_angle_with_array_angle(angle_rads_array, toa_reflectance):
    scattering_angle = srem._calc_rayleigh_phase(**angle_rads_array)
    assert isinstance(scattering_angle, np.ndarray)
    assert scattering_angle.shape == toa_reflectance.shape
    assert scattering_angle.min() >= 0
    assert scattering_angle.max() <= np.pi


def test_calc_relative_azimuth_angle_with_float_angle(angle_rads_float):
    relative_azimuth_angle = srem._calc_relative_azimuth_angle(
        angle_1=angle_rads_float['solar_azimuth_angle'],
        angle_2=angle_rads_float['sensor_azimuth_angle'])
    assert isinstance(relative_azimuth_angle, float)
    assert 0 <= relative_azimuth_angle <= np.pi


def test_calc_relative_azimuth_angle_with_array_angle(angle_rads_array, toa_reflectance):
    relative_azimuth_angle = srem._calc_relative_azimuth_angle(
        angle_1=angle_rads_array['solar_azimuth_angle'],
        angle_2=angle_rads_array['sensor_azimuth_angle'])
    assert isinstance(relative_azimuth_angle, np.ndarray)
    assert relative_azimuth_angle.shape == toa_reflectance.shape
    assert relative_azimuth_angle.min() >= 0
    assert relative_azimuth_angle.max() <= np.pi


def test_calc_satm(rayleigh_optical_depths):
    for rayleigh_optical_depth in rayleigh_optical_depths:
        satm = srem._calc_satm(rayleigh_optical_depth)
        assert isinstance(satm, float)
        assert satm > 0


def test_total_transmittance_with_float_angle(angle_rads_float, rayleigh_optical_depths):
    for rayleigh_optical_depth in rayleigh_optical_depths:
        total_transmittance = srem._calc_total_transmittance(
            solar_zenith_angle=angle_rads_float['solar_zenith_angle'],
            sensor_zenith_angle=angle_rads_float['sensor_zenith_angle'],
            rayleigh_optical_depth=rayleigh_optical_depth
        )
        assert isinstance(total_transmittance, float)
        assert total_transmittance > 0


def test_calc_total_transmittance_with_array_angle(angle_rads_array, rayleigh_optical_depths, toa_reflectance):
    for rayleigh_optical_depth in rayleigh_optical_depths:
        total_transmittance = srem._calc_total_transmittance(
            solar_zenith_angle=angle_rads_array['solar_zenith_angle'],
            sensor_zenith_angle=angle_rads_array['sensor_zenith_angle'],
            rayleigh_optical_depth=rayleigh_optical_depth
        )
        assert isinstance(total_transmittance, np.ndarray)
        assert total_transmittance.shape == toa_reflectance.shape
        assert total_transmittance.min() > 0
