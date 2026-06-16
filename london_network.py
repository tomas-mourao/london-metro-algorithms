"""
Módulo responsável pela modelação, análise e visualização da rede do Metro de Londres.
Implementa algoritmos de procura e otimização (Dijkstra e Kruskal) aplicados à infraestrutura de transportes
"""

import csv
import numpy as np
import folium as fl
from Graph import Graph


class LondonNetworkGraph:
    def __init__(self):
        """
        Estrutura do grafo (lista de adjacências) e os dicionários auxiliares
        """
        self._stations = {} #guarda informação das estações
        self._graph = Graph()    # lista de adjacências
        self._edges = []
        self._lines = {}
        self._lines_info = {}

    def colour_lines(self, filename = "lines.csv"):
        """
        Importa as linhas a partir do ficheiro CSV
        """
        with open(filename, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                line_id = int(row['line'])
                self._lines_info[line_id] = {
                    'name': row['name'],
                    'colour': '#' + row['colour'],
                }

    def stations(self, filename = 'stations.csv'):
        """
        Importa as estações a partir do ficheiro CSV, incluindo todos os
        atributos relevantes (id, nome, latitude, longitude)
        """
        with open(filename, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                station_id = int(row['id'])
                self._stations[station_id] = {
                    'name': row['name'],
                    'latitude': float(row['latitude']),
                    'longitude': float(row['longitude'])
                }
                self._graph.add_vertex(station_id, payload={
                    'name' : row['name'],   # chave : valor
                    'latitude' : float(row['latitude']),
                    'longitude' : float(row['longitude'])
                })    # cria lista vazia no grafo

    def connections(self, filename = "connections.csv"):
        """
        Importa as ligações entre estações
        """
        with open(filename, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                station1 = int(row["station1"])
                station2 = int(row["station2"])
                line = int(row["line"])
                if line not in self._lines:
                    self._lines[line] = 0
                self._lines[line] += 1
                edge_info = {'line': line}
                self._graph.add_edge(station1, station2,payload=line, weight=1)
                self._edges.append((station1, station2, edge_info))

    def n_stations(self):
        """
        Devolve o número total de estações
        """
        return len(self._stations)

    def n_edges(self):
        """
        Devolve o número total de ligações
        """
        return len(self._edges)

    def n_edges_line(self):
        """
        Devolve o número de ligações por linha
        """
        return self._lines

    def mean_degree(self):
        """
        calcula o grau medio das estações
        """
        total = 0
        for station in self._graph.iter_vertex():
            total += self._graph.degree(station)
        return round(total / self.n_stations(), 2)

    def _haversine(self, station1, station2):
        """
        Calcula a distância geográfica em km entre duas estações pela fórmula de Haversine
        """
        r = 6371
        lat1 = np.radians(self._stations[station1]['latitude'])
        lat2 = np.radians(self._stations[station2]['latitude'])
        lon1 = np.radians(self._stations[station1]['longitude'])
        lon2 = np.radians(self._stations[station2]['longitude'])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a  = (np.sin(dlat / 2)) ** 2 + np.cos(lat1) * np.cos(lat2) * (np.sin(dlon/ 2 )) ** 2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
        return round(float(c * r) , 3)

    def mean_weight(self):
        """
        Calcula o peso médio das arestas
        """
        if not self._edges:
            return 0
        distancia = 0
        for station1,station2,_ in self._edges:
            distancia += self._haversine(station1, station2)
        return round(distancia / len(self._edges) , 2)

    def _count_changes(self, path):
        """
        contabiliza o número de mudanças de linha efetuadas
        """
        changes = 0
        current_line = None
        for i in range(len(path) - 1):
            s1 = path[i]
            s2 = path[i + 1]
            for st1, st2, edge_info in self._edges:
                if (st1 == s1 and st2 == s2) or (st1 == s2 and st2 == s1):
                    line = edge_info['line']
                    if current_line is not None and line != current_line:
                        changes += 1
                    current_line = line
                    break
        return changes

    def dijkstra_nx(self, origin, destination, weight_type = 'uniform', hora = 8):
        """
        Calcula o caminho mínimo entre duas estações
        """
        import networkx as nx
        G = nx.Graph()
        for station1, station2, edge_info in self._edges:
            if weight_type == 'uniform':
                weight = 1
            elif weight_type == 'distance':
                weight = self._haversine(station1, station2)
            elif weight_type == 'rush_hour':
                dist = self._haversine(station1, station2)
                if 7 < hora < 9 or 17 < hora < 19:
                    fator = 2
                else:
                    fator = 1
                weight = dist * fator
            else:
                weight = 1
            G.add_edge(station1,station2, w = weight)
        path = nx.dijkstra_path(G, origin, destination, weight = 'w')
        cost = nx.dijkstra_path_length(G, origin, destination, weight = 'w')
        changes = self._count_changes(path)
        return G, path, cost, len(path), changes


    def dijkstra_proprio(self, start_id, end_id, weight_type = 'uniform', hora = 8):
        """
        Implementação do algoritmo de Dijkstra com recurso à fila de prioridade (heapq)
        """
        import heapq
        distances = {station: float("inf") for station in self._stations}
        predecessors = {station: None for station in self._stations}
        distances[start_id] = 0
        priority_queue = [(0, start_id)]
        visited = set()
        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)
            #condição de paragem antecipada ao atingir o destino
            if current_node == end_id:
                break
            if current_node in visited:
                continue
            visited.add(current_node)
            for edge in self._graph._graph[current_node]:
                neighbor = edge.opposite(current_node)
                if neighbor in visited:
                    continue
                if weight_type == 'uniform':
                    weight = 1
                elif weight_type == 'distance':
                    weight = self._haversine(current_node, neighbor)
                elif weight_type == 'rush_hour':
                    dist = self._haversine(current_node, neighbor)
                    if 7 < hora < 9 or 17 < hora < 19:
                        fator = 2
                    else:
                        fator = 1
                    weight = dist * fator
                else:
                    weight = 1
                distance =  current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    predecessors[neighbor] = current_node
                    heapq.heappush(priority_queue, (distance, neighbor))
        path = []
        current = end_id
        if distances[end_id] != float("inf"):
            while current is not None:
                path.insert(0, current)
                current = predecessors[current]
        changes = self._count_changes(path)
        return path, distances[end_id], len(path), changes

    def processar_e_exibir_resultado(self, path, cost, execution_time, name):
        """
        Imprime o detalhe formatado das simulações da rota
        """
        if not path:
            print(f"[{name}] Caminho não encontrado.")
            return
        line_change = self._count_changes(path)
        name_sequence =[self._stations[st_id]['name'] for st_id in path]

        print(f"\n" + "=" * 40)
        print(f"{name}")
        print(f"=" * 40)
        print(f"Sequência: {' -> '.join(name_sequence)}")
        print(f"Número total de estações do percurso: {len(path)}")
        print(f"Custo total do caminho: {cost}")
        print(f"Número de mudanças de linha: {line_change}")
        print(f"Tempo de execução: {execution_time:.4f} segundos")
        print(f"=" * 40)

    def obter_custo_aresta(self, s1, s2, line_id, tipo_custo):
        """
        devolve o pese de uma aresta dependendo da função de custo a ser usada
        """
        if tipo_custo == 'uniform':
            return 1
        elif tipo_custo == 'distance':
            return self._haversine(s1,s2)
        else:
            return 1

    def kruskal_mst(self, tipo_custo="uniform"):
        """
        Implementa o algoritmo de Kruskal para obter a árvore geradora mínima (MST)
        """
        mst_edges = []
        total_cost = 0.0
        arestas_com_custo = []
        for s1, s2, edge_info in self._edges:
            line_id = edge_info["line"]
            custo = self.obter_custo_aresta(s1, s2, line_id, tipo_custo)
            arestas_com_custo.append((custo, s1, s2, line_id))
        arestas_com_custo.sort(key=lambda x: x[0])
        uf = UnionFind(self._stations.keys())
        for custo, s1, s2, line_id in arestas_com_custo:
            if uf.union(s1, s2):
                mst_edges.append((s1, s2, {"line": line_id, "weight": custo}))
                total_cost += custo
            if len(mst_edges) == len(self._stations) - 1:
                break
        return mst_edges, round(total_cost, 2)

    def visualizar_mst(self, mst_edges, output_file='london_mst.html'):
        """Gera um mapa destacando a MST sobre a rede original (Secção 4.3)."""
        mapa = fl.Map(location=[51.5074, -0.1278], zoom_start=11, tiles="CartoDB positron")

        # Cria um set com tuplos ordenados para identificar as arestas da MST
        mst_set = set()
        for s1, s2, _ in mst_edges:
            mst_set.add((min(s1, s2), max(s1, s2)))

        # Desenha toda a rede original em fundo (Cinzento, Fina, Opaca)
        for s1, s2, edge_info in self._edges:
            if (min(s1, s2), max(s1, s2)) not in mst_set:
                lat1, lon1 = self._stations[s1]['latitude'], self._stations[s1]['longitude']
                lat2, lon2 = self._stations[s2]['latitude'], self._stations[s2]['longitude']
                fl.PolyLine(
                    locations=[[lat1, lon1], [lat2, lon2]],
                    color="#d1d1d1", weight=1.5, opacity=0.4
                ).add_to(mapa)

        # Desenha as arestas da MST por cima (Coloridas, Grossas)
        for s1, s2, edge_info in mst_edges:
            lat1, lon1 = self._stations[s1]['latitude'], self._stations[s1]['longitude']
            lat2, lon2 = self._stations[s2]['latitude'], self._stations[s2]['longitude']

            line_id = edge_info['line']
            cor = self._lines_info.get(line_id, {}).get('colour', '#2ecc71')
            nome_linha = self._lines_info.get(line_id, {}).get('name', f"Linha {line_id}")

            fl.PolyLine(
                locations=[[lat1, lon1], [lat2, lon2]],
                color=cor, weight=4.5, opacity=0.9,
                tooltip=f"MST - {nome_linha}"
            ).add_to(mapa)

        # Desenhar as Estações
        for station_id, info in self._stations.items():
            fl.CircleMarker(
                location=[info['latitude'], info['longitude']],
                radius=3, color="#2c3e50", fill=True, fill_color="#2c3e50",
                tooltip=info['name']
            ).add_to(mapa)

        mapa.save(output_file)
        print(f"Mapa da MST guardado com sucesso em '{output_file}'")

    def simular_e_documentar_kruskal(self, tipo_custo="uniform"):
        """Calcula, extrai métricas e exibe o relatório da simulação """

        # Calcula custos totais da rede original para termos de comparação
        custo_total_original = sum(
            self.obter_custo_aresta(s1, s2, e['line'], tipo_custo) for s1, s2, e in self._edges
        )

        mst, custo_mst = self.kruskal_mst(tipo_custo)

        print("\n" + "=" * 50)
        print(f" RELATÓRIO DE SIMULAÇÃO MST (Custo: {tipo_custo.upper()})")
        print(f"=" * 50)
        print(f"● Número de arestas da rede original: {len(self._edges)}")
        print(f"● Número de arestas da MST:           {len(mst)}")
        print(f"● Custo total da rede original:       {custo_total_original:.2f}")
        print(f"● Custo total da MST:                 {custo_mst:.2f}")
        print(
            f"● Redução de infraestrutura (Arestas): {((len(self._edges) - len(mst)) / len(self._edges)) * 100:.1f}%")
        print(f"=" * 50)


        self.visualizar_mst(mst, output_file=f"london_mst_{tipo_custo}.html")
        return mst

    def visualize(self, output_file='london_network.html'):
        """
		Gera um mapa interativo da rede do metro de Londres
		"""
        mapa = fl.Map(location=[51.5074, -0.1278], zoom_start=11, tiles="CartoDB positron")

        for station1, station2, edge_info in self._edges:
            lat1 = self._stations[station1]['latitude']
            lon1 = self._stations[station1]['longitude']
            lat2 = self._stations[station2]['latitude']
            lon2 = self._stations[station2]['longitude']

            line_id = edge_info['line']
            cor = self._lines_info.get(line_id, {}).get('colour', '#888888')
            nome_linha = self._lines_info.get(line_id, {}).get('name', str(line_id))

            fl.PolyLine(
                locations=[[lat1, lon1], [lat2, lon2]],
                color=cor,
                weight=2,
                opacity=0.7,
                tooltip=nome_linha
            ).add_to(mapa)

        for station_id, info in self._stations.items():
            degree = self._graph.degree(station_id)
            if degree > 2:
                radius, cor = 6, "#c0392b"
            else:
                radius, cor = 4, "#8e44ad"

            fl.CircleMarker(
                location=[info['latitude'], info['longitude']],
                radius=radius,
                color=cor,
                fill=True,
                fill_color=cor,
                fill_opacity=0.9,
                tooltip=f"<b>{info['name']}</b><br>ID: {station_id}<br>Ligações: {degree}"
            ).add_to(mapa)

        mapa.get_root().html.add_child(fl.Element(self._build_legend()))

        mapa.save(output_file)
        print(f"Mapa guardado em '{output_file}'")
        return mapa

    def visualize_path(self, path, output_file = 'london_path.html'):
        """
        Gera um mapa com o caminho escolhido calculado
        """
        mapa = fl.Map(location=[51.5074, -0.1278], zoom_start=11, tiles="CartoDB positron")

        for station1, station2, edge_info in self._edges:
            lat1, lon1 = self._stations[station1]['latitude'], self._stations[station1]['longitude']
            lat2, lon2 = self._stations[station2]['latitude'], self._stations[station2]['longitude']
            fl.PolyLine(
                locations=[[lat1, lon1], [lat2, lon2]],
                color="#d1d1d1", weight=1.5, opacity=0.4
            ).add_to(mapa)


        for i in range(len(path) - 1):
            s1, s2 = path[i], path[i + 1]
            lat1, lon1 = self._stations[s1]['latitude'], self._stations[s1]['longitude']
            lat2, lon2 = self._stations[s2]['latitude'], self._stations[s2]['longitude']
            fl.PolyLine(
                locations=[[lat1, lon1], [lat2, lon2]],
                color="#e74c3c", weight=5, opacity=0.9
            ).add_to(mapa)

        #gera o índice de partida e chegada
        fl.Marker(
            location=[self._stations[path[0]]['latitude'], self._stations[path[0]]['longitude']],
            tooltip=f"Origem: {self._stations[path[0]]['name']}",
            icon=fl.Icon(color='green')
        ).add_to(mapa)
        fl.Marker(
            location=[self._stations[path[-1]]['latitude'], self._stations[path[-1]]['longitude']],
            tooltip=f"Destino: {self._stations[path[-1]]['name']}",
            icon=fl.Icon(color='red')
        ).add_to(mapa)

        mapa.save(output_file)
        print(f"Mapa do caminho guardado em '{output_file}'")

    def _build_legend(self):
        """
		Constrói o HTML da legenda das linhas do metro
		"""
        items = ""
        for line_id, info in sorted(self._lines_info.items()):
            items += f"""
               <div style="display:flex; align-items:center; margin:3px 0;">
                   <div style="width:28px; height:8px; background:{info['colour']};
                   border-radius:3px; margin-right:8px;"></div>
                   <span style="font-size:11px;">{info['name']}</span>
               </div>"""
        return f"""
           <div style="position:fixed; bottom:30px; left:30px; z-index:1000;
                       background:white; padding:12px 16px; border-radius:8px;
                       box-shadow:2px 2px 8px rgba(0,0,0,0.3);
                       font-family:Arial, sans-serif; max-height:340px; overflow-y:auto;">
               <b style="font-size:13px;">Linhas do Metro</b><br><br>
               {items}
               <hr style="margin:8px 0;">
               <div style="display:flex; align-items:center; margin:3px 0;">
                   <div style="width:28px; height:8px; background:#c0392b;
                   border-radius:3px; margin-right:8px;"></div>
                   <span style="font-size:11px;">Intercâmbio</span>
               </div>
               <div style="display:flex; align-items:center; margin:3px 0;">
                   <div style="width:28px; height:8px; background:#f39c12;
                   border-radius:3px; margin-right:8px;"></div>
                   <span style="font-size:11px;">Estação simples</span>
               </div>
           </div>"""

class UnionFind:
    def __init__(self, elements):
        self.parent = {elem: elem for elem in elements}
        self.rank = {elem: 0 for elem in elements}

    def find(self, i):
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]
    
    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            if self.rank[root_i] > self.rank[root_j]:
                self.parent[root_j] = root_i
            elif self.rank[root_i] < self.rank[root_j]:
                self.parent[root_i] = root_j
            else:
                self.parent[root_j] = root_i
                self.rank[root_i] += 1
            return True
        return False



