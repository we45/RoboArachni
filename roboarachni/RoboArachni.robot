*** Settings ***
Library  RoboArachni.py
Library  Collections
Library  Selenium2Library


*** Variables ***
${PROXY_PORT}  9090
${ARACHNI_PATH}  /home/user/Documents/Tools/arachni-1.5.1-0.5.12/bin/arachni_rest_server
${TARGET}  http://example.com/
${BASE_URL}  http://example.com/
${LOGIN_URL}  http://example.com/login/

*** Test Cases ***
Initiate ARACHNI
    start arachni restserver  ${ARACHNI_PATH}

Start Proxy
    start arachni proxy  ${TARGET}  ${PROXY_PORT}

Open App
    [Tags]  phantomjs
    ${service args}=    Create List    --proxy=127.0.0.1:${PROXY_PORT}
    Create WebDriver  PhantomJS  service_args=${service args}
    go to  ${LOGIN_URL}

Login to App
    [Tags]  login
    input text  username  user@user.com
    input password  password  password
    click button  id=submit
    set browser implicit wait  10
    location should be  ${BASE_URL}dashboard/


Visit Random Pages
    [Tags]  visit
    go to  ${BASE_URL}tests/
    input text  search  something
    click button  name=look
    go to  ${BASE_URL}secure_tests/

Initiate Scan
    initiate scan  ${PROXY_PORT}

Scanning
    get scan status

Get Arachni Results
    get results

Kill Arachni
    delete scan
