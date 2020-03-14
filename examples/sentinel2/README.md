# Example of applying SREM to Sentinel-2 imagery

Mean solar and viewing angles are used as an example of float value of angles. Regarding example of pixel level angles, please check [example of Landsat-8](https://github.com/oyam/srem/tree/master/examples/landsat8). Geotiff format is used as output format in this example.

## Requirement
[Docker](https://www.docker.com/) is requried in this example.

## Build

```sh
docker build -t example-sentinel2 .
```

## Usage
```sh
docker run \
    --rm -it \
    -v `pwd`:/workspace \
    example-sentinel2 python3 src/main.py \
    --input_raster_files <path/to/input_raster_files> \
    --metadata_file <path/to/metadata_file> \
    --output_raster_dir <path/to/output_raster_dir>
```

Help
```
$ docker run --rm -it -v `pwd`:/workspace example-sentinel2 python3 src/main.py --help
usage: main.py [-h] -i [INPUT_RASTER_FILES [INPUT_RASTER_FILES ...]] -m
               METADATA_FILE -o OUTPUT_RASTER_DIR

optional arguments:
  -h, --help            show this help message and exit
  -i [INPUT_RASTER_FILES [INPUT_RASTER_FILES ...]], --input_raster_files [INPUT_RASTER_FILES [INPUT_RASTER_FILES ...]]
                        Path to input raster files
  -m METADATA_FILE, --metadata_file METADATA_FILE
                        Path to metadata file
  -o OUTPUT_RASTER_DIR, --output_raster_dir OUTPUT_RASTER_DIR
                        Path to output directory. Each file name is same as
                        input raster file name in this example.
```

Example of usage
```sh
docker run \
    --rm -it \
    -v `pwd`:/workspace \
    example-sentinel2 python3 src/main.py \
        -i data/B*.jp2 -m data/metadata.xml -o output
```

### Lint
```bash
docker run \
    --rm -it \
    -v `pwd`:/workspace \
    example-sentinel2 /bin/bash -c \
        "pip3 install -r requirements-dev.txt && \
        flake8 --config=.flake8"
```

### Type check
```bash
docker run \
    --rm -it \
    -v `pwd`:/workspace \
    example-sentinel2 /bin/bash -c \
        "pip3 install -r requirements-dev.txt && \
        mypy --config-file mypy.ini ./src/*.py"
```

### Unit test
AWS account information in ~/.aws/credential is required in this unit test. Note this test uses [Requester Pays Buckets](https://docs.aws.amazon.com/AmazonS3/latest/dev/RequesterPaysBuckets.html) for Sentinel-2 data.
```bash
docker run \
    --rm -it \
    -e "PYTHONPATH=./src" \
    -e "HOME=/home" \
    -v `pwd`:/workspace \
    -v "$HOME/.aws:/home/.aws" \
    example-sentinel2 /bin/bash -c \
        "pip3 install -r requirements-dev.txt && pytest tests"
```
