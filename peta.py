import folium


# DATA PETA (GRAPH) DENGAN KOORDINAT 
koordinat_kota = {
    "Jakarta": [-6.2088, 106.8456],
    "Bandung": [-6.9175, 107.6191],
    "Surabaya": [-7.2575, 112.7521],
    "Semarang": [-6.9932, 110.4203],
    "Yogyakarta": [-7.7956, 110.3695],
    "Malang": [-7.9797, 112.6304],
    "Bogor": [-6.5971, 106.8060],
    "Cirebon": [-6.7320, 108.5523],
}


# GAMBAR PETA MULTI RUTE 
def gambar_peta(rute_pilihan, semua_rute_mode=False):
    # Titik Kota
    if semua_rute_mode and rute_pilihan:
        pusat = koordinat_kota[rute_pilihan[0][0][0]]
    elif rute_pilihan:
        pusat = koordinat_kota[rute_pilihan[0]]
    else:
        return None
    peta = folium.Map(location=pusat, zoom_start=7)
    
    # Warna rute alternatif
    warna_list = ["blue", "purple", "orange", "green", "magenta", "cadetblue"]

    if semua_rute_mode:
        # Loop semua rute alternatif yang udh ditemuin
        for idx, (rute, jarak) in enumerate(rute_pilihan):
            warna = warna_list[idx % len(warna_list)]
            koordinat_rute = [koordinat_kota[kota] for kota in rute if kota in koordinat_kota]
            
            # Gambar garis rute
            if len(koordinat_rute) > 1:
                folium.PolyLine(
                    koordinat_rute, 
                    color=warna, 
                    weight=4, 
                    opacity=0.8, 
                    tooltip=f"Alternatif {idx+1}: {jarak} km"
                ).add_to(peta)
                
            # marker khusus tiap kota di dalam rute
            for kota in rute:
                folium.Marker(
                    location=koordinat_kota[kota],
                    popup=f"{kota} (Rute {idx+1})",
                    icon=folium.Icon(color=warna, icon="info-sign")
                ).add_to(peta)
                
    # Mode Rute Tunggal (Dijkstra)                
    else:    
        koordinat_rute = [koordinat_kota[kota] for kota in rute_pilihan if kota in koordinat_kota]
        if len(koordinat_rute) > 1:
            folium.PolyLine(koordinat_rute, color="red", weight=5, opacity=0.9, tooltip="Rute Terpendek").add_to(peta)
        
        for kota in rute_pilihan:
            folium.Marker(
                location=koordinat_kota[kota],
                popup=kota,
                icon=folium.Icon(color="red", icon="info-sign")
            ).add_to(peta)
            
    return peta