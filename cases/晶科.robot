*** Settings ***

Library  晶科.py   WITH NAME  M

Library  晶科.C001   WITH NAME  C001



*** Test Cases ***

接口-码印刷
  [Tags]    smoke
  [Setup]     C001.setup
  [Teardown]  C001.teardown

  C001.teststeps
