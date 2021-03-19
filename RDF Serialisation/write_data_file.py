import pandas as pd
import re


def replaceSpaceWithunderScore(string):
    string = string.replace(" ", "")
    if string == "<250":
        string = "WorkforceSizeLessThan250"
    if string == "250+":
        string = "WorkforceSize250More"
    if string == "AllSizeBands":
        string = "Total"

    string = string.replace("<", "LessThan")
    string = string.replace("+", "More")
    string = re.sub('[^A-Za-z0-9]+', '', string)
    string = string.replace(",", "").replace(";", "")

    return string


def getSheet(sheet_num, header, use_cols):
    Sheet = pd.read_excel(
        "CW1-BusinessImpactsOfCovid19Data.xlsx", sheet_name=sheet_num, header=header, usecols=use_cols)
    return Sheet


def remove_notes(sheet, indexes):
    sheet = sheet.drop(indexes)
    return sheet


def sampleSize(outputDataFile):
    sample_size = getSheet(2, 3, "A:D")
    sample_size = remove_notes(sample_size, indexes=sample_size.index[16:24])
    printDataSet("Total Number of Survey Sent Out", sample_size,
                 outputDataFile=outputDataFile, ds="ds1")
    printDataPoint(sample_size, outputDataFile=outputDataFile, ds="ds1")


def responseRate(outputDataFile):
    num_responses = getSheet(sheet_num=3, header=3, use_cols="A:D")
    num_responses = num_responses.head(13)

    printDataSet("Number of Responses", num_responses,
                 outputDataFile=outputDataFile, ds="ds2")
    printDataPoint(num_responses, outputDataFile=outputDataFile, ds="ds2")

    proportion_responses = getSheet(sheet_num=3, header=3, use_cols="G:J")
    proportion_responses = proportion_responses.head(13)

    proportion_responses.columns = num_responses.columns
    printDataSet("Proportion of Responses", proportion_responses,
                 outputDataFile=outputDataFile, ds="ds3")
    printDataPoint(
        proportion_responses, outputDataFile=outputDataFile, ds="ds3")


def tradingStatus(outputDataFile):
    trading_status_industry = getSheet(sheet_num=4, header=3, use_cols="A:D")
    trading_status_industry = trading_status_industry.head(13)
    printDataSet("Trading Status By Industry", trading_status_industry,
                 outputDataFile=outputDataFile, ds="ds4")
    printDataPoint(trading_status_industry,
                   outputDataFile=outputDataFile, ds="ds4")

    trading_status_workforce = getSheet(sheet_num=4, header=29, use_cols="A:D")
    trading_status_workforce = trading_status_workforce.head(3)

    printDataSet("Trading Status By Workforce", trading_status_workforce,
                 outputDataFile=outputDataFile, ds="ds5")
    printDataPoint(trading_status_workforce,
                   outputDataFile=outputDataFile, ds="ds5")

    trading_status_country = getSheet(sheet_num=4, header=44, use_cols="A:D")
    trading_status_country = trading_status_country.head(5)
    printDataSet("Trading Status By Country", trading_status_country,
                 outputDataFile=outputDataFile, ds="ds6")
    printDataPoint(trading_status_country,
                   outputDataFile=outputDataFile, ds="ds6")


def govSchemeOne(outputDataFile):
    goveScheme_industry = getSheet(sheet_num=5, header=3, use_cols="A:H")
    goveScheme_industry = goveScheme_industry.head(13)
    printDataSet("Government Scheme By Industry", goveScheme_industry,
                 outputDataFile=outputDataFile, ds="ds7")
    printDataPoint(goveScheme_industry,
                   outputDataFile=outputDataFile, ds="ds7")

    goveScheme_workforce = getSheet(sheet_num=5, header=27, use_cols="A:H")
    goveScheme_workforce = goveScheme_workforce.head(3)
    printDataSet("Government Scheme By Workforce", goveScheme_workforce,
                 outputDataFile=outputDataFile, ds="ds8")
    printDataPoint(goveScheme_workforce,
                   outputDataFile=outputDataFile, ds="ds8")

    goveScheme_country = getSheet(sheet_num=5, header=27, use_cols="A:H")
    goveScheme_country = goveScheme_country.head(3)
    printDataSet("Government Scheme By Country", goveScheme_country,
                 outputDataFile=outputDataFile, ds="ds9")
    printDataPoint(goveScheme_country,
                   outputDataFile=outputDataFile, ds="ds9")


def govSchemeTwo(outputDataFile):
    goveScheme_industry = getSheet(sheet_num=6, header=3, use_cols="A:H")
    goveScheme_industry = goveScheme_industry.head(13)
    printDataSet("Government Scheme2 By Industry", goveScheme_industry,
                 outputDataFile=outputDataFile, ds="ds10")
    printDataPoint(goveScheme_industry,
                   outputDataFile=outputDataFile, ds="ds10")

    goveScheme_workforce = getSheet(sheet_num=6, header=29, use_cols="A:H")
    goveScheme_workforce = goveScheme_workforce.head(3)
    printDataSet("Government Scheme2 By Workforce", goveScheme_workforce,
                 outputDataFile=outputDataFile, ds="ds11")
    printDataPoint(goveScheme_workforce,
                   outputDataFile=outputDataFile, ds="ds11")


