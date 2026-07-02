import streamlit as st
from datetime import date
from base import init_db
from models import save_entry, get_entry_by_date, get_all_entries, delete_entry

init_db()

page = st.sidebar.radio("Navigation", ["Log Today", "Dashboard", "History"])

if page == "Log Today":
    st.title("Log Today")

    selected_date = st.date_input("Date", value=date.today())
    existing = get_entry_by_date(str(selected_date))

    sleep_hours   = st.slider("Sleep Hours",   0.0, 12.0, float(existing["sleep_hours"])   if existing else 7.0, 0.5)
    sleep_quality = st.slider("Sleep Quality", 1,   5,    int(existing["sleep_quality"])   if existing else 3)
    mood          = st.slider("Mood",          1,   5,    int(existing["mood"])             if existing else 3)
    water_ml      = st.number_input("Water (ml)",    0, 5000, int(existing["water_ml"])    if existing else 2000, 100)
    screen_min    = st.number_input("Screen Time (min)", 0, 1440, int(existing["screen_min"]) if existing else 120, 10)
    weight_kg     = st.number_input("Weight (kg)",  0.0, 300.0, float(existing["weight_kg"]) if existing else 70.0, 0.1)
    notes         = st.text_area("Notes", value=existing["notes"] if existing and existing["notes"] else "")

    if st.button("Save"):
        save_entry(str(selected_date), sleep_hours, sleep_quality, mood, water_ml, screen_min, weight_kg, notes)
        st.success("Saved!")

elif page == "Dashboard":
    pass

elif page == "History":
    st.title("History")

    df = get_all_entries()

    if df.empty:
        st.info("No entries yet.")
    else:
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download CSV", csv, "life_metrics.csv", "text/csv")

        st.divider()
        delete_date = st.text_input("Delete entry by date (YYYY-MM-DD)")
        if st.button("Delete"):
            delete_entry(delete_date)
            st.success(f"Deleted {delete_date}")