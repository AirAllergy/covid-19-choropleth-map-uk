import requests
from pathlib import Path
from util import retrieveFileLinkWls

fileLinks = {
    "eng": "https://coronavirus.data.gov.uk/downloads/csv/coronavirus-cases_latest.csv",
    "wls": retrieveFileLinkWls(),
    # 'sct': 'https://raw.githubusercontent.com/tomwhite/covid-19-uk-data/master/data/covid-19-cases-uk.csv',
    "sct": "https://www.gov.scot/binaries/content/documents/govscot/publications/statistics/2020/04/coronavirus-covid-19-trends-in-daily-data/documents/covid-19-data-by-nhs-board/covid-19-data-by-nhs-board/govscot%3Adocument/COVID-19%2Bdata%2Bby%2BNHS%2BBoard%2B110520.xlsx",
    "nir": "https://api.coronavirus-staging.data.gov.uk/v1/data?filters=areaType=nation;areaName=Northern%2520Ireland&structure=%7B%22areaType%22:%22areaType%22,%22areaName%22:%22areaName%22,%22areaCode%22:%22areaCode%22,%22date%22:%22date%22,%22newCasesByPublishDate%22:%22newCasesByPublishDate%22,%22cumCasesByPublishDate%22:%22cumCasesByPublishDate%22%7D&format=csv",
}


def downloadFile(fileLink, fileDir, filename):
    response = requests.get(fileLink, stream=True)
    fileExtension = fileLink.split(".")[-1]
    if fileExtension not in ("csv", "xlsx"):
        fileExtension = "csv"
    filePath = Path(fileDir, ".".join([filename, fileExtension]))
    with open(filePath, "wb") as f:
        for chunk in response.iter_content(1024):
            f.write(chunk)


def retrieveData(country):
    country = country.lower()
    fileLink = fileLinks[country]
    fileDir = "data/csv/src"
    filename = "data_latest_" + country
    downloadFile(fileLink, fileDir, filename)
