# Shortest Path Algorithms: Dijkstra and Bellman-Ford Comparison

## Description

This project implements and analyzes the performance of two classic shortest path algorithms: Dijkstra's algorithm and the Bellman-Ford algorithm. [cite: 1, 4] The algorithms are implemented in Python and tested using real-world GTFS (General Transit Feed Specification) data from the Tadao transport network. [cite: 6, 7, 8]

The primary goals of this project are:
* To implement Dijkstra's algorithm with two different priority queue structures: a binary heap and a Fibonacci heap. [cite: 5]
* To implement the Bellman-Ford algorithm. [cite: 1]
* To conduct a theoretical complexity analysis of each algorithm.
* To perform an empirical analysis of the algorithms' performance using the Tadao GTFS dataset, comparing their execution times. [cite: 6, 28, 31]
* To determine the most efficient algorithm for finding the shortest paths within the context of the Tadao transport network. [cite: 43]

## Project Structure
```
.
├── algorithme.py       # Python script with algorithm implementations
├── report.pdf          # Detailed project report with analysis and results
├── tadao/              # Directory containing GTFS data for the Tadao network
│   ├── routes.txt      # Information about transit routes 
│   ├── stop_times.txt  # Arrival and departure times for stops 
│   ├── stops.txt       # Information about transit stops 
│   └── trips.txt       # Information about individual trips 
└── README.md           # This file
```
## Data

The project utilizes GTFS data from the Tadao public transport network. [cite: 7, 8] This dataset was obtained from data.gouv.fr. [cite: 7] The data files describe the transport network, including stops, routes, trip schedules, and stop times. [cite: 8] This data is used to construct a weighted graph where stops are vertices and connections between stops (with travel times as weights) are edges. [cite: 9]

The following files are used from the GTFS dataset:
* `stops.txt`: Contains information about individual stops. [cite: 8, 10]
* `stop_times.txt`: Contains arrival and departure times for each stop in a trip. [cite: 8, 10]
* `trips.txt`: Contains information about individual transit trips. [cite: 8, 10]
* `routes.txt`: Contains information about transit lines/routes. [cite: 8, 10]

The data is loaded and preprocessed using the pandas library in Python. [cite: 10]

## Algorithms Implemented

1.  **Dijkstra's Algorithm**:
    * Implemented with a binary heap for the priority queue. [cite: 1, 5, 13, 16, 17]
    * Implemented with a Fibonacci heap for the priority queue. [cite: 1, 5, 18, 23, 24]
2.  **Bellman-Ford Algorithm**:
    * Implemented as described in the project report. [cite: 1, 25, 26]

## How to Run

1.  **Prerequisites**: Ensure you have Python installed. You will likely need the `pandas` library for data processing. [cite: 10]
    ```bash
    pip install pandas
    ```
2.  **Data**: Place the `tadao` folder containing the GTFS `.txt` files (`routes.txt`, `stop_times.txt`, `stops.txt`, `trips.txt`) in the same directory as `algorithme.py`. [cite: 10]
3.  **Execute**: Run the Python script:
    ```bash
    python algorithme.py
    ```
    The script will likely load the GTFS data, build the graph, and then run the implemented shortest path algorithms, possibly outputting performance metrics or shortest path results as described in the `report.pdf`. [cite: 28, 29, 39, 40]

## Report

A comprehensive analysis of the algorithms, their implementations, theoretical complexity, and empirical performance results on the Tadao dataset can be found in `report.pdf`. [cite: 1, 4, 28, 30, 31, 32, 33, 36, 38, 41, 42] The report discusses the construction of the graph from GTFS data[cite: 9, 10, 12], the implementation details of Dijkstra's algorithm (with both binary and Fibonacci heaps)[cite: 13, 16, 17, 18, 23, 24], and the Bellman-Ford algorithm[cite: 25, 26]. It also includes a comparison of their execution times and practical applications. [cite: 30, 31, 39]

## Dependencies

* Python 3.x
* pandas (for loading and preprocessing GTFS data [cite: 10])
