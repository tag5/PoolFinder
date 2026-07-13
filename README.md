# 🏊 PoolFinder : Satellite Pool Detection Dataset Builder

> 🧠 Turning real-estate open data into a deep-learning ready dataset of swimming pools.

## What is this ?

PoolFinder is a small data pipeline designed to build a labeled image dataset for training a deep learning neural network to automatically detect swimming pools in satellite images.
It all starts with the official French open dataset of geolocated property sales and ends with a collection of hand-tagged satellite images.

## 🧩 Architecture

The project is composed of 2 Docker images and 3 shared volumes:

### 🐳 Containers

- **scrapper** reads property sales from the CSV files and downloads a satellite view for each entry.
- **webapp** is a web interface (port 5000) to manually tag the location of swimming pools on each image.

### 📦 Volumes

- **csv** French property sales data (CSV files to be decompressed) from data.gouv.fr
- **images** contains Satellite views fetched by the scrapper for each CSV entry.
- **tagged_images** contains images manually annotated through the webapp, marking pool locations.

## 🚀 Getting Started

### Prerequisites

- 🐳 Docker installed and running
- 📄 CSV files downloaded and **decompressed** from [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/demandes-de-valeurs-foncieres-geolocalisees/) into `./data/csv/`


### 🔨 Build the images

```bash
docker build -t webapp webapp/
docker build -t scrapper scrapper/
```

### ▶️ Run the containers

- Launch the scrapper (fetches satellite images for each CSV entry):

```bash
bashdocker run --rm \
  -v ./data/csv/:/csv \
  -v ./data/images/:/images \
  scrapper
```

- Launch the webapp (tagging interface on port 5000):

```bash
bashdocker run --rm \
  -v ./data/images/:/images \
  -v ./data/tagged_images:/tagged_images \
  -p 5000:5000 \
  webapp
```

Then open your browser at http://localhost:5000 and start tagging !

Happy tagging! 🔖
