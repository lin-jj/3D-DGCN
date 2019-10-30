# 3D-DGCN

An implementation of 3D-DGCN. The paper is submitted to ICDE 2020.

## Datasets

Our datasets is from the [NYC Bike](https://www.citibikenyc.com/system-data). We obtained road network and 9 categories of PoIs from [OpenStreatMap](https://www.openstreetmap.org/#map=4/36.96/104.17). In two datasets, the city is devided into 128 regular regions and 82 irregular regions, respectively. Each dataset contains 1448 time intervals, spanning from Jul. 1st to Sept. 30th, 2017.

## Requirements

- python 2.7
- PyTorch 0.2.0
- NumPy
- JSON

## Project Structure

- /flow
  - flow_bike_nyc_regular.json contains the regular dataset
  - flow_bike_nyc_irregular.json contains the irregular dataset
- /poi (* = regular or irregular)
  - *_feature.npy is the features of all regions $\bm{F}$
  - *_idx.npy is the index of labeled regions $\mathcal{V}_L$ 
  - *_label.npy is the labels of all regions $\bm{\Omega}$
  - *_weight.npy is the normalization term $frac{1}{|\mathcal{V}_L^{\Omega_i}|}$
- /path
  - regular_path.npy contains the historical flow paths for the regular dataset
  - irregular_path.npy contains the historical flow paths for the irregular dataset
- /main.py ***run this file to get the results of 3D-DGCN in our paper***
- /gcn.py is the implementation of our neural network
- /dataset.py loads the dataset

## Usage

> python main.py
