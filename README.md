# Drug-Drug Interaction (DDI) API and Analysis

This repository contains the Drug-Drug Interaction (DDI) API and Analysis project, designed to facilitate the exploration and analysis of drug interactions through a RESTful API and interactive Jupyter Notebooks. 

## Overview

The project is divided into four main components:

1. **DDI_API.py**: A FastAPI application providing endpoints to access and manipulate drug interaction data. This Python script offers a streamlined way to query drug interactions, update the dataset, and perform administrative tasks related to drug interaction data management.

2. **DDI RAG.ipynb**: A Jupyter Notebook for analyzing drug interaction data. This notebook includes code to load, process, and visualize drug interaction information, offering insights into the complexity and nuances of drug interactions.
3. **Testing** : This part includes unit testing and Load Testing of FastAPI. Files are - LoadTesting_locust.py, Unit_test.py
4. **User Interface** : This includes a search function where user can pass the prompt and it returns the results from chromdb. The files under it are - App.js, app.cs, ResultsDisplay.js, QueryForm.js

## Features

- **FastAPI Backend**: A RESTful API to query drug interaction data efficiently.
- **Data Analysis**: Tools and visualizations for understanding drug interactions.
- **Interactive Exploration**: Jupyter Notebook for hands-on data exploration.

## Getting Started

### Prerequisites

- Python 3.8+
- FastAPI
- Uvicorn (for serving the API)
- Jupyter Notebook or JupyterLab

### Installation

1. Clone the repository:
   ```sh
   git clone <repository-url>
   ```
2. Install the required Python packages:
   ```sh
   pip install fastapi uvicorn jupyterlab
   ```

### Running the API

Navigate to the project directory and run:
```sh
uvicorn DDI_API:app --reload
```
This command will start the FastAPI server, making the API accessible on `localhost:8000`.

### Exploring the Notebook

Open the Jupyter Notebook `DDI RAG.ipynb` in JupyterLab or Jupyter Notebook to start your exploration:
```sh
jupyter lab DDI RAG.ipynb
```
or
```sh
jupyter notebook DDI RAG.ipynb
```

## Contributing

Contributions are welcome! Please feel free to submit pull requests, report bugs, and suggest features.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
