
RoboArachni

Robot Framework Library for the Arachni Scanner to perform authenticated scans of an application. Funtionalities of Arachni Rest API Server such as initiating the REST API server, Checking for status of the scan, Initiating scan, Getting results of the scan and stopping of the REST API server can be done with simple nautral language syntax mentioned below. The results of the scan is saved in JSON, XMl and HTML format. Walkthrough of the application prior to scanning can be designed easily using simple keywords available in the selenium library for ROBOT Framework.

## Installation Instructions
* You will need the Arachni Docker Image. Can be found here: https://hub.docker.com/r/arachni/arachni/
* `docker pull arachni/arachni`
* Git clone this repo and install deps with `python setup.py install`

------------------------
Keywords Implemented
------------------------
Initiate the Arachni Service as a Docker Container

`| Library  | RoboArachni | rest_port = 7331 (optional/default) |  proxy_port=9090 (optional/default)  | arachni_username = "arachni" (optional/default)  |  arachni_pw = "password" (optional/default)  |`

`| start arachni docker  |`
------------------------
Starts the Arachni as a Docker Container


`| start_arachni_proxy |`
-------------------------
Starts Arachni Proxy on default port 9090


`| get arachni scanid  |`
-------------------------
Gets the Arachni Scan ID when the proxy runs

|initiate Scan|
---------------
Get status of initiated scan 

`| get scan status|`
--------------------
Get results of the scan

`|get arachni results|`
-----------------------
Writes Arachni JSON results to the localpath

`stop arachni kill container`
-----------------------------
Stops the Arachni Docker container