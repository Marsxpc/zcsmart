*** Settings ***

Library  药业打码操作.py   WITH NAME  M

Library  药业打码操作.C401   WITH NAME  C401

Library  药业打码操作.C402   WITH NAME  C402

Library  药业打码操作.C403   WITH NAME  C403



*** Test Cases ***

药业标准-产品批量打码
  [Setup]     C401.setup
  [Teardown]  C401.teardown

  C401.teststeps


药业标准-包装批量打码
  [Setup]     C402.setup
  [Teardown]  C402.teardown

  C402.teststeps


药业标准-流通批量打码
  [Setup]     C403.setup
  [Teardown]  C403.teardown

  C403.teststeps
