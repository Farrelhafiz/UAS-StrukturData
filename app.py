import streamlit as st
import folium
import heapq
from streamlit_folium import folium_static

from algoritma import graph, cari_rute_dijkstra, cari_semua_rute
from peta import koordinat_kota, gambar_peta

# PAGE TITLE
st.set_page_config(page_title="Aplikasi Travel Bus dengan Rute Terpendek & Alternatif", layout="wide")

# Judul
st.title("Aplikasi Penentuan Rute Travel Bus")
st.markdown("Berbasis Python untuk Penentuan Rute Terpendek (Dijkstra) dan Rute Alternatif (DFS)")
st.markdown("-------")


# MAIN APP 
def main():
    with st.sidebar:
        st.header("Parameter Perjalanan")
        kota_list = list(graph.keys())
        
        start = st.selectbox("Kota Asal (Keberangkatan)", kota_list)
        tujuan = st.selectbox("Kota Tujuan (Destinasi)", kota_list)
        
        st.markdown("---")
        # Pilihan tipe pencarian rute
        mode_pencarian = st.radio(
            "Pilih Mode Pencarian:",
            ("Rute Terpendek (Dijkstra)", "Semua Rute Alternatif (DFS)")
        )
        
        cari_button = st.button("Hitung Jalur", type="primary")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Visualisasi Peta")
        peta_placeholder = st.empty()
    
    with col2:
        st.subheader("Hasil Analisis Rute")
        hasil_placeholder = st.empty()
    
    if cari_button:
        if start == tujuan:
            st.warning("Kota asal dan tujuan tidak boleh sama!")
            return
            
        # RUTE TERPENDEK
        if mode_pencarian == "Rute Terpendek (Dijkstra)":
            with st.spinner("Mencari rute terpendek..."):
                rute, total_jarak = cari_rute_dijkstra(start, tujuan)
                
                if rute:
                    hasil_text = f"""
                    ### Rute Terpendek Ditemukan!
                    * **Jalur Terpilih:** {' -> '.join(rute)}
                    * **Total Jarak:** **{total_jarak} KM**
                    * **Jumlah Transit:** {len(rute) -2} kali
                    * **Jumlah Perpindahan Kota:** {len(rute) -1} kali
                
                    """
                    hasil_placeholder.markdown(hasil_text)
                    
                    peta = gambar_peta(rute, semua_rute_mode=False)
                    with peta_placeholder:
                        folium_static(peta, width=700, height=500)
                else:
                    hasil_placeholder.error(f"Tidak ada jalur bus dari {start} ke {tujuan}")
                    
        # SEMUA RUTE 
        else:
            with st.spinner("Mencari semua kemungkinan rute alternatif..."):
                semua_opsi = cari_semua_rute(start, tujuan)
                
                if semua_opsi:
                    # ni gw urutin rute dari yang terpendek ke terpanjang 
                    semua_opsi.sort(key=lambda x: x[1])
                    
                    hasil_text = f"### Ditemukan {len(semua_opsi)} Rute dari {start} ke {tujuan}:\n\n"
                    for idx, (rute, jarak) in enumerate(semua_opsi):
                        
                        opsi_label = "(Rute Terpendek)" if idx == 0 else f"(Rute Alternatif {idx+1})"
                        hasil_text += f"**{opsi_label}**\n"
                        hasil_text += f"* Jalur: {'  -> '.join(rute)}\n"
                        hasil_text += f"* Total Jarak: **{jarak} KM**\n"
                        hasil_text += f"* Jumlah Transit: {len(rute) -2} kali\n"
                        hasil_text += f"* Jumlah Perpindahan Kota: {len(rute) -1} kali\n\n"
                    
                    
                    hasil_placeholder.markdown(hasil_text)
                    
                    peta = gambar_peta(semua_opsi, semua_rute_mode=True)
                    with peta_placeholder:
                        folium_static(peta, width=700, height=500)
                else:
                    hasil_placeholder.error(f"Tidak ada jalur bus sama sekali dari {start} ke {tujuan}")

     #Peta Default               
    else:        
        peta_default = folium.Map(location=[-7.0, 110.0], zoom_start=7)
        for kota, (lat, lon) in koordinat_kota.items():
            folium.Marker([lat, lon], popup=kota).add_to(peta_default)
        with peta_placeholder:
            folium_static(peta_default, width=700, height=500)
        
        hasil_placeholder.info("""Pilih kota asal, tujuan, dan 
                            metode di sidebar,lalu klik 'Hitung Jalur'""")

if __name__ == "__main__":
    main()