def govThree(outputDataFile):
    goveScheme_industry = getSheet(sheet_num=7, header=3, use_cols="A:H")
    goveScheme_industry = goveScheme_industry.head(13)
    printDataSet("Government Scheme3 By Industry", goveScheme_industry,
                 outputDataFile=outputDataFile, ds="ds12")
    printDataPoint(goveScheme_industry,
                   outputDataFile=outputDataFile, ds="ds12")

    goveScheme_workforce = getSheet(sheet_num=7, header=28, use_cols="A:H")
    goveScheme_workforce = goveScheme_workforce.head(3)
    printDataSet("Government Scheme3 By Workforce", goveScheme_workforce,
                 outputDataFile=outputDataFile, ds="ds13")
    printDataPoint(goveScheme_workforce,
                   outputDataFile=outputDataFile, ds="ds13")


def printDataSet(table_name, table, outputDataFile, ds):

    outputDataFile.write("#Dataset\n")
    outputDataFile.write(":"+ds+" rdf:type qb:dataset;\n")
    outputDataFile.write(
        '\t dc:title' + '"'+table_name + '"' + ';')
    outputDataFile.write("\n")

    for row in range(1, len(table.index)+1):
        for col in range(1, len(table.columns)):
            if row == len(table.index) and col == len(table.columns)-1:
                outputDataFile.write("     qb:observation :"+ds +
                                     "_"+str(row)+"_"+str(col)+".\n")
                outputDataFile.write("\n")
            else:
                outputDataFile.write("     qb:observation :"+ds +
                                     "_"+str(row)+"_"+str(col)+";\n")


def printDataPoint(table, outputDataFile, ds):

    for row in range(0, len(table.index)):
        for col in range(0, len(table.columns)-1):
            outputDataFile.write(":"+ds+"_"+str(row+1)+"_"+str(col+1) +
                                 " rdf:type qb:observation;\n")
            outputDataFile.write(
                "      rdf:value "+str(table.iloc[row][table.columns[col+1]])+";\n")
            outputDataFile.write(
                "      qb:DimensionProperty "+" :"+replaceSpaceWithunderScore(table.columns[col+1])+";\n")

            outputDataFile.write("      qb:DimensionProperty " + ":" +
                                 replaceSpaceWithunderScore(str(table.iloc[row][table.columns[0]]))+".\n")

            outputDataFile.write("\n")


def printDataFile(outputDataFile):

    outputDataFile.write("@prefix : <BCISSurvey.com/data/>.\n")
    outputDataFile.write(
        "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n")
    outputDataFile.write("@prefix dc: <http://purl.org/dc/elements/1.1/> .\n")

    outputDataFile.write("@prefix owl: <http://www.w3.org/2002/07/owl#> .\n")
    outputDataFile.write(
        "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n")
    outputDataFile.write(
        "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n")
    outputDataFile.write("@prefix qb: <http://purl.org/linked-dat/cube#> .\n")
    outputDataFile.write(
        "@prefix survey: <http://enakting.org/schema/survey/> .\n")

    outputDataFile.write("\n")

    sample_size = getSheet(2, 3, "A:D")
    sample_size = sample_size.head(16)

    trading_status_country = getSheet(sheet_num=4, header=44, use_cols="A:D")
    trading_status_country = trading_status_country.head(5)

    goveScheme_industry = getSheet(sheet_num=7, header=3, use_cols="A:H")
    goveScheme_industry = goveScheme_industry.head(13)

    printClassEntities(sample_size,
                       "Industry", class_name="Industry", outputDataFile=outputDataFile)

    printClassEntities(sample_size,
                       row_name=None, class_name="WorkForce", outputDataFile=outputDataFile)

    printClassEntities(trading_status_country,
                       "Country", class_name="Country", outputDataFile=outputDataFile)

    printClassEntities(trading_status_country,
                       row_name=None, class_name="TradingStatus", outputDataFile=outputDataFile)

    printClassEntities(goveScheme_industry,
                       row_name=None, class_name="SchemeType", outputDataFile=outputDataFile)


def printClassEntities(sheet, row_name, class_name, outputDataFile):
    if row_name:
        for index, row in sheet.iterrows():

            outputDataFile.write(
                ':'+replaceSpaceWithunderScore(row[row_name]) + ' rdf:type survey:'+class_name+';\n     dc:title '+'"'+row[row_name]+'"'+'.\n')
            outputDataFile.write("\n")
    else:
        for col in sheet.columns:
            if col != "Industry" and col != "Workforce Size" and col != "Country":
                outputDataFile.write(
                    ':'+replaceSpaceWithunderScore(col) + ' rdf:type survey:'+class_name+';\n     dc:title '+'"'+col+'"'+'.\n')
                outputDataFile.write("\n")


# print the data file
def main():
    outputDataFile = open("BCISSurveyData.ttl", 'w')
    printDataFile(outputDataFile)
    sampleSize(outputDataFile)
    responseRate(outputDataFile)
    tradingStatus(outputDataFile)
    govSchemeOne(outputDataFile)
    govSchemeTwo(outputDataFile)
    govThree(outputDataFile)


main()
