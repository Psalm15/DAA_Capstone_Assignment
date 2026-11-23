import time

import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

from graph_utils import create_empty_graph, add_node, add_edge, generate_sample_graph, get_adjacency_list, get_adjacency_matrix
from route_planner import dijkstra
from traffic_analysis import bellman_ford, simulate_congestion
from connectivity_module import bfs_traversal, dfs_traversal
from mst_planner import prim_mst, kruskal_mst
from styles import CSS

# ---------------------------------------------------------------- palette
BG = "#0b1020"
PANEL = "#121a33"
CYAN = "#22d3ee"
VIOLET = "#8b5cf6"
AMBER = "#fbbf24"
GREEN = "#34d399"
MUTED = "#94a3c7"
TEXT = "#e6ecff"


# ---------------------------------------------------------------- plotting
def plot_graph(graph, highlight_nodes=None, highlight_edges=None):
    fig, ax = plt.subplots(figsize=(6.4, 4.4))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    if len(graph.nodes()) == 0:
        ax.text(0.5, 0.5, "Empty Graph", ha="center", va="center", color=MUTED, fontsize=14)
        ax.axis('off')
        return fig

    pos = nx.spring_layout(graph, seed=42)

    # base roads
    nx.draw_networkx_edges(graph, pos, ax=ax, edge_color="#3b4670", width=1.8, alpha=0.9)
    # base nodes (soft glow + node)
    nx.draw_networkx_nodes(graph, pos, ax=ax, node_color=CYAN, node_size=900, alpha=0.10)
    nx.draw_networkx_nodes(graph, pos, ax=ax, node_color="#1b2a55", node_size=520,
                           edgecolors=CYAN, linewidths=1.8)

    if highlight_nodes:
        nodes = [n for n in highlight_nodes if n in graph]
        nx.draw_networkx_nodes(graph, pos, nodelist=nodes, node_color=GREEN, node_size=1000, alpha=0.14, ax=ax)
        nx.draw_networkx_nodes(graph, pos, nodelist=nodes, node_color="#0f3b33", node_size=520,
                               edgecolors=GREEN, linewidths=2.2, ax=ax)
    if highlight_edges:
        edges_to_draw = []
        for edge in highlight_edges:
            u, v = edge[0], edge[1]
            if graph.has_edge(u, v):
                edges_to_draw.append((u, v))
            elif graph.has_edge(v, u):
                edges_to_draw.append((v, u))
        # glow underlay, then crisp line on top
        nx.draw_networkx_edges(graph, pos, edgelist=edges_to_draw, edge_color=AMBER, width=8, alpha=0.18, ax=ax)
        nx.draw_networkx_edges(graph, pos, edgelist=edges_to_draw, edge_color=AMBER, width=3, ax=ax)

    nx.draw_networkx_labels(graph, pos, ax=ax, font_color=TEXT, font_weight="bold", font_size=10)
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(
        graph, pos, edge_labels=edge_labels, ax=ax, font_color=AMBER, font_size=8,
        bbox=dict(boxstyle="round,pad=0.2", fc=BG, ec="none", alpha=0.85),
    )
    ax.axis('off')
    fig.tight_layout()
    return fig


def show_graph(graph, highlight_nodes=None, highlight_edges=None):
    fig = plot_graph(graph, highlight_nodes, highlight_edges)
    st.pyplot(fig)
    plt.close(fig)


def path_to_edges(path):
    return [(path[i], path[i+1]) for i in range(len(path)-1)]


