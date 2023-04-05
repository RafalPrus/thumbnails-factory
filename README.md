# thumbnails-factory
A tool used for generating thumbnail images in directories, participating in part of the process of preparing and adding products to a website.

[![Python Version](https://img.shields.io/badge/python-3.10.6-blue.svg)](https://www.python.org/downloads/release/python-3.10.6/)

## Getting Started
To use this tool, you will need to have Python 3.6 or higher installed on your system. Once you have those installed, clone this repository by running the following command in your terminal
```bash
git clone https://github.com/RafalPrus/thumbnails-factory.git
```
Then, install all necessary dependencies with:
```bash
pip install -r requirements.txt
```

## Usage
To use the application, first upload the directories with photos for which you want to create thumbnails to the 'images' folder. Upon launching the program, it will automatically create a new folder named 'small' in each directory, where it will place the generated thumbnails for each photo in the folder. To run the program and create thumbnails, simply launch main.py and select the appropriate option from the displayed menu.

## Statistic feature
The application can store detailed statistics about the created thumbnails if you place an info.txt file in each product folder, which will contain the first line with the product category name, and the second line with the product number, for example:
```bash
CARS
23923
```
You can select the option to display statistics from the application menu. If the product folder does not have an info.txt file with information about the product, the application will store only basic information about the created thumbnails for products: the number of products for which thumbnails were created during a given time.
