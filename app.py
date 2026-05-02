import streamlit as st
import google.generativeai as genai
import time

# --- PENGATURAN HALAMAN & WARNA SEWUADS ---
st.set_page_config(page_title="SewuAds - AI Storyboard", page_icon="🎬")

st.markdown("""
    <style>
    .stButton>button {
        background-color: #4F46E5; /* Deep Indigo */
        color: white;
        border-radius: 8px;
        font-weight: bold;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #FACC15; /* Electric Yellow */
        color: black;
    }
    </style>
""", unsafe_allow_html=True)

# --- SETUP API KEY ---
# API Key diambil dari brankas rahasia Streamlit (Advanced Settings)
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash')
except:
    st.warning("⚠️ API Key belum dimasukkan di menu Advanced Settings Streamlit.")

# --- LOGIKA PINDAH HALAMAN (STATE) ---
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'data' not in st.session_state:
    st.session_state.data = {}

def lanjut():
    st.session_state.step += 1

def reset():
    st.session_state.step = 1
    st.session_state.data = {}

# --- TAMPILAN APLIKASI ---
st.title("🎬 SewuAds Pringsewu")
st.write("Bikin Iklan Sinematik dari Foto Produk Biasa - GRATIS untuk UMKM 🇮🇩")
st.markdown("---")

# HALAMAN 1: INFO PRODUK
if st.session_state.step == 1:
    st.subheader("Step 1: Info Produk")
    nama = st.text_input("Nama Produk", placeholder="Contoh: Kripik Pisang Susanti")
    kategori = st.selectbox("Kategori", ["Makanan & Minuman", "Fashion", "Skincare", "Kerajinan", "Lainnya"])
    
    if st.button("Lanjut ➔"):
        if nama:
            st.session_state.data['nama'] = nama
            st.session_state.data['kategori'] = kategori
            lanjut()
        else:
            st.error("Nama produk harus diisi ya!")

# HALAMAN 2: SETUP IKLAN
elif st.session_state.step == 2:
    st.subheader("Step 2: Setup Iklan")
    mood = st.selectbox("Gaya / Mood Iklan", ["Premium & Elegan", "Ceria & Enerjik", "Hangat & Emosional", "Natural"])
    durasi = st.radio("Durasi Video", ["15 Detik (Cepat)", "30 Detik (Standar)"], horizontal=True)
    
    if st.button("✨ Generate Storyboard Sekarang"):
        st.session_state.data['mood'] = mood
        st.session_state.data['durasi'] = durasi
        lanjut()
        st.rerun()

# HALAMAN 3: LOADING & HASIL (RESULT)
elif st.session_state.step == 3:
    st.subheader("Membuat Storyboard...")
    
    with st.spinner('AI sedang meracik ide sinematik untuk produkmu... Tunggu sebentar ya!'):
        # Prompt Rahasia untuk AI
        prompt_sistem = f"""
        Kamu adalah Sutradara Iklan Profesional. Buatkan storyboard iklan untuk produk UMKM ini:
        Nama Produk: {st.session_state.data['nama']}
        Kategori: {st.session_state.data['kategori']}
        Mood Iklan: {st.session_state.data['mood']}
        Durasi: {st.session_state.data['durasi']}

        BERIKAN OUTPUT DALAM FORMAT MARKDOWN SEPERTI INI UNTUK 3 SCENE:
        ### 🎬 Scene [Nomor]
        **Visual:** [Jelaskan apa yang terlihat di kamera]
        **Audio:** [Suara atau musik yang terdengar]
        
        **Prompt Gambar (Copy ke Gemini/ChatGPT):**
        [Tulis prompt bahasa inggris untuk generate gambar, sertakan lighting dan camera angle]
        
        **Prompt Video (Copy ke Kling/Veo):**
        [Tulis prompt bahasa inggris untuk generate video, sertakan pergerakan kamera]
        ---
        """
        
        try:
            # Meminta AI membuat storyboard
            response = model.generate_content(prompt_sistem)
            hasil_ai = response.text
            
            st.success("🎉 Storyboard Berhasil Dibuat!")
            
            # Menampilkan hasil (st.code memunculkan tombol copy otomatis)
            st.markdown(hasil_ai)
            
            st.markdown("---")
            if st.button("🔄 Buat Iklan Baru"):
                reset()
                st.rerun()
                
        except Exception as e:
            st.error("Terjadi kesalahan. Pastikan API Key sudah benar.")