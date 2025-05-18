# Shortest Path Algorithms: Dijkstra and Bellman-Ford Comparison

## 📚 Description

This project implements and analyzes the performance of two classic shortest path algorithms: **Dijkstra's algorithm** and the **Bellman-Ford algorithm**. The algorithms are implemented in **Python** and tested using real-world **GTFS (General Transit Feed Specification)** data from the **Tadao** public transport network.

### 🎯 Project Objectives

- Implement Dijkstra's algorithm using:
  - A **binary heap** priority queue
  - A **Fibonacci heap** priority queue
- Implement the **Bellman-Ford algorithm**
- Perform a **theoretical complexity analysis** of each algorithm
- Conduct an **empirical performance comparison** using the Tadao GTFS dataset
- Determine the most efficient algorithm for computing shortest paths in the context of the Tadao network

---

## 🗂️ Project Structure
```
├── algorithme.py # Python script with algorithm implementations
├── report.pdf # Detailed report with analysis and results
├── tadao/ # Directory containing GTFS data
│ ├── routes.txt
│ ├── stop_times.txt
│ ├── stops.txt
│ └── trips.txt
└── README.md # This file
```
---

## 🗃️ Data

The project uses **GTFS data** from the **Tadao** public transport network, available from [data.gouv.fr](https://www.data.gouv.fr/). The data describes the transport network as a **weighted graph** where:

- **Vertices** represent stops
- **Edges** represent connections between stops with **travel time as weight**

### GTFS Files Used

- `stops.txt`: Information about stops
- `stop_times.txt`: Stop arrival and departure times
- `trips.txt`: Trip-level information
- `routes.txt`: Details about transit routes

Data is processed using the **pandas** library.

---

## 🧠 Algorithms Implemented

### Dijkstra's Algorithm

- With **binary heap** priority queue
- With **Fibonacci heap** priority queue

### Bellman-Ford Algorithm

- Classic implementation as described in theoretical literature

---

## 🛠️ How to Run

### Prerequisites

Ensure you have **Python 3.x** and **pandas** installed.

Install pandas:
```bash
pip install pandas
```
Steps
Place the tadao/ folder (with the GTFS files) in the same directory as algorithme.py.

Run the main script:

```bash
python algorithme.py
```
The script will load the GTFS data, construct the graph, and run the shortest path algorithms, printing results or saving performance metrics depending on the implementation.

## 📄 Report
- A complete report is provided in report.pdf, covering:

- Graph construction from GTFS data

- Algorithm implementations (Dijkstra: binary/Fibonacci heaps, Bellman-Ford)

- Theoretical complexity analysis

- Empirical performance comparison on Tadao data

- Real-world application insights

## 📦 Dependencies
Python 3.x

pandas – for loading and preprocessing GTFS data

## 📃 License
This project is provided for educational and research purposes. Free to use, modify, and share under the terms of academic use.

## 🧾 References
References and citations are detailed in the report.pdf.


