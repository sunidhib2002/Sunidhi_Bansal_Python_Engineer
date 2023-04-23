# -*- coding: utf-8 -*-
"""
@author: Abhilash Raj

Unit Testing module for Steel Eye Assigment
"""

import unittest
from XML_Parser import *
import os
import xmltodict


class TestXMLParser(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        """
        Class method calls once at the beginning of unit test
        """
        # loading the configuration
        config = load_config()
        # Extracting the required s3 information from config
        self.bucket_name = config["bucket_name"]
        self.aws_access_key_id = config["aws_access_key_id"]
        self.aws_secret_access_key = config["aws_secret_access_key"]
        self.region_name = config["region_name"]
        self.s_bucket = initialize_s3_bucket(self.aws_access_key_id, self.aws_secret_access_key, self.region_name, self.bucket_name)

    def test_bucket(self):
        """Function to check whether the S3 Bucket exists or not"""
        self.assertIsNotNone(self.s_bucket, "Bucket is NONE")

    def download(self):
        self.s_bucket.download_file(Key='DLTINS_20210117_01of01.xml', Filename='DLTINS_20210117_01of01.xml')
        if os.path.exists("DLTINS_20210117_01of01.xml"):
            return "True"
        else:
            return "False"

    def test_download(self):
        """Function to test download function"""

        # Test for all correct data
        self.assertEqual(self.download(), "True", "File downloaded successfully")

    def read_data(self, file_name):
        data_dict = None
        if os.path.exists(file_name):
            with open(file_name, "r", encoding = "utf-8") as file:
                file_data = file.read()

            # parsing the xml file and converting it to the python dictionary
            data_dict = xmltodict.parse(file_data)
        return data_dict

    def test_parse_xml_data(self):
        """Function to test parse_xml_data function"""
        # Test for correct data
        # Path to original source file
        file = "DLTINS_20210117_01of01.xml"
        testcase_1 = parse_xml_data(self.read_data(file))
        self.assertEqual(len(testcase_1[0]), )
        self.assertEqual(len(testcase_1[1]), )

        # Test for incorrect data
        # Path of random source file
        not_file = "SomeRandomFile.xml"
        testcase_2 = parse_xml_data(self.read_data(not_file))
        self.assertEqual(len(testcase_2[0]), 0)
        self.assertEqual(len(testcase_2[1]), 0)

    def test_create_csv(self):
        """Function to test create_csv funtion"""
        success_flag = False
        file = "DLTINS_20210117_01of01.xml"
        ls1, ls2 = parse_xml_data(self.read_data(file))

        csv_file = "Parsed_DLTINS_20210117_01of01.csv"
        create_csv(ls1, ls2)
        if os.path.exists(csv_file):
            success_flag = True
        # Test for correct data
        self.assertTrue(success_flag)

    def aws_s3_upload(self, filename):
        try:
            self.s_bucket.upload_file(Filename=filename, Key=filename)
            return True
        except Exception as e:
            return False

    def test_aws_s3_upload(self):
        """Function to test aws_s3_upload function"""
        
        # Test for correct file
        csv_file = "Parsed_DLTINS_20210117_01of01.csv"
        self.assertTrue(self.aws_s3_upload(csv_file))

        # Test for non existent file
        csv_file_tc2 = "SomeRandomFile.csv"
        self.assertFalse(self.aws_s3_upload(csv_file_tc2))


if __name__ == "__main__":
    unittest.main()