# ---------------------------------------------------------------- UI helpers
def hero(title, subtitle):
    st.markdown(
        f"""
        <div class="hero">
            <div class="badge"><span class="dot"></span> LIVE SIMULATION</div>
            <h1>{title}</h1>
            <p>{subtitle}</p>
            <div class="road"></div><div class="car"></div><div class="car c2"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section(text):
    st.markdown(f'<div class="section-title">{text}</div>', unsafe_allow_html=True)


def path_chips(path):
    parts = []
    for i, node in enumerate(path):
        if i:
            parts.append('<span class="chip arrow">&rarr;</span>')
        parts.append(f'<span class="chip hot" style="animation-delay:{i * 0.08:.2f}s">{node}</span>')
    st.markdown(f'<div class="chip-row">{"".join(parts)}</div>', unsafe_allow_html=True)


def node_chips(nodes, cls="ok"):
    parts = [f'<span class="chip {cls}" style="animation-delay:{i * 0.05:.2f}s">{n}</span>' for i, n in enumerate(nodes)]
    st.markdown(f'<div class="chip-row">{"".join(parts)}</div>', unsafe_allow_html=True)


def cost_card(label, value):
    st.markdown(
        f'<div class="cost-card"><div class="v">{value}</div><div class="l">{label}</div></div>',
        unsafe_allow_html=True,
    )


def thinking(message="Crunching the network..."):
    """Short loading animation so results feel like they are being computed."""
    with st.spinner(message):
        time.sleep(0.45)


def init_state():
    if 'graph' not in st.session_state:
        st.session_state.graph = generate_sample_graph(5)


# ---------------------------------------------------------------- pages
def page_network_modeling():
    hero("Network Modeling", "Build the city's road network: add intersections, connect them with weighted roads.")
    g = st.session_state.graph

    col1, col2 = st.columns([1, 1.2], gap="large")

    with col1:
        section("Add Node")
        new_node = st.text_input("Node Name (e.g., A, B, 1, 2)")
        if st.button("Add Node"):
            if new_node:
                try:
                    new_node = int(new_node)
                except ValueError:
                    pass
                add_node(g, new_node)
                st.success(f"Added node: {new_node}")
                st.rerun()

        section("Add Edge")
        nodes = list(g.nodes())
        if len(nodes) >= 2:
            u = st.selectbox("Source", nodes, key="edge_u")
            v = st.selectbox("Destination", nodes, key="edge_v")
            w = st.number_input("Weight", min_value=1, value=10)
            if st.button("Add Edge"):
                if u != v:
                    add_edge(g, u, v, w)
                    st.success(f"Added edge {u}-{v} with weight {w}")
                    st.rerun()
                else:
                    st.error("Source and destination must be different.")

        section("Load Sample Graph")
        size = st.number_input("Number of Nodes", min_value=2, max_value=20, value=5)
        if st.button("Generate"):
            st.session_state.graph = generate_sample_graph(size)
            st.rerun()

    with col2:
        section("Road Network")
        show_graph(g)

    section("Graph Representations")
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.write("**Adjacency List**")
        st.json(get_adjacency_list(g))
    with c2:
        st.write("**Adjacency Matrix**")
        if len(list(g.nodes())) > 0:
            st.dataframe(get_adjacency_matrix(g), use_container_width=True)


def page_route_planning():
    hero("Route Planning", "Dijkstra's algorithm finds the cheapest route between two intersections.")
    g = st.session_state.graph
    nodes = list(g.nodes())

    if len(nodes) < 2:
        st.warning("Need at least 2 nodes in the graph.")
        return

    c1, c2 = st.columns(2, gap="large")
    with c1:
        src = st.selectbox("Source", nodes, key="rp_src")
    with c2:
        dst = st.selectbox("Destination", nodes, key="rp_dst")

    if st.button("Find Shortest Path"):
        thinking("Running Dijkstra...")
        path, cost, log = dijkstra(g, src, dst)

        if not path:
            st.error("No path found!")
        else:
            section("Best Route")
            path_chips(path)
            cost_card("Total cost", cost)
            cost_card("Stops", len(path))
            show_graph(g, highlight_nodes=path, highlight_edges=path_to_edges(path))

            section("Distance Updates Log")
            st.table(pd.DataFrame({"Log": log}))


def page_traffic_analysis():
    hero("Traffic Analysis", "Bellman-Ford shows how congestion on one road reshapes the best route.")
    g = st.session_state.graph
    nodes = list(g.nodes())
    edges = list(g.edges())

    if len(nodes) < 2 or len(edges) == 0:
        st.warning("Graph must have nodes and edges.")
        return

    c1, c2, c3 = st.columns(3, gap="large")
    with c1:
        src = st.selectbox("Source", nodes, key="ta_src")
    with c2:
        dst = st.selectbox("Destination", nodes, key="ta_dst")
    with c3:
        edge_to_congest = st.selectbox("Road to Congest", edges, format_func=lambda e: f"{e[0]} - {e[1]}")
        factor = st.slider("Congestion Factor", min_value=2.0, max_value=10.0, value=3.0)

    if st.button("Analyze Impact"):
        thinking("Simulating congestion...")
        orig_path, orig_cost, _ = bellman_ford(g, src, dst)

        congested_graph = simulate_congestion(g, [edge_to_congest], increase_factor=factor)
        new_path, new_cost, _ = bellman_ford(congested_graph, src, dst)

        col1, col2 = st.columns(2, gap="large")
        with col1:
            section("Before Congestion")
            if orig_path:
                path_chips(orig_path)
                cost_card("Cost", orig_cost)
                show_graph(g, highlight_edges=path_to_edges(orig_path))
            else:
                st.write("No path found.")

        with col2:
            section("After Congestion")
            if new_path:
                path_chips(new_path)
                cost_card("Cost", new_cost)
                show_graph(congested_graph, highlight_edges=path_to_edges(new_path))
            else:
                st.write("No path found.")

        section("Comparison")
        df = pd.DataFrame({
            "Metric": ["Path", "Cost"],
            "Original": [str(orig_path), orig_cost],
            "Congested": [str(new_path), new_cost]
        })
        st.table(df)


def page_connectivity():
    hero("Connectivity Analysis", "BFS and DFS reveal which zones are reachable and in what order.")
    g = st.session_state.graph
    nodes = list(g.nodes())

    if not nodes:
        st.warning("Empty graph.")
        return

    start = st.selectbox("Start Node", nodes)

    if st.button("Analyze Connectivity"):
        thinking("Traversing the network...")
        bfs_order, bfs_reachable = bfs_traversal(g, start)
        dfs_order, dfs_reachable = dfs_traversal(g, start)

        c1, c2 = st.columns(2, gap="large")
        with c1:
            section("BFS Traversal")
            st.markdown('<div class="kv"><b>Order</b></div>', unsafe_allow_html=True)
            path_chips(list(bfs_order))
            st.markdown(f'<div class="kv"><b>Reachable nodes:</b> {len(bfs_reachable)}</div>', unsafe_allow_html=True)
            show_graph(g, highlight_nodes=list(bfs_reachable))

        with c2:
            section("DFS Traversal")
            st.markdown('<div class="kv"><b>Order</b></div>', unsafe_allow_html=True)
            path_chips(list(dfs_order))
            st.markdown(f'<div class="kv"><b>Reachable nodes:</b> {len(dfs_reachable)}</div>', unsafe_allow_html=True)
            show_graph(g, highlight_nodes=list(dfs_reachable))


def page_infrastructure():
    hero("Infrastructure Planning", "Prim's and Kruskal's build the cheapest road layout that links every zone.")
    g = st.session_state.graph

    if len(g.nodes()) == 0:
        st.warning("Empty graph.")
        return

    if st.button("Compute Minimum Spanning Trees"):
        thinking("Building spanning trees...")
        p_edges, p_cost = prim_mst(g)
        k_edges, k_cost = kruskal_mst(g)

        c1, c2 = st.columns(2, gap="large")
        with c1:
            section("Prim's Algorithm")
            cost_card("Total cost", p_cost)
            cost_card("Edges", len(p_edges))
            show_graph(g, highlight_edges=p_edges)
            with st.expander("Edge list"):
                st.write(p_edges)

        with c2:
            section("Kruskal's Algorithm")
            cost_card("Total cost", k_cost)
            cost_card("Edges", len(k_edges))
            show_graph(g, highlight_edges=k_edges)
            with st.expander("Edge list"):
                st.write(k_edges)


# ---------------------------------------------------------------- main
def main():
    st.set_page_config(page_title="Smart City Traffic System", page_icon="🚦", layout="wide")
    st.markdown(CSS, unsafe_allow_html=True)
    init_state()

    st.sidebar.markdown(
        """
        <div class="brand">
            <div class="logo">🚦</div>
            <div><b>Smart City Traffic</b><span>Graph algorithm playground</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    pages = {
        "🏙️  Network Modeling": page_network_modeling,
        "🧭  Route Planning": page_route_planning,
        "🚗  Traffic Analysis": page_traffic_analysis,
        "🔗  Connectivity Analysis": page_connectivity,
        "🏗️  Infrastructure Planning": page_infrastructure,
    }

    selection = st.sidebar.radio("Go to", list(pages.keys()), label_visibility="collapsed")

    g = st.session_state.graph
    st.sidebar.markdown(
        f"""
        <div class="stat-row">
            <div class="stat"><div class="v">{g.number_of_nodes()}</div><div class="l">Intersections</div></div>
            <div class="stat"><div class="v">{g.number_of_edges()}</div><div class="l">Roads</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    pages[selection]()


if __name__ == "__main__":
    main()
