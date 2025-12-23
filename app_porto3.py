import streamlit as st
import pandas as pd
from collections import Counter

# ============================
# 1. PAGE CONFIGURATION
# ============================
st.set_page_config(
    page_title="E-commerce Product Category Recommender",
    layout="wide"
)

# Header
st.markdown(
    "<h1 style='text-align: center;'>🛒 E-commerce Product Category Recommendation System</h1>",
    unsafe_allow_html=True
)

st.markdown(
    """
Aplikasi ini memberikan rekomendasi **kategori produk** untuk pengguna e-commerce  
berdasarkan kemiripan profil mereka (minat dan kategori produk favorit).

Silakan pilih **User ID**, lalu aplikasi akan menampilkan:
- Profil singkat pengguna
- Rekomendasi kategori produk beserta proporsinya
- Daftar pengguna lain yang paling mirip sebagai penjelasan (explainability)
"""
)

st.write("---")

# ============================
# 2. LOAD DATA
# ============================
@st.cache_data
def load_data():
    users = pd.read_csv("users_clean.csv")
    sim = pd.read_csv("user_similarity.csv", index_col=0)
    return users, sim

df_users, user_similarity_df = load_data()

# ============================
# 3. RECOMMENDER FUNCTIONS
# ============================
def recommend_top_categories_for_user(user_id, df_users, sim_df,
                                      top_k_neighbors=5, top_n_cats=3):
    """
    Menghasilkan daftar kategori produk yang direkomendasikan untuk satu user
    berdasar kategori favorit user-user lain yang paling mirip.
    """
    if user_id not in sim_df.index:
        return pd.DataFrame()
    
    sims = sim_df.loc[user_id].drop(user_id, errors="ignore")
    neighbors = sims.sort_values(ascending=False).head(top_k_neighbors)
    neighbor_ids = neighbors.index

    neighbor_rows = df_users[df_users['User_ID'].isin(neighbor_ids)]
    cats = neighbor_rows['Product_Category_Preference']

    if cats.empty:
        return pd.DataFrame()

    counts = Counter(cats)
    total = sum(counts.values())

    data = []
    for cat, cnt in counts.most_common(top_n_cats):
        data.append({
            "Category": cat,
            "Neighbor_Count": cnt,
            "Proportion": round(cnt / total, 3)
        })

    return pd.DataFrame(data), neighbors


def explain_recommendation(user_id, df_users, sim_series, top_k_neighbors=5):
    """
    Mengembalikan daftar user tetangga paling mirip beserta
    similarity score dan kategori favorit mereka.
    """
    neighbors = sim_series.sort_values(ascending=False).head(top_k_neighbors)
    neighbor_ids = neighbors.index

    neighbor_rows = df_users[df_users['User_ID'].isin(neighbor_ids)].copy()
    neighbor_rows = neighbor_rows[[
        'User_ID','Age','Gender','Location','Interests',
        'Product_Category_Preference'
    ]]
    neighbor_rows['Similarity'] = neighbor_rows['User_ID'].map(neighbors)
    return neighbor_rows.sort_values('Similarity', ascending=False)


# ============================
# 4. SIDEBAR – FILTER & PARAMETER
# ============================
st.sidebar.header("⚙️ Pengaturan")

user_ids = df_users['User_ID'].unique()
selected_user = st.sidebar.selectbox("Pilih User ID", user_ids)

top_k_neighbors = st.sidebar.slider("Jumlah tetangga (K)", 3, 30, 10)
top_n_cats = st.sidebar.slider("Jumlah kategori rekomendasi", 1, 5, 3)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "Dataset: 1000 pengguna dengan informasi demografis, perilaku belanja, "
    "minat, dan kategori produk favorit."
)


# ============================
# 5. MAIN LAYOUT
# ============================
col_left, col_right = st.columns([1.1, 1.3], gap="large")

# -------- LEFT: PROFILE & BEHAVIOR --------
with col_left:
    st.subheader("📌 Profil Pengguna")

    user_profile = df_users[df_users['User_ID'] == selected_user].iloc[0]

    # Tampilkan info dalam dua kolom
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"**User ID:** {user_profile['User_ID']}")
        st.markdown(f"**Gender:** {user_profile['Gender']}")
        st.markdown(f"**Age:** {user_profile['Age']}")
        st.markdown(f"**Location:** {user_profile['Location']}")
        st.markdown(f"**Income:** {user_profile['Income']}")
    with c2:
        st.markdown(f"**Interests:** {user_profile['Interests']}")
        st.markdown(
            f"**Fav Category:** {user_profile['Product_Category_Preference']}"
        )
        st.markdown(
            f"**Purchase Freq.:** {user_profile['Purchase_Frequency']}"
        )
        st.markdown(
            f"**Total Spending:** {user_profile['Total_Spending']}"
        )
        st.markdown(
            f"**Pages Viewed:** {user_profile['Pages_Viewed']}"
        )

    st.write("---")
    st.markdown(
        """
**Catatan:**  
Kategori favorit saat ini berasal dari kolom `Product_Category_Preference`.  
Model akan melihat pengguna lain dengan minat dan kategori yang mirip
untuk menyarankan kategori tambahan yang potensial.
"""
    )

# -------- RIGHT: RECOMMENDATIONS & EXPLANATION --------
with col_right:
    st.subheader("⭐ Rekomendasi Kategori Produk")

    # Hitung rekomendasi
    sims = user_similarity_df.loc[selected_user].drop(selected_user, errors="ignore")
    rec_df, neighbors_sim = recommend_top_categories_for_user(
        selected_user, df_users, user_similarity_df,
        top_k_neighbors=top_k_neighbors, top_n_cats=top_n_cats
    )

    if rec_df.empty:
        st.warning("Belum ada rekomendasi untuk user ini.")
    else:
        # Tampilkan hasil dalam bentuk tabel dengan highlight
        st.dataframe(rec_df, use_container_width=True)

    st.write("---")
    st.subheader("👥 Tetangga Paling Mirip (Penjelasan)")

    explain_df = explain_recommendation(
        selected_user, df_users, sims,
        top_k_neighbors=top_k_neighbors
    )

    st.dataframe(explain_df, use_container_width=True)

    st.markdown(
        """
Keterangan:  
User dengan nilai **Similarity** tinggi memiliki profil minat dan kategori
produk yang mirip dengan pengguna terpilih.  
Kategori yang paling sering muncul di antara tetangga inilah yang menjadi
dasar rekomendasi di tabel atas.
"""
    )
