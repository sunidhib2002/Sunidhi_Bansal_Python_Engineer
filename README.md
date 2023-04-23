<h2>About the Task:</h2>

<h4>XML TO CSV:</h4>
XML to CSV is done using the XML_Parser.py file. The conversion is done using xmltodict python library.
<h4>Pydoc:</h4>
For the documentation, I used Pydoc and generated XML_Parser.html
<h4>Unit Testing:</h4>
For unit testing, I wrote Unit_test.py script. 
<h4>Python Script to run as AWS Lambda function:</h4>
aws_xml_parser.py file was used to run the python script as Lambda function.
<h5>I uploaded the csv file in AWS S3 bucket.</h5>
<img src = "https://github.com/sunidhib2002/Sunidhi_Bansal_Python_Engineer/blob/main/Images/Bucket.PNG">
<h5>I tried the setting the lambda function, but that didnot run properly. It gave the ModuleNameError.</h5>
<h5>Creation of Lambda function:</h5>
<img src = "https://github.com/sunidhib2002/Sunidhi_Bansal_Python_Engineer/blob/main/Images/lambda.PNG">
<h5>Python Script uploaded on AWS</h5>
<img src = "https://github.com/sunidhib2002/Sunidhi_Bansal_Python_Engineer/blob/main/Images/lambd_fn.PNG">
<h5>I tried importing the necessary library by creating a layer in Lambda. But it didnot work.</h5>
<img src = "https://github.com/sunidhib2002/Sunidhi_Bansal_Python_Engineer/blob/main/Images/layer.PNG">
