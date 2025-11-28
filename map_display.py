# map_display.py
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


def build_map_figure(G, path1=None, path2=None, map_path="michigan_map.png"):
    img = mpimg.imread(map_path)

    fig, ax = plt.subplots(figsize=(6, 4))

    #show image and fill
    ax.imshow(img)
    ax.set_xticks([])
    ax.set_yticks([])

    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    ax.set_xlim(0, img.shape[1])
    ax.set_ylim(img.shape[0], 0)

    #draw cities
    for city in G.nodes():
        x, y = CITY_PIXELS[city]
        ax.scatter(x, y, color="black", s=30)

    #draw paths
    if path1:
        for i in range(len(path1) - 1):
            c1, c2 = path1[i], path1[i + 1]
            x1, y1 = CITY_PIXELS[c1]
            x2, y2 = CITY_PIXELS[c2]

            #only every first segment gets a label
            label = "Shortest Path" if i == 0 else "_nolegend_"

            ax.plot([x1, x2], [y1, y2], color="red", linewidth=3, label=label)

    if path2:
        for i in range(len(path2) - 1):
            c1, c2 = path2[i], path2[i + 1]
            x1, y1 = CITY_PIXELS[c1]
            x2, y2 = CITY_PIXELS[c2]

            #only every first segment gets a label
            label = "Second Shortest Path" if i == 0 else "_nolegend_"

            ax.plot([x1, x2], [y1, y2], color="blue", linestyle="--", linewidth=3, label=label)

    #show only if paths exist
    if path1 or path2:
        ax.legend(loc="lower left", fontsize=8)

    ax.axis("off")
    return fig
