import pandas as pd


def replaceSpaceWithunderScore(string):
    if string == " < 250 ":
        string = "WorkforceSizeLessThan250"
    if string == " 250 +":
        string = "WorkforceSize250More"
    if string == "All Size Bands":
        string = "Total"

    string = string.replace(",", "").replace(" ", "").replace(";", "")
    string = string.lower()
    string = string.capitalize()
    return string


def getSheet(sheet_num, header, use_cols):
    Sheet = pd.read_excel(
        "CW1-BusinessImpactsOfCovid19Data.xlsx", sheet_name=sheet_num, header=header, usecols=use_cols)

    return Sheet

# remove notes from array


def remove_notes(sheet, indexes):
    sheet = sheet.drop(indexes)
    return sheet


def main():
    sample_size = getSheet(2, 3, "A:D")
    sample_size = remove_notes(sample_size, indexes=sample_size.index[16:24])
    # industries = sample_size.Industry

    # printSchemaFile()
    printDataFile(sample_size, filename="Sample_Size.ttl")
    printWorkForceToDataFile(filename="Sample_Size.ttl")
    printDataSet("Total Number of Survey Sent Out", sample_size,
                 filename="Sample_Size.ttl", ds="ds1")
    printDataPoint(sample_size, filename="Sample_Size.ttl", ds="ds1")

    num_responses = getSheet(sheet_num=3, header=3, use_cols="A:D")
    num_responses = num_responses.head(13)

    printDataFile(num_responses, filename="NumberOfResponse.ttl")

    printWorkForceToDataFile(filename="NumberOfResponse.ttl")
    printDataSet("Number of Responses", num_responses,
                 filename="NumberOfResponse.ttl", ds="ds3")
    printDataPoint(num_responses, filename="NumberOfResponse.ttl", ds="ds3")

    proportion_responses = getSheet(sheet_num=3, header=3, use_cols="G:J")
    proportion_responses = proportion_responses.head(13)

    proportion_responses.columns = num_responses.columns

    print(proportion_responses)

    printDataFile(proportion_responses, filename="ProportionOfResponse.ttl")
    printWorkForceToDataFile(filename="ProportionOfResponse.ttl")
    printDataSet("Proportion of Responses", proportion_responses,
                 filename="ProportionOfResponse.ttl", ds="ds3")
    printDataPoint(
        proportion_responses, filename="ProportionOfResponse.ttl", ds="ds3")


def printSchemaFile(filename):
    # namespace
    print('hello')
    outputSchemaFile = open(filename, "w")
    outputSchemaFile.write(
        "@prefix : <http://enakting.org/schema/Survey/> .\n")
    outputSchemaFile.write(
        "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n")
    outputSchemaFile.write(
        "@prefix dc: <http://purl.org/dc/elements/1.1/> ./n")
    outputSchemaFile.write("@prefix owl: <http://www.w3.org/2002/07/owl#> .\n")
    outputSchemaFile.write(
        "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n")
    outputSchemaFile.write(
        "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n")
    outputSchemaFile.write(
        "@prefix qb: <http://purl.org/linked-data/cube#> http://purl.org/linked-data/cube#> .\n")

    outputSchemaFile.write("#Dimension - row\n")
    outputSchemaFile.write(
        ":Industry rdfs:subClassOf qb:Dimension;\n")
    outputSchemaFile.write(
        " \t dc:title \"Industry\". \n")

    outputSchemaFile.write("#Dimensions - columns\n")
    outputSchemaFile.write(":WorkForce rdf:type owl:Class ;\n")
    outputSchemaFile.write("\t rdfs:subClassOf qb:Dimension .\n")

    outputSchemaFile.write("#Dimensions - columns\n")
    outputSchemaFile.write(":Country rdf:type owl:Class ;\n")
    outputSchemaFile.write("\t rdfs:subClassOf qb:Dimension .\n")


def printDataFile(sheet, filename):
    print('hello')
    outputDataFile = open(filename, 'w')
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

    for index, row in sheet.iterrows():
        outputDataFile.write(
            ':'+replaceSpaceWithunderScore(row["Industry"]) + ' rdf:type survey:Industry;\n     dc:title '+'"'+row["Industry"]+'"'+'.\n')
        outputDataFile.write("\n")


def printWorkForceToDataFile(filename):
    outputDataFile = open(filename, 'a')
    outputDataFile.write(
        ':'+'0-99' + ' rdf:type survey:WorkForce;\n     dc:title '+'"'+'WorkForceSize 0-99'+'"'+'.\n')
    outputDataFile.write("\n")
    outputDataFile.write(
        ':'+'100-249' + ' rdf:type survey:WorkForce;\n     dc:title '+'"'+'WorkForceSize 100-249'+'"'+'.\n')
    outputDataFile.write("\n")
    outputDataFile.write(
        ':'+'Lessthan250' + ' rdf:type survey:WorkForce;\n     dc:title '+'"'+'WorkForceSize <250'+'"'+'.\n')
    outputDataFile.write("\n")
    outputDataFile.write(
        ':'+'250andMore' + ' rdf:type survey:WorkForce;\n     dc:title '+'"'+'WorkForceSize 250+'+'"'+'.\n')
    outputDataFile.write("\n")
    outputDataFile.write(
        ':'+'Total' + ' rdf:type survey:WorkForce;\n     dc:title '+'"'+'Total'+'"'+'.\n')
    outputDataFile.write("\n")


def printDataSet(table_name, table, filename, ds):
    outputDataFile = open(filename, 'a')
    outputDataFile.write("#Dataset\n")
    outputDataFile.write(":"+ds+" rdf:type qb:dataset;\n")
    outputDataFile.write(
        '\t dc:title' + '"'+table_name + '"' + ';')
    outputDataFile.write("\n")

    for row in range(1, len(table.index)+1):
        for col in range(1, len(table.columns)):
            if row == len(table.index)+1 and col == len(table.columns):
                outputDataFile.write("     qb:observation :"+ds +
                                     "_"+str(row)+"_"+str(col)+".\n")
            else:
                outputDataFile.write("     qb:observation :"+ds +
                                     "_"+str(row)+"_"+str(col)+";\n")


def printDataPoint(table, filename, ds):
    outputDataFile = open(filename, 'a')
    for row in range(0, len(table.index)-1):
        for col in range(0, len(table.columns)-1):
            outputDataFile.write(":"+ds+"_"+str(row+1)+"_"+str(col+1) +
                                 " rdf:type qb:observation;\n")
            outputDataFile.write(
                "      rdf:value "+str(table.iloc[row][table.columns[col+1]])+";\n")

            if table.columns[col+1] == "Workforce Size < 250":
                outputDataFile.write(
                    "      qb:DimensionProperty "+":Lessthan250;\n")
            elif table.columns[col+1] == "Workforce Size 250 +":
                outputDataFile.write(
                    "      qb:DimensionProperty "+":250andMore;\n")
            else:
                outputDataFile.write("      qb:DimensionProperty "+":Total;\n")

            outputDataFile.write("      qb:DimensionProperty " + ":" +
                                 replaceSpaceWithunderScore(str(table.iloc[row][table.columns[0]]))+".\n")

            outputDataFile.write("\n")


main()


#  rdf:value 55,094;
# 	 scovo:dataset :ds1;
# 	 scovo:dimension :Total;
# 	 scovo:dimension :Cleveland;
# 	 scovo:dimension :TP2008_09.
