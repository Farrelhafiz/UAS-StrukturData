import heapq

# Directed Graph
graph = {
    "Jakarta": [("Bandung", 150), ("Bogor", 60), ("Yogyakarta",210)],
    "Bandung": [ ("Cirebon", 125), ("Semarang", 450)],
    "Surabaya": [("Semarang", 330), ("Malang", 90)],
    "Semarang": [ ("Cirebon", 300), ("Yogyakarta", 120)],
    "Yogyakarta": [("Bandung", 270), ("Malang", 150)],
    "Malang": [("Bogor", 90), ("Jakarta", 350)],
    "Bogor": [("Bandung", 100)],
    "Cirebon": [("Jakarta", 180), ("Yogyakarta", 120)],
}

# Algoritma Dijkstra (Shortest Path) 
def cari_rute_dijkstra(start, goal):
    if start not in graph or goal not in graph:
        return None, 0
    
    # pq = priority queue 
    pq = [(0, start, [start])]
    jarak_terpendek = {kota: float('inf') for kota in graph}
    jarak_terpendek[start] = 0
    
    while pq:
        jarak_saat_ini, kota, rute = heapq.heappop(pq)
        
        if kota == goal:
            return rute, jarak_saat_ini
        
        if jarak_saat_ini > jarak_terpendek[kota]:
            continue
        
        for tetangga, bobot in graph.get(kota, []):
            jarak_baru = jarak_saat_ini + bobot
            if jarak_baru < jarak_terpendek[tetangga]:
                jarak_terpendek[tetangga] = jarak_baru
                heapq.heappush(pq, (jarak_baru, tetangga, rute + [tetangga]))
    
    return None, 0


#Cari semua rute

def cari_semua_rute(start, goal, path=[], total_dist=0):
    path = path + [start]
    
    if start == goal:
        return [(path, total_dist)]
        
    if start not in graph:
        return []
        
    paths = []
    for tetangga, jarak in graph[start]:
        if tetangga not in path:
            new_paths = cari_semua_rute(tetangga, goal, path, total_dist + jarak)
            for p in new_paths:
                paths.append(p)
                
    return paths