
import matplotlib.pyplot as plt
import networkx as nx

G = nx.Graph()

G.add_edge(0, 1, weight=0.6)
G.add_edge(0, 2, weight=0.2)
G.add_edge(2, 3, weight=0.1)
G.add_edge(2, 4, weight=0.7)
G.add_edge(2, 5, weight=0.9)
G.add_edge(0, 3, weight=0.3)

pos = nx.spring_layout(G, seed=7)  # positions for all nodes - seed for reproducibility

nx.draw(G, pos)

nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")


edge_labels = nx.get_edge_attributes(G, "weight")
nx.draw_networkx_edge_labels(G, pos, edge_labels)

ax = plt.gca()
ax.margins(0.08)
plt.axis("off")
plt.tight_layout()
plt.show()