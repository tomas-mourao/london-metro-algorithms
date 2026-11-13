# London Metro – Graph Search Algorithms

Graph model of the London Underground network with shortest-path search (**Dijkstra**), minimum spanning tree (**Kruskal**) and interactive map visualizations.

> **Course:** Data Structures and Algorithms · BSc in Data Science, ISCTE · Year 1, Semester 2 · Group 15 (2025/2026)

## Features
- Builds the metro network as a graph from CSV data (stations, lines and connections).
- Network statistics: number of stations and connections, mean degree, mean distance (Haversine).
- **Dijkstra** shortest path, both a custom implementation and NetworkX for comparison, with two cost types:
  - *uniform* – every connection costs the same
  - *distance* – cost is the distance in km between stations
- Counts line changes along a route.
- **Kruskal** minimum spanning tree with a Union-Find structure.
- Interactive maps with Folium.

## Tech stack
Python · NumPy · NetworkX · Folium

## How to run
```bash
pip install numpy folium networkx
python main.py
```

## Project structure
```
.
├── main.py              # Entry point
├── london_network.py    # LondonNetworkGraph: graph, Dijkstra, Kruskal and visualizations
├── Graph.py             # Graph ADT (Vertex, Edge, Graph)
├── report.pdf           # Project report (Portuguese)
├── data/
│   ├── stations.csv
│   ├── connections.csv
│   └── lines.csv
└── *.html               # Generated interactive maps
```

## Generated outputs
| File | Description |
|------|-------------|
| `london_metro.html` | Full London metro network |
| `london_path_curto_uniform.html` / `_distance.html` | Short route (uniform / distance cost) |
| `london_path_longo_uniform.html` / `_distance.html` | Long route (uniform / distance cost) |
| `london_path_transbordos_uniform.html` / `_distance.html` | Route with multiple line changes (uniform / distance cost) |
| `london_mst_uniform.html` / `_distance.html` | Minimum spanning tree (uniform / distance cost) |
