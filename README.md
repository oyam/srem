# SREM: A Simplified and Robust Surface Reflectance Estimation Method

![systematic_methodology](./img/systematic_methodology.png)  

[![PyPI version](https://img.shields.io/pypi/v/srem.svg)](https://pypi.python.org/pypi/srem)
[![Python Versions](https://img.shields.io/pypi/pyversions/srem.svg)](https://pypi.org/project/srem/)
[![GitHub license](https://img.shields.io/github/license/oyam/srem.svg)](https://github.com/oyam/srem)
![CI](https://github.com/oyam/srem/workflows/CI/badge.svg)

SREM estimates surface reflectance of satellite imagery without integrating information of aerosol particles and
atmospheric gasses. Core algorithm is based on "A Simplified and Robust Surface Reflectance Estimation Method (SREM) for Use over DiverseLand Surfaces Using Multi-Sensor Data" [[pdf](https://www.mdpi.com/2072-4292/11/11/1344/pdf)]. 


### Installation
This library supports Python >= 3.6
```sh
pip install srem
```

### Usage
```python
import numpy as np
from srem import srem

surface_reflectance = srem(
    toa_reflectance, # np.ndarray with shape of (height, width)
    wavelength, # float in micrometer
    solar_azimuth_angle_deg, # float or np.ndarray with shape of (height, width)
    solar_zenith_angle_deg, # float or np.ndarray with shape of (height, width)
    sensor_azimuth_angle_deg, # float or np.ndarray with shape of (height, width)
    sensor_zenith_angle_deg # float or np.ndarray with shape of (height, width)
)

assert isinstance(surface_reflectance, np.ndarray)
assert surface_reflectance.shape == toa_reflectance.shape
```

For detailed usage, please refer to examples of Landsat-8 and Sentinel-2.
- [example/landsat8](https://github.com/oyam/srem/tree/master/examples/landsat8)
- [example/sentinel2](https://github.com/oyam/srem/tree/master/examples/sentinel2)


### References
- Bilal, Muhammad, et al. "A simplified and robust surface reflectance estimation method (srem) for use over diverse land surfaces using multi-sensor data." Remote Sensing 11.11 (2019): 1344.
