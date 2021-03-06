import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.collections import PatchCollection
from matplotlib.font_manager import FontProperties
from pyproj import Proj, transform
import pickle
import geopandas as gpd
from geopandas.plotting import _flatten_multi_geoms, _mapclassify_choro
from util import getAbbrv, calBinsScale, calBinsBoundary


def plotCase(ax, caseGeo, caseDate, binsScale=None, legendScale=1.0):
    """
    plot the choropleth map
    """
    if binsScale is None:
        binsScale = calBinsScale(caseGeo[caseDate])

    ax.axis("off")
    ax.set_aspect("equal")

    binsBoundary = calBinsBoundary(binsScale)
    bins = binsBoundary[1:] - 0.01

    cmap = "OrRd"
    ncolor = 256
    norm = mcolors.BoundaryNorm(
        binsBoundary, ncolor, clip=True
    )  # norm takes (..., ...]

    pc = PatchCollection([], edgecolors="none", cmap=cmap, norm=norm)

    binsTextsLeft = binsBoundary.astype(int).astype(str)
    binsTextsRight = (binsBoundary - 1).astype(int).astype(str)
    binsTexts = zip(binsTextsLeft[1:-2], binsTextsRight[2:-1])
    texts = (
        ["0"]
        + ["{:s} - {:s}".format(i, j) for i, j in binsTexts]
        + ["≥ " + binsTextsLeft[-2]]
    )

    handles = [
        plt.plot(
            [],
            [],
            marker="s",
            linestyle="",
            color=pc.cmap(pc.norm(j)),
            label="{:s}".format(texts[i]),
        )[0]
        for i, j in tuple(zip(range(len(texts)), bins))
    ]

    font = FontProperties(family="Palatino", size=4 * legendScale)

    caseGeo.to_crs(epsg=3857).plot(
        column=caseDate,
        ax=ax,
        legend=True,
        legend_kwds={
            "handles": handles,
            "bbox_to_anchor": (0.5, -0.1 / legendScale),
            "loc": "lower center",
            "ncol": len(bins),
            "prop": font,
            "frameon": False,
            "markerscale": 0.5 * legendScale,
        },
        scheme="UserDefined",
        classification_kwds={"bins": bins,},  # mapclassify takes [..., ...)
        cmap=cmap,
        norm=mcolors.BoundaryNorm(np.arange(len(binsBoundary)), ncolor, clip=True),
        edgecolor="grey",
        linewidths=0.05,
        zorder=1,
        label="plotPC",
    )


def plotName(caseGeo, adjustName):
    """
    plot region names
    """
    nameAbbrvDict = getAbbrv()
    caseGeo["coords"] = caseGeo["geometry"].apply(lambda x: x.centroid)
    for idx, row in caseGeo.iterrows():
        xcoord = row["coords"].x
        ycoord = row["coords"].y
        name = row["name"]
        xcoord, ycoord, name, font = adjustName(xcoord, ycoord, name)
        s = nameAbbrvDict[name].replace("\\n", "\n")
        xy = transform(Proj(init="epsg:4326"), Proj(init="epsg:3857"), xcoord, ycoord)
        plt.annotate(
            s=s,
            xy=xy,
            horizontalalignment="center",
            verticalalignment="center",
            fontproperties=font,
        )


def plotCasePickle(binsScale, caseGeo, caseDate, plotPicklePath):
    with open(plotPicklePath, "rb") as f:
        ax = pickle.load(f)
    binsBoundary = calBinsBoundary(binsScale)
    bins = binsBoundary[1:] - 0.01
    binning = _mapclassify_choro(
        caseGeo.loc[:, caseDate], scheme="UserDefined", bins=bins, k=len(bins)
    )
    geoms, multiindex = _flatten_multi_geoms(caseGeo.geometry, prefix="Geom")
    values = np.take(binning.yb, multiindex, axis=0)
    geoms, multiindex = _flatten_multi_geoms(gpd.GeoSeries(geoms))
    values = np.take(values, multiindex, axis=0)
    for item in ax.get_children():
        if item.get_label() == "plotPC":
            item.set_array(values)
        if item.get_label() == "dateText":
            item.set_text(caseDate.strftime("%d %b %Y"))
    return ax
