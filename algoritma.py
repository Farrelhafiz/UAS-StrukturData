import heapq
from peta import koordinat_kota, ambil_jarak_real

# DIrected Graph
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


# penyesuaian atau sinkronisasi jarak peta
def sinkronisasi_jarak_real():
    for kota_asal, tetangga_list in graph.items():
        new_tetangga = []
        for kota_tujuan, jarak_lama in tetangga_list:
            lat1, lon1 = koordinat_kota[kota_asal]
            lat2, lon2 = koordinat_kota[kota_tujuan]
            
            jarak_real = ambil_jarak_real(lat1, lon1, lat2, lon2)
            
            if jarak_real is not None:
                new_tetangga.append((kota_tujuan, jarak_real))
            else:
                new_tetangga.append((kota_tujuan, jarak_lama))
                
        graph[kota_asal] = new_tetangga

# ini bakal otomatis berjalan saat file algoritma di import oleh app.py
sinkronisasi_jarak_real()