# coco_json_to_csv_example
Python script that process certain coco dataframe in .json file using pandas and export it to .csv

## How to use:
python3 coco_to_csv.py <link_to_coco_dataset> <path_for_output_csv_file>

## Docker image
Repository contains dockerfile, which can be used to create image containing this script.
In order to get image, clone whole repository and run next command in directory containing downloaded files: 
```
docker build -t <your_docker_id>/cocojtc . 
```
