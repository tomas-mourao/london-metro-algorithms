import time
from london_network import LondonNetworkGraph

metro = LondonNetworkGraph()
metro.stations("data/stations.csv")
metro.colour_lines("data/lines.csv")
metro.connections("data/connections.csv")

print("Nº de estações:", metro.n_stations())
print("Nº de ligações:", metro.n_edges())
print("Grau médio:", metro.mean_degree())
print("Distância média (km):", metro.mean_weight())

# ============ TRAJETO CURTO - Baker Street → Bond Street ============
# Dijkstra NX - uniform
start = time.time()
G, path, cost, n, changes = metro.dijkstra_nx(11, 28, weight_type='uniform')
t = time.time() - start
metro.processar_e_exibir_resultado(path, cost, t, "Dijkstra NX - Uniforme - Trajeto Curto")
metro.visualize_path(path, 'london_path_curto_uniform.html')

# Dijkstra NX - distance
start = time.time()
G, path, cost, n, changes = metro.dijkstra_nx(11, 28, weight_type='distance')
t = time.time() - start
metro.processar_e_exibir_resultado(path, cost, t, "Dijkstra NX - Distância - Trajeto Curto")
metro.visualize_path(path, 'london_path_curto_distance.html')

# Dijkstra Próprio - uniform
start = time.time()
path, cost, n, changes = metro.dijkstra_proprio(11, 28, weight_type='uniform')
t = time.time() - start
metro.processar_e_exibir_resultado(path, cost, t, "Dijkstra Próprio - Uniforme - Trajeto Curto")

# ============ TRAJETO LONGO - Heathrow → Stratford ============
# Dijkstra NX - uniform
start = time.time()
G, path, cost, n, changes = metro.dijkstra_nx(117, 247, weight_type='uniform')
t = time.time() - start
metro.processar_e_exibir_resultado(path, cost, t, "Dijkstra NX - Uniforme - Trajeto Longo")
metro.visualize_path(path, 'london_path_longo_uniform.html')

# Dijkstra NX - distance
start = time.time()
G, path, cost, n, changes = metro.dijkstra_nx(117, 247, weight_type='distance')
t = time.time() - start
metro.processar_e_exibir_resultado(path, cost, t, "Dijkstra NX - Distância - Trajeto Longo")
metro.visualize_path(path, 'london_path_longo_distance.html')

# Dijkstra Próprio - uniform
start = time.time()
path, cost, n, changes = metro.dijkstra_proprio(117, 247, weight_type='uniform')
t = time.time() - start
metro.processar_e_exibir_resultado(path, cost, t, "Dijkstra Próprio - Uniforme - Trajeto Longo")

# ============ MÚLTIPLOS TRANSBORDOS - Wimbledon → Canary Wharf ============
# Dijkstra NX - uniform
start = time.time()
G, path, cost, n, changes = metro.dijkstra_nx(299, 42, weight_type='uniform')
t = time.time() - start
metro.processar_e_exibir_resultado(path, cost, t, "Dijkstra NX - Uniforme - Múltiplos Transbordos")
metro.visualize_path(path, 'london_path_transbordos_uniform.html')

# Dijkstra NX - distance
start = time.time()
G, path, cost, n, changes = metro.dijkstra_nx(299, 42, weight_type='distance')
t = time.time() - start
metro.processar_e_exibir_resultado(path, cost, t, "Dijkstra NX - Distância - Múltiplos Transbordos")
metro.visualize_path(path, 'london_path_transbordos_distance.html')

# Dijkstra Próprio - uniform
start = time.time()
path, cost, n, changes = metro.dijkstra_proprio(299, 42, weight_type='uniform')
t = time.time() - start
metro.processar_e_exibir_resultado(path, cost, t, "Dijkstra Próprio - Uniforme - Múltiplos Transbordos")

# Kruskal
metro.simular_e_documentar_kruskal(tipo_custo='uniform')
metro.simular_e_documentar_kruskal(tipo_custo='distance')

metro.visualize("london_metro.html")