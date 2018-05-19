*** Settings ***
Library  /Users/abhaybhargav/Documents/Code/Python/RoboArachni/roboarachni/RoboArachni.py
Library  Collections
Library  REST  http://3a3186c7.ngrok.io  proxies={"http": "http://localhost:9090", "https": "http://localhost:9090"}


*** Variables ***
${TARGET}  http://3a3186c7.ngrok.io

*** Test Cases ***
Initiate ARACHNI
    start arachni docker

Start Proxy
    start arachni proxy  ${TARGET}
    sleep  5

Authenticate to Web Service Arachni
    &{res}=  POST  /login  {"username": "admin", "password": "admin123"}
    Integer  response status  200
    set suite variable  ${TOKEN}  ${res.headers["Authorization"]}

Get Customer by ID
    [Setup]  Set Headers  { "Authorization": "${TOKEN}" }
    GET  /get/2
    Integer  response status  200

Post Fetch Customer
    [Setup]  Set Headers  { "Authorization": "${TOKEN}" }
    POST  /fetch/customer  { "id": 3 }
    Integer  response status  200

Search Customer by Username
    [Setup]  Set Headers  { "Authorization": "${TOKEN}" }
    POST  /search  { "search": "dleon" }
    Integer  response status  200

Initiate Scan
    initiate scan

Scanning
    get scan status

Get Arachni Results
    get results

Kill Arachni
    stop arachni kill container