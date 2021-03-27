import pandas as pd
import re
import json


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
            outputDataFile.write('      qb:dimension' +
                                 ' :'+"TP04_2020" + '' + ';\n')
            outputDataFile.write(
                "      qb:dimension"+" :"+replaceSpaceWithunderScore(table.columns[col+1])+";\n")

            outputDataFile.write("      qb:dimension " + ":" +
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

    # sampleSizeJSON(outputDataFile)
    # responseRateJson(outputDataFile)
    # tradingStatusJSON(outputDataFile)
    # govSchemeOneJSON(outputDataFile)
    # govSchemeTwoJSON(outputDataFile)
    # govThreeJSON(outputDataFile)
# main()


def sampleSizeJSON(outputDataFile):
    table = getSheet(2, 3, "A:D")
    table = remove_notes(table, indexes=table.index[16:24])

    res = []
    for row in range(0, len(table.index)):
        for col in range(0, len(table.columns)-1):
            data = {}
            print(table.iloc[row][table.columns[col+1]])
            data['value'] = table.iloc[row][table.columns[col+1]]
            data['WorkForce'] = replaceSpaceWithunderScore(
                table.columns[col+1])
            data['Industry'] = replaceSpaceWithunderScore(
                str(table.iloc[row][table.columns[0]]))
            res.append(data)

    jsondata = {'name': 'sample size', 'dataset': res,
                'notes': 'Sample Size Table, show number of survey sent out.'}
    json.dump(jsondata, outputDataFile)


def responseRateJson(outputDataFile):
    table = getSheet(sheet_num=3, header=3, use_cols="A:D")
    table = table.head(13)
    res = []
    for row in range(0, len(table.index)):
        for col in range(0, len(table.columns)-1):
            data = {}
            print(table.iloc[row][table.columns[col+1]])
            data['value'] = table.iloc[row][table.columns[col+1]]
            data['WorkForce'] = replaceSpaceWithunderScore(
                table.columns[col+1])
            data['Industry'] = replaceSpaceWithunderScore(
                str(table.iloc[row][table.columns[0]]))
            res.append(data)
    jsondata = {'name': 'Number of responses', 'dataset': res}
    json.dump(jsondata, outputDataFile)

    temp = table.columns
    table = getSheet(sheet_num=3, header=3, use_cols="G:J")
    table = table.head(13)
    table.columns = temp
    res = []
    for row in range(0, len(table.index)):
        for col in range(0, len(table.columns)-1):
            data = {}
            print(table.iloc[row][table.columns[col+1]])
            data['value'] = table.iloc[row][table.columns[col+1]]
            data['WorkForce'] = replaceSpaceWithunderScore(
                table.columns[col+1])
            data['Industry'] = replaceSpaceWithunderScore(
                str(table.iloc[row][table.columns[0]]))
            res.append(data)
    jsondata = {'name': 'Proportion of Responses', 'dataset': res}
    json.dump(jsondata, outputDataFile)


def tradingStatusJSON(outputDataFile):
    trading_status_industry = getSheet(sheet_num=4, header=3, use_cols="A:D")
    trading_status_industry = trading_status_industry.head(13)
    res = []
    for row in range(0, len(trading_status_industry.index)):
        for col in range(0, len(trading_status_industry.columns)-1):
            data = {}
            print(trading_status_industry.iloc[row]
                  [trading_status_industry.columns[col+1]])
            data['value'] = trading_status_industry.iloc[row][trading_status_industry.columns[col+1]]
            data['TradingStatus'] = replaceSpaceWithunderScore(
                trading_status_industry.columns[col+1])
            data['Industry'] = replaceSpaceWithunderScore(
                str(trading_status_industry.iloc[row][trading_status_industry.columns[0]]))
            res.append(data)

    jsondata = {'name': 'Trading Status by Industry', 'dataset': res}
    json.dump(jsondata, outputDataFile)

    trading_status_workforce = getSheet(sheet_num=4, header=29, use_cols="A:D")
    trading_status_workforce = trading_status_workforce.head(3)

    res = []
    for row in range(0, len(trading_status_workforce.index)):
        for col in range(0, len(trading_status_workforce.columns)-1):
            data = {}
            print(trading_status_workforce.iloc[row]
                  [trading_status_workforce.columns[col+1]])
            data['value'] = trading_status_workforce.iloc[row][trading_status_workforce.columns[col+1]]
            data['TradingStatus'] = replaceSpaceWithunderScore(
                trading_status_workforce.columns[col+1])
            data['WorkForce'] = replaceSpaceWithunderScore(
                str(trading_status_workforce.iloc[row][trading_status_workforce.columns[0]]))
            res.append(data)

    jsondata = {'name': 'Trading Status by Workforce', 'dataset': res}
    json.dump(jsondata, outputDataFile)

    trading_status_country = getSheet(sheet_num=4, header=44, use_cols="A:D")
    trading_status_country = trading_status_country.head(5)
    res = []
    for row in range(0, len(trading_status_country.index)):
        for col in range(0, len(trading_status_country.columns)-1):
            data = {}
            print(trading_status_country.iloc[row]
                  [trading_status_country.columns[col+1]])
            data['value'] = trading_status_country.iloc[row][trading_status_country.columns[col+1]]
            data['TradingStatus'] = replaceSpaceWithunderScore(
                trading_status_country.columns[col+1])
            data['Country'] = replaceSpaceWithunderScore(
                str(trading_status_country.iloc[row][trading_status_country.columns[0]]))
            res.append(data)
    jsondata = {'name': 'Trading Status by Country', 'dataset': res}
    json.dump(jsondata, outputDataFile)


def govSchemeOneJSON(outputDataFile):
    goveScheme_industry = getSheet(sheet_num=5, header=3, use_cols="A:H")
    goveScheme_industry = goveScheme_industry.head(13)
    res = []
    for row in range(0, len(goveScheme_industry.index)):
        for col in range(0, len(goveScheme_industry.columns)-1):
            data = {}
            print(goveScheme_industry.iloc[row]
                  [goveScheme_industry.columns[col+1]])
            data['value'] = goveScheme_industry.iloc[row][goveScheme_industry.columns[col+1]]
            data['SchemeType'] = replaceSpaceWithunderScore(
                goveScheme_industry.columns[col+1])
            data['Industry'] = replaceSpaceWithunderScore(
                str(goveScheme_industry.iloc[row][goveScheme_industry.columns[0]]))
            res.append(data)
    jsondata = {'name': 'Government Scheme One by Industry', 'dataset': res}
    json.dump(jsondata, outputDataFile)

    goveScheme_workforce = getSheet(sheet_num=5, header=27, use_cols="A:H")
    goveScheme_workforce = goveScheme_workforce.head(3)
    res = []
    for row in range(0, len(goveScheme_workforce.index)):
        for col in range(0, len(goveScheme_workforce.columns)-1):
            data = {}
            print(goveScheme_workforce.iloc[row]
                  [goveScheme_workforce.columns[col+1]])
            data['value'] = goveScheme_workforce.iloc[row][goveScheme_workforce.columns[col+1]]
            data['SchemeType'] = replaceSpaceWithunderScore(
                goveScheme_workforce.columns[col+1])
            data['WorkForce'] = replaceSpaceWithunderScore(
                str(goveScheme_workforce.iloc[row][goveScheme_workforce.columns[0]]))
            res.append(data)
    jsondata = {'name': 'Government Scheme One by WorkForce', 'dataset': res}
    json.dump(jsondata, outputDataFile)

    goveScheme_country = getSheet(sheet_num=5, header=27, use_cols="A:H")
    goveScheme_country = goveScheme_country.head(3)
    res = []
    for row in range(0, len(goveScheme_country.index)):
        for col in range(0, len(goveScheme_country.columns)-1):
            data = {}
            print(goveScheme_country.iloc[row]
                  [goveScheme_country.columns[col+1]])
            data['value'] = goveScheme_country.iloc[row][goveScheme_country.columns[col+1]]
            data['SchemeType'] = replaceSpaceWithunderScore(
                goveScheme_country.columns[col+1])
            data['Country'] = replaceSpaceWithunderScore(
                str(goveScheme_country.iloc[row][goveScheme_country.columns[0]]))
            res.append(data)
    jsondata = {'name': 'Government Scheme One by Country', 'dataset': res}
    json.dump(jsondata, outputDataFile)


def govSchemeTwoJSON(outputDataFile):
    goveScheme_industry = getSheet(sheet_num=6, header=3, use_cols="A:H")
    goveScheme_industry = goveScheme_industry.head(13)
    res = []
    for row in range(0, len(goveScheme_industry.index)):
        for col in range(0, len(goveScheme_industry.columns)-1):
            data = {}
            print(goveScheme_industry.iloc[row]
                  [goveScheme_industry.columns[col+1]])
            data['value'] = goveScheme_industry.iloc[row][goveScheme_industry.columns[col+1]]
            data['SchemeType'] = replaceSpaceWithunderScore(
                goveScheme_industry.columns[col+1])
            data['Industry'] = replaceSpaceWithunderScore(
                str(goveScheme_industry.iloc[row][goveScheme_industry.columns[0]]))
            res.append(data)
    jsondata = {'name': 'Government Scheme Two by Industry', 'dataset': res}
    json.dump(jsondata, outputDataFile)

    goveScheme_workforce = getSheet(sheet_num=6, header=29, use_cols="A:H")
    goveScheme_workforce = goveScheme_workforce.head(3)
    res = []
    for row in range(0, len(goveScheme_workforce.index)):
        for col in range(0, len(goveScheme_workforce.columns)-1):
            data = {}
            print(goveScheme_workforce.iloc[row]
                  [goveScheme_workforce.columns[col+1]])
            data['value'] = goveScheme_workforce.iloc[row][goveScheme_workforce.columns[col+1]]
            data['SchemeType'] = replaceSpaceWithunderScore(
                goveScheme_workforce.columns[col+1])
            data['WorkForce'] = replaceSpaceWithunderScore(
                str(goveScheme_workforce.iloc[row][goveScheme_workforce.columns[0]]))
            res.append(data)
    jsondata = {'name': 'Government Scheme Two by WorkForce', 'dataset': res}
    json.dump(jsondata, outputDataFile)


def govThreeJSON(outputDataFile):
    goveScheme_industry = getSheet(sheet_num=7, header=3, use_cols="A:H")
    goveScheme_industry = goveScheme_industry.head(13)
    res = []
    for row in range(0, len(goveScheme_industry.index)):
        for col in range(0, len(goveScheme_industry.columns)-1):
            data = {}
            print(goveScheme_industry.iloc[row]
                  [goveScheme_industry.columns[col+1]])
            data['value'] = goveScheme_industry.iloc[row][goveScheme_industry.columns[col+1]]
            data['SchemeType'] = replaceSpaceWithunderScore(
                goveScheme_industry.columns[col+1])
            data['Industry'] = replaceSpaceWithunderScore(
                str(goveScheme_industry.iloc[row][goveScheme_industry.columns[0]]))
            res.append(data)
    jsondata = {'name': 'Government Scheme Three by Industry', 'dataset': res}
    json.dump(jsondata, outputDataFile)

    goveScheme_workforce = getSheet(sheet_num=7, header=28, use_cols="A:H")
    goveScheme_workforce = goveScheme_workforce.head(3)
    res = []
    for row in range(0, len(goveScheme_workforce.index)):
        for col in range(0, len(goveScheme_workforce.columns)-1):
            data = {}
            print(goveScheme_workforce.iloc[row]
                  [goveScheme_workforce.columns[col+1]])
            data['value'] = goveScheme_workforce.iloc[row][goveScheme_workforce.columns[col+1]]
            data['SchemeType'] = replaceSpaceWithunderScore(
                goveScheme_workforce.columns[col+1])
            data['WorkForce'] = replaceSpaceWithunderScore(
                str(goveScheme_workforce.iloc[row][goveScheme_workforce.columns[0]]))
            res.append(data)
    jsondata = {'name': 'Government Scheme Three by WorkForce', 'dataset': res}
    json.dump(jsondata, outputDataFile)


main()
