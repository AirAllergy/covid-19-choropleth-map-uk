from retrieve_data import retrieveData
from parse_data import parseData
from plot_uk_latest import plotUK
from plot_ldn_latest import plotLdn


def main():
    for country in ["Eng", "Wls", "Sct", "Nir"]:
        retrieveData(country)
        parseData(country)

    plotUK()
    plotLdn()


if __name__ == "__main__":
    main()
