# Metro de londres - Algortimos de Procura
## Grupo 15 - Estrutura de dados e Algoritmos 2025/2026

## Estrutura dos ficheiros
```bash 

Grupo15/
├── README.md
├── Graph.py
├── london_network.py
├── main.py
├── london_metro.html
├── london_path_curto_uniform.html
├── london_path_curto_distance.html
├── london_path_longo_uniform.html
├── london_path_longo_distance.html
├── london_path_transbordos_uniform.html
├── london_path_transbordos_distance.html
├── london_mst_uniform.html
├── london_mst_distance.html
└── data/
    ├── stations.csv
    ├── connections.csv
    ├── lines.csv

```

## Descrição dos Ficheiros

- `main.py` -> ficheiro principal para executar o projeto
- `london_network.py` -> classe LondonNetworkGraph com implementação do grafo, algoritmos de Dijkstra, Kruskal e visualizações
- `Graph.py` -> implementação do TAD Grafo (Vertex, Edge, Graph). Foi também adicionado o método público iter_vertex() para permitir iteração sem aceder a métodos protegidos
- `data\` -> pasta com os ficheiros de dados CSV


## Como executar

Instalar dependências:
pip install numpy folium networkx

Executar o projeto:
py main.py

## Outputs Gerados
- `london_metro.html` -> mapa interativo da rede do metro de Londres completa 
- `london_path_curto_uniform.html` -> trajeto curto com custo uniforme
- `london_path_curto_distance.html`-> trajeto curto com custo por distância
- `london_path_longo_uniform.html` -> trajeto longo com custo uniforme 
- `london_path_longo_distance.html`-> trajeto longo com custo por distância
- `london_path_transbordos_uniform.html` -> múltiplos transbordos com custo uniforme
- `london_path_transbordos_distance.html` -> múltiplos transbordos com custo por distância
- `london_mst_uniform.html` -> MST com custo uniforme
- `london_mst_distance.html` -> MST com custo por distância