from typing import Dict
import xml.etree.ElementTree as ET


class MetadataParser(object):
    def __init__(self, metadata_file):
        tree = ET.parse(metadata_file)
        self.root = tree.getroot()

    def get_mean_angles(self, band_id: int) -> Dict[str, float]:
        angles = {}
        for sun_angles in self.root.iter('Mean_Sun_Angle'):
            angles['solar_azimuth_angle_deg'] = \
                float(sun_angles.find('AZIMUTH_ANGLE').text)
            angles['solar_zenith_angle_deg'] = \
                float(sun_angles.find('ZENITH_ANGLE').text)

        for viewing_angles in self.root.iter('Mean_Viewing_Incidence_Angle'):
            attrib = viewing_angles.attrib
            if int(attrib['bandId']) == band_id:
                angles['sensor_azimuth_angle_deg'] = \
                    float(viewing_angles.find('AZIMUTH_ANGLE').text)
                angles['sensor_zenith_angle_deg'] = \
                    float(viewing_angles.find('ZENITH_ANGLE').text)

        return angles

    def get_platform(self) -> str:
        for tile_id in self.root.iter('TILE_ID'):
            platform = tile_id.text[:3]
        return platform
