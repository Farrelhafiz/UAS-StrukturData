import folium
import requests


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
def ambil_koordinat_jalan(lat1, lon1, lat2, lon2):
    url = (
        f"https://router.project-osrm.org/route/v1/driving/"
        f"{lon1},{lat1};{lon2},{lat2}"
        "?overview=full&geometries=geojson"
    )

    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()

            if data["code"] == "Ok":
                koordinat = data["routes"][0]["geometry"]["coordinates"]

                # OSRM menghasilkan [lon, lat]
                return [[lat, lon] for lon, lat in koordinat]

    except Exception:
        pass

    # fallback jika API gagal
    return [
        [lat1, lon1],
        [lat2, lon2]
    ]

# jarak peta real time dari kota ke kota
def ambil_jarak_real(lat1, lon1, lat2, lon2):
    url = (
        f"https://router.project-osrm.org/route/v1/driving/"
        f"{lon1},{lat1};{lon2},{lat2}"
        "?overview=false"
    )
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data["code"] == "Ok":
                # Konversi meter ke KM
                jarak_meter = data["routes"][0]["distance"]
                return round(jarak_meter / 1000) 
    except Exception:
        pass
    
    return None


# GAMBAR PETA MULTI RUTE 
def gambar_peta(rute_pilihan, semua_rute_mode=False):
    # Ini buat nentuin titik pusat peta berdasarkan kota pertama yang ditemukan yee
    if semua_rute_mode and rute_pilihan:
        pusat = koordinat_kota[rute_pilihan[0][0][0]]
    elif rute_pilihan:
        pusat = koordinat_kota[rute_pilihan[0]]
    else:
        return None

    peta = folium.Map(location=pusat, zoom_start=7)
    
    # Warna yang dipakai kalau nampilin banyak rute alternatif
    warna_list = ["blue", "purple", "orange", "green", "magenta", "cadetblue"]

    if semua_rute_mode:
        # kalo ini buat Loop semua rute alternatif yang udh ditemuin
        for idx, (rute, jarak) in enumerate(rute_pilihan):
            warna = warna_list[idx % len(warna_list)]
            for i in range(len(rute)-1):

                kota_awal = rute[i]
                kota_tujuan = rute[i+1]

                lat1, lon1 = koordinat_kota[kota_awal]
                lat2, lon2 = koordinat_kota[kota_tujuan]

                jalur_jalan = ambil_koordinat_jalan(
                    lat1,
                    lon1,
                    lat2,
                    lon2
                )

                folium.PolyLine(
                    jalur_jalan,
                    color=warna,
                    weight=6,
                    opacity=0.9,
                    tooltip=f"Alternatif {idx+1} ({jarak} km)"
                ).add_to(peta)
                
            # marker khusus tiap kota di dalam rute(biar ga bingung lu pada bedain warnanya)
            for kota in rute:
                folium.Marker(
                    location=koordinat_kota[kota],
                    popup=f"{kota} (Rute {idx+1})",
                    icon=folium.Icon(color=warna, icon="info-sign")
                ).add_to(peta)
    else:
        # Mode Rute Tunggal (Dijkstra)
        for i in range(len(rute_pilihan)-1):

            kota_awal = rute_pilihan[i]
            kota_tujuan = rute_pilihan[i+1]

            lat1, lon1 = koordinat_kota[kota_awal]
            lat2, lon2 = koordinat_kota[kota_tujuan]

            jalur_jalan = ambil_koordinat_jalan(
                lat1,
                lon1,
                lat2,
                lon2
            )

            folium.PolyLine(
                jalur_jalan,
                color="red",
                weight=7,
                opacity=0.9,
                tooltip="Rute Terpendek"
            ).add_to(peta)
        
        for kota in rute_pilihan:
            folium.Marker(
                location=koordinat_kota[kota],
                popup=kota,
                icon=folium.Icon(color="red", icon="info-sign")
            ).add_to(peta)
            
    return peta