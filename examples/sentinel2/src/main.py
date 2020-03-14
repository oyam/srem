import argparse
import os
from typing import List

from tqdm import tqdm

from apply_srem import apply_srem


def main(input_raster_files: List[str],
         metadata_file: str,
         output_raster_dir: str) -> None:
    os.makedirs(output_raster_dir, exist_ok=True)
    for input_raster_file in tqdm(input_raster_files):
        output_raster_file = os.path.join(
            output_raster_dir,
            os.path.basename(input_raster_file))
        apply_srem(
            input_raster_file=input_raster_file,
            metadata_file=metadata_file,
            output_raster_file=output_raster_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_raster_files', nargs='*', required=True,
                        help='Path to input raster files')
    parser.add_argument('-m', '--metadata_file', required=True,
                        help='Path to metadata file')
    parser.add_argument('-o', '--output_raster_dir', required=True,
                        help='Path to output directory. Each file name is '
                             'same as input raster file name in this example.')
    args = parser.parse_args()

    main(
        input_raster_files=args.input_raster_files,
        metadata_file=args.metadata_file,
        output_raster_dir=args.output_raster_dir)
