*** Settings ***

Library  湘蘅.py   WITH NAME  M

Library  湘蘅.C101   WITH NAME  C101

Library  湘蘅.C102   WITH NAME  C102

Library  湘蘅.C103   WITH NAME  C103

Library  湘蘅.C104   WITH NAME  C104

Library  湘蘅.C105   WITH NAME  C105



*** Test Cases ***

接口-新灌装
  [Setup]     C101.setup
  [Teardown]  C101.teardown

  C101.teststeps


接口-新入库
  [Setup]     C102.setup
  [Teardown]  C102.teardown

  C102.teststeps


接口-新出库
  [Setup]     C103.setup
  [Teardown]  C103.teardown

  C103.teststeps


接口-移库
  [Setup]     C104.setup
  [Teardown]  C104.teardown

  C104.teststeps


接口-查询码是否已记录
  [Setup]     C105.setup
  [Teardown]  C105.teardown

  C105.teststeps
