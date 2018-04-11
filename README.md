
RoboArachni

Robot Framework Library for the Arachni Scanner to perform authenticated scans of an application. Funtionalities of Arachni Rest API Server such as initiating the REST API server, Checking for status of the scan, Initiating scan, Getting results of the scan and stopping of the REST API server can be done with simple nautral language syntax mentioned below. The results of the scan is saved in JSON, XMl and HTML format. Walkthrough of the application prior to scanning can be designed easily using simple keywords available in the selenium library for ROBOT Framework.     


------------------------
Keywords Implemented
------------------------
Initiate the Arachni Rest API Server

|initiate arachni|arachni rest server path|
------------------------
Start the Proxy with host and port as argument

target : The target host URL to be tested.
port : The port to start the listener proxy. 

|start proxy|target|port|
------------------------
Open the App in a browser

|open app|
------------------------
Login to the app with username and password

|Login to App|
------------------------
Initiate the scan after completion of walkthrough

|Initiate Scan|
------------------------
Get status of initiated scan 

|scanning|
------------------------
Get results of the scan

|Get Arachni Results|
------------------------
Stoping Arachni after Completion of the scans

Kill Arachni
------------------------

