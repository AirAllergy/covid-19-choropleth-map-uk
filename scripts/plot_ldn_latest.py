import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import pickle
from pathlib import Path
import shutil
import numpy as np
from itertools import compress
from process_data import getData
from util import calBinsScale, getPlotPicklePath, classifyDf
from plot import plotCase, plotName, plotCasePickle
import warnings


def adjustNameLdn(xcoord, ycoord, name):
    """
    annotations adjustment for london boroughs
    """
    if name == "City of London":
        font = FontProperties(family="Palatino", size=3)
    else:
        font = FontProperties(family="Palatino", size=4)
    if name == "Hammersmith and Fulham":
        xcoord += 0.015
        ycoord -= 0.015
    if name == "Kensington and Chelsea":
        xcoord -= 0.015
        ycoord += 0.01
    if name == "Westminster":
        xcoord += 0.01
        ycoord -= 0.005
    if name == "Camden":
        xcoord -= 0.005
    if name.startswith("Hackney"):
        xcoord += 0.015
    if name == "Barking and Dagenham":
        ycoord -= 0.005
    if name == "Lewisham":
        ycoord -= 0.005
    return xcoord, ycoord, name, font


def plotLdn():
    fig, ax = plt.subplots(1, figsize=(6, 4))

    caseDates, caseGeo = getData(loc="London")

    binsScale = calBinsScale(caseGeo[caseDates[-1]])
    plotPicklePath = Path(getPlotPicklePath(binsScale, loc="ldn"))
    rebase = False
    if not plotPicklePath.is_file():
        rebase = True
    else:
        with warnings.catch_warnings(record=True) as w:
            with open(plotPicklePath, "rb") as f:
                ax = pickle.load(f)
            try:
                rebase = "This figure was saved with matplotlib version" in str(
                    w[-1].message
                )
            except IndexError:
                pass

    if rebase:
        caseDate = caseDates[-1]
        plotCase(ax, caseGeo, caseDate)
        plotName(caseGeo, adjustNameLdn)
        plt.text(
            0.1,
            0.05,
            caseDate.strftime("%d %b %Y"),
            transform=ax.transAxes,
            fontproperties=FontProperties(family="Palatino", size=8),
            label="dateText",
        )
        with open(plotPicklePath, "wb") as f:
            pickle.dump(ax, f, pickle.HIGHEST_PROTOCOL)

    caseToday = (
        caseGeo.drop(columns=["geometry", "coords"], errors="ignore")
        .set_index("name")
        .transpose()
    )
    caseYesterdayPicklePath = Path(
        "data", "pickle", "_".join(["cases", "ldn", "yesterday"]) + ".pickle"
    )
    if (not rebase) and caseYesterdayPicklePath.is_file():
        with open(caseYesterdayPicklePath, "rb") as f:
            caseYesterday = pickle.load(f)
        caseDiff = (
            classifyDf(caseYesterday, binsScale)
            .eq(classifyDf(caseToday, binsScale))
            .all(axis=1)
            .to_numpy()
        )
    else:
        caseDiff = np.full(len(caseDates), False)

    for caseDate in compress(caseDates, ~caseDiff):
        plt.cla()
        ax = plotCasePickle(binsScale, caseGeo, caseDate, plotPicklePath)
        caseImgPath = Path(
            "docs",
            "img",
            "_".join(["ldn", "cases"]),
            "_".join(["ldn", "cases", caseDate.strftime("%Y_%m_%d")]) + ".png",
        )
        plt.savefig(caseImgPath, dpi=300, transparent=False)
        if caseDate == caseDates[-1]:
            caseLatestImgPath = Path(
                "docs", "img", "_".join(["ldn", "cases", "latest"]) + ".png"
            )
            shutil.copy2(caseImgPath, caseLatestImgPath)

    with open(caseYesterdayPicklePath, "wb") as f:
        pickle.dump(caseToday, f, pickle.HIGHEST_PROTOCOL)

    plt.close("all")
