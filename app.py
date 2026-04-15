import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from simulation import run_simulation_with_graph

st.set_page_config(page_title="Deadlock Simulator", layout="wide")

st.title("Distributed Deadlock Detection Simulator")

if st.button("Run Simulation"):

    logs, edges, deadlocks = run_simulation_with_graph()

    col1, col2 = st.columns([1, 2])

    # 🔴 Deadlocks Panel
    with col1:
        st.subheader(" Deadlocks")
        if deadlocks:
            for d in deadlocks:
                st.error(f"Deadlock involving {d}")
        else:
            st.success("No deadlocks detected")

    # 📊 Graph Panel
    with col2:
        st.subheader(" Wait-For Graph")

        G = nx.DiGraph()
        G.add_edges_from(edges)

        pos = nx.spring_layout(G)

        plt.figure(figsize=(6, 4))
        nx.draw(
            G,
            pos,
            with_labels=True,
            node_color="lightblue",
            node_size=2000,
            font_size=10,
            arrows=True
        )

        st.pyplot(plt)

    # 📜 Logs (collapsible)
    with st.expander(" Simulation Logs"):
        for log in logs:
            st.text(log)