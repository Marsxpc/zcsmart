*** Settings ***

Library  盐业打码操作.py   WITH NAME  M

Library  盐业打码操作.C301   WITH NAME  C301

Library  盐业打码操作.C302   WITH NAME  C302

Library  盐业打码操作.C303   WITH NAME  C303

Library  盐业打码操作.C304   WITH NAME  C304

Library  盐业打码操作.C305   WITH NAME  C305

Library  盐业打码操作.C306   WITH NAME  C306

Library  盐业打码操作.C307   WITH NAME  C307

Library  盐业打码操作.C308   WITH NAME  C308

Library  盐业打码操作.C309   WITH NAME  C309

Library  盐业打码操作.C310   WITH NAME  C310

Library  盐业打码操作.C311   WITH NAME  C311

Library  盐业打码操作.C312   WITH NAME  C312



*** Test Cases ***

盐业标准-单个产品溯码打码
  [Setup]     C301.setup
  [Teardown]  C301.teardown

  C301.teststeps


盐业标准-产品批量打码
  [Setup]     C302.setup
  [Teardown]  C302.teardown

  C302.teststeps


盐业标准-产品密唯码打码
  [Setup]     C303.setup
  [Teardown]  C303.teardown

  C303.teststeps


盐业标准-产品唯码打码
  [Setup]     C304.setup
  [Teardown]  C304.teardown

  C304.teststeps


盐业标准-单个包装溯码打码
  [Setup]     C305.setup
  [Teardown]  C305.teardown

  C305.teststeps


盐业标准-包装批量打码
  [Setup]     C306.setup
  [Teardown]  C306.teardown

  C306.teststeps


盐业标准-包装唯码打码
  [Setup]     C307.setup
  [Teardown]  C307.teardown

  C307.teststeps


盐业标准-单个流通溯码打码
  [Setup]     C308.setup
  [Teardown]  C308.teardown

  C308.teststeps


盐业标准-流通批量打码
  [Setup]     C309.setup
  [Teardown]  C309.teardown

  C309.teststeps


盐业标准-流通唯码打码
  [Setup]     C310.setup
  [Teardown]  C310.teardown

  C310.teststeps


盐业标准-主体码溯码打码
  [Setup]     C311.setup
  [Teardown]  C311.teardown

  C311.teststeps


盐业标准-主体码唯码打码
  [Setup]     C312.setup
  [Teardown]  C312.teardown

  C312.teststeps
