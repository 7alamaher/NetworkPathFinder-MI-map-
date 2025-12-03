import matplotlib.pyplot as plt
import matplotlib.image as mpimg

CITY_PIXELS = {
    "Detroit": (417, 391),
    "Pontiac": (407, 372),
    "Flint": (380, 347),
    "Ann Arbor": (377, 398),
    "Lansing": (337, 370),
    "Battle Creek": (297, 400),
    "Grand Rapids": (267, 350),
    "Muskegon": (231, 330),
    "Traverse City": (268, 215),
    "Cheboygan": (335, 145),
    "Marquette": (173, 73),
}

def build_map_figure(G, path1=None, path2=None, invalid_pair=None, map_path="michigan_map.png"):
    img = mpimg.imread(map_path)

    fig, ax = plt.subplots(figsize=(8, 10))

    # Base map
    ax.imshow(img)
    ax.set_xticks([])
    ax.set_yticks([])
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_xlim(0, img.shape[1])
    ax.set_ylim(img.shape[0], 0)

    # Draw cities
    for city in G.nodes():
        x, y = CITY_PIXELS[city]
        ax.scatter(x, y, color="black", s=30)

    # ------------------------------------
    # Draw INVALID DIRECT ROAD (GRAY LINE)
    # ------------------------------------
    if invalid_pair:
        c1, c2 = invalid_pair
        x1, y1 = CITY_PIXELS[c1]
        x2, y2 = CITY_PIXELS[c2]

        ax.plot(
            [x1, x2], [y1, y2],
            color="yellow",
            linestyle=":",
            linewidth=2,
            label="Invalid path"
        )

    # Draw shortest path (RED)
    if path1:
        for i in range(len(path1) - 1):
            c1, c2 = path1[i], path1[i+1]
            x1, y1 = CITY_PIXELS[c1]
            x2, y2 = CITY_PIXELS[c2]
            label = "Shortest Path" if i == 0 else "_nolegend_"
            ax.plot([x1, x2], [y1, y2], color="lightgreen", linewidth=3, label=label)

    # Draw second-best path (BLUE)
    if path2:
        for i in range(len(path2) - 1):
            c1, c2 = path2[i], path2[i+1]
            x1, y1 = CITY_PIXELS[c1]
            x2, y2 = CITY_PIXELS[c2]
            label = "Second Shortest Path" if i == 0 else "_nolegend_"
            ax.plot([x1, x2], [y1, y2], color="darkblue", linestyle="--", linewidth=3, label=label)

    # Legend
    if path1 or path2 or invalid_pair:
        ax.legend(loc="lower left", fontsize=8)

    ax.axis("off")
    return fig

