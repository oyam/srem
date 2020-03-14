# Example of applying SREM to Landsat-8 (OLI) imagery

Codes in `src/l8_angles` are borrowed from https://www.usgs.gov/land-resources/nli/landsat/solar-illumination-and-sensor-viewing-angle-coefficient-files?qt-science_support_page_related_con=1#qt-science_support_page_related_con. Please find detailed information in the page.

## Requirement
[Docker](https://www.docker.com/) is requried in this example.

## Build

```sh
docker build -t example-landsat8 .
```

## Usage
```sh
docker run --rm -it -v `pwd`:/workspace example-landsat8 python3 src/main.py --input_raster_files <path/to/input_raster_files> --metadata_file <path/to/metadata_file> --angle_file <path/to/angle_file> --output_raster_dir <path/to/output_raster_dir>
```

Help
```
$ docker run --rm -it -v `pwd`:/workspace example-landsat8 python3 src/main.py --help
usage: main.py [-h] -i [INPUT_RASTER_FILES [INPUT_RASTER_FILES ...]] -m
               METADATA_FILE -a ANGLE_FILE -o OUTPUT_RASTER_DIR

optional arguments:
  -h, --help            show this help message and exit
  -i [INPUT_RASTER_FILES [INPUT_RASTER_FILES ...]], --input_raster_files [INPUT_RASTER_FILES [INPUT_RASTER_FILES ...]]
                        Path to input raster files
  -m METADATA_FILE, --metadata_file METADATA_FILE
                        Path to metadata file
  -a ANGLE_FILE, --angle_file ANGLE_FILE
                        Path to angle file
  -o OUTPUT_RASTER_DIR, --output_raster_dir OUTPUT_RASTER_DIR
                        Path to output directory. Each file name is same as
                        input raster file name in this example.
```

Example of usage
```sh
docker run --rm -it -v `pwd`:/workspace example-landsat8 python3 src/main.py -i data/*B[1-9].TIF -m data/LC08_L1TP_013032_20200222_20200225_01_T1_MTL.json -a data/LC08_L1TP_013032_20200222_20200225_01_T1_ANG.txt -o output
```

### Lint
```bash
docker run \
    --rm -it \
    -v `pwd`:/workspace \
    example-landsat8 /bin/bash -c \
        "pip3 install -r requirements-dev.txt && \
        flake8 --config=.flake8"
```

### Type check
```bash
docker run \
    --rm -it \
    -v `pwd`:/workspace \
    example-landsat8 /bin/bash -c \
        "pip3 install -r requirements-dev.txt && \
        mypy --config-file mypy.ini ./src/*.py"
```

### Unit test
AWS account information in ~/.aws/credential is required in this unit test. 
```bash
docker run \
    --rm -it \
    -e "PYTHONPATH=./src" \
    -e "HOME=/home" \
    -v `pwd`:/workspace \
    -v "$HOME/.aws:/home/.aws" \
    example-landsat8 /bin/bash -c \
        "pip3 install -r requirements-dev.txt && pytest tests"
```
