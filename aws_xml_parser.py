def lambda_handler(event, context):
    # TODO implement
    main()
    return {
        'statusCode': 200,
        # 'body': json.dumps('Hello from Lambda!')
    }
# importing important libraries 
import csv
import xmltodict
import logging
import boto3
import configparser
import os

logging.getLogger().setLevel(logging.INFO)
FILE_PATH = 'config.cfg'

#This function is used for loading the config file and get necessary credetial details from AWS, like the S3 bucket name, access key, secret access key, etc.
def load_config():
    config = configparser.ConfigParser()
    config.read(FILE_PATH)
    return {'bucket_name' : config.get("AWS", "BUCKET_NAME"),
    'aws_access_key_id' : config.get("AWS", "ACCESS_KEY"),
    'aws_secret_access_key' : config.get("AWS", "SECRET_ACCESS_KEY"),
    'region_name' : config.get("AWS", "REgION_NAME")}

# This function is used for initializing the s3 bucket from where we want to access the XML file.
def initialize_s3_bucket(access_key, secret_access_key, region, bucket_name):
    s3 = boto3.resource(
        service_name = 's3',
        region_name = region,
        aws_access_key_id = access_key,
        aws_secret_access_key = secret_access_key
    )
    if bucket_name in s3.buckets.all():
        return s3.Bucket(bucket_name)
    else:
        logging.error("S3 Bucket not found")
        return None

# This function is used for identifying different tags in the XML file and check its structure.
def validate_xml_structure(data_dict):
    logging.info("Validating the XML structure")
    if 'BizData' in data_dict.keys():
        if 'Pyld' in data_dict['BizData'].keys():
            if 'Document' in data_dict['BizData']['Pyld'].keys():
                if 'FinInstrmRptgRefDataDltaRpt' in data_dict['BizData']['Pyld']['Document'].keys():
                    if 'FinInstrm' in data_dict['BizData']['Pyld']['Document']['FinInstrmRptgRefDataDltaRpt'].keys():
                        return True
    return False

# This is used for validating the xml structure and parsing the file to extract the required information.
def parse_xml_data(data_dict):
    logging.info("Parsing the XML data")
    success = True
    if validate_xml_structure(data_dict):
        logging.info("XML structure validated successfully, data parsing starting now..")
        list_item = data_dict['BizData']['Pyld']['Document']['FinInstrmRptgRefDataDltaRpt']['FinInstrm']
        data = []
        data_issr = []
        for element in list_item:
            if 'TermntdRcrd' in element.keys():
                if 'FinInstrmGnlAttrbts' in element['TermntdRcrd'] and 'Issr' in element['TermntdRcrd']:
                    data.append(element['TermntdRcrd']['FinInstrmGnlAttrbts'])
                    data_issr.append(element['TermntdRcrd']['Issr'])
                else:
                    success = False
                    break
            elif 'ModfdRcrd' in element.keys():
                if 'FinInstrmGnlAttrbts' in element['ModfdRcrd'] and 'Issr' in element['ModfdRcrd']:
                    data.append(element['ModfdRcrd']['FinInstrmGnlAttrbts'])
                    data_issr.append(element['ModfdRcrd']['Issr'])
                else:
                    success = False
                    break
            elif 'NewRcrd' in element.keys():
                if 'FinInstrmGnlAttrbts' in element['NewRcrd'] and 'Issr' in element['NewRcrd']:
                    data.append(element['NewRcrd']['FinInstrmGnlAttrbts'])
                    data_issr.append(element['NewRcrd']['Issr'])
                else:
                    success = False
                    break
    else:
        success = False

    if (success == False):
        logging.error("Please verify your xml structure")
        return [], []

    return data, data_issr


# This function is used for creating the csv file from the extracted data.
def create_csv(data, data_issr):
    # defining the header for the csv file
    logging.info("Creating the csv file")
    headers = ["FinInstrmGnlAttrbts.Id", "FinInstrmGnlAttrbts.FullNm", "FinInstrmGnlAttrbts.ClssfctnTp", "FinInstrmGnlAttrbts.CmmdtyDerivInd", "FinInstrmGnlAttrbts.NtnlCcy", "Issr"]
    rows = []
    i = 0
    for element in data:
        id = element['Id']
        name = element['FullNm']
        clssfctnTp = element['ClssfctnTp']
        NtnlCcy = element['NtnlCcy']
        CmmdtyDerivInd = element['CmmdtyDerivInd']
        issr = data_issr[i]
        i += 1

        rows.append([id, name, clssfctnTp, CmmdtyDerivInd, NtnlCcy, issr])
    
    with open('Parsed_DLTINS_20210117_01of01.csv', 'w',newline="") as f:
        write = csv.writer(f)
        write.writerow(headers)
        write.writerows(rows)

# This the main function from where call all the other functions.
def main():
    
    configurations = load_config()
    s3_bucket = initialize_s3_bucket(configurations['aws_access_key_id'], configurations['aws_secret_access_key'], configurations['region_name'], configurations['bucket_name'])

    if s3_bucket is not None: 
        # opening the xml file in read mode with utf-8 encoding method to read the data inside the file.
        s3_bucket.download_file(Key='DLTINS_20210117_01of01.xml', Filename='DLTINS_20210117_01of01.xml')
        if os.path.exists("DLTINS_20210117_01of01.xml"):
            with open("DLTINS_20210117_01of01.xml", "r", encoding = "utf-8") as file:
                file_data = file.read()

            # parsing the xml file and converting it to the python dictionary
            data_dict = xmltodict.parse(file_data)
            
            data, data_issr = parse_xml_data(data_dict)
            if len(data) > 0 and len(data_issr) > 0:
                create_csv(data, data_issr)
                s3_bucket.upload_file(Filename='Parsed_DLTINS_20210117_01of01.csv', Key='Parsed_DLTINS_20210117_01of01.csv')
            else: 
                logging.error("Parsed data not returned")
        else:
            logging.error("Some Error in downloading the file")
    else:
        logging.error("Bucket not found")

if __name__ == '__main__':
    main()

