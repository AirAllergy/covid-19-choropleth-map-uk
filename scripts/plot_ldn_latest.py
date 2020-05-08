import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import pickle
from process_data import getData, getGeoIreland
from util import calBinsScale, getPlotPicklePath, checkPlotPickle
from plot import plotCase, plotName, plotCasePickle


def adjustNameLdn(xcoord, ycoord, name):
    '''
    annotations adjustment for london boroughs
    '''
    if name == 'City of London':
        font = FontProperties(family='Palatino', size=3)
    else:
        font = FontProperties(family='Palatino', size=4)
    if name == 'Hammersmith and Fulham':
        xcoord += 0.015
        ycoord -= 0.015
    if name == 'Kensington and Chelsea':
        xcoord -= 0.015
        ycoord += 0.01
    if name == 'Westminster':
        xcoord += 0.01
        ycoord -= 0.005
    if name == 'Camden':
        xcoord -= 0.005
    if name == 'Hackney':
        xcoord += 0.015
    if name == 'Barking and Dagenham':
        ycoord -= 0.005
    if name == 'Lewisham':
        ycoord -= 0.005
    return xcoord, ycoord, name, font


def plot_ldn_latest():
    fig, ax = plt.subplots(1, figsize=(6, 4))

    caseDates, caseGeo = getData(loc='London')

    binsScale = calBinsScale(caseGeo[caseDates[-1]])
    plotPicklePath = getPlotPicklePath(binsScale, loc='London')
    if not checkPlotPickle(binsScale, loc='London'):
        caseDate = caseDates[-1]
        plotCase(ax, caseGeo, caseDate)
        plotName(caseGeo, adjustNameLdn)
        plt.text(
            0.1, 0.05,
            caseDate.strftime('%d %b %Y'),
            transform=ax.transAxes,
            fontproperties=FontProperties(family='Palatino', size=8),
            label='dateText'
        )
        with open(plotPicklePath, 'wb') as f:
            pickle.dump(ax, f, pickle.HIGHEST_PROTOCOL)
    else:
        plotCasePickle(binsScale, caseGeo, caseDates[-1], plotPicklePath)

    plt.savefig('docs/img/london_cases_latest.png', dpi=300, transparent=False)
