*** Settings ***

Library  通用打码操作.py   WITH NAME  M

Library  通用打码操作.C201   WITH NAME  C201

Library  通用打码操作.C202   WITH NAME  C202

Library  通用打码操作.C203   WITH NAME  C203

Library  通用打码操作.C204   WITH NAME  C204

Library  通用打码操作.C205   WITH NAME  C205

Library  通用打码操作.C206   WITH NAME  C206

Library  通用打码操作.C207   WITH NAME  C207

Library  通用打码操作.C208   WITH NAME  C208

Library  通用打码操作.C209   WITH NAME  C209

Library  通用打码操作.C210   WITH NAME  C210

Library  通用打码操作.C211   WITH NAME  C211

Library  通用打码操作.C212   WITH NAME  C212



*** Test Cases ***

通用标准-单个产品溯码打码
  [Setup]     C201.setup
  [Teardown]  C201.teardown

  C201.teststeps


通用标准-产品批量打码
  [Setup]     C202.setup
  [Teardown]  C202.teardown

  C202.teststeps


通用标准-产品密唯码打码
  [Setup]     C203.setup
  [Teardown]  C203.teardown

  C203.teststeps


通用标准-产品唯码打码
  [Setup]     C204.setup
  [Teardown]  C204.teardown

  C204.teststeps


通用标准-单个包装溯码打码
  [Setup]     C205.setup
  [Teardown]  C205.teardown

  C205.teststeps


通用标准-包装批量打码
  [Setup]     C206.setup
  [Teardown]  C206.teardown

  C206.teststeps


通用标准-包装唯码打码
  [Setup]     C207.setup
  [Teardown]  C207.teardown

  C207.teststeps


通用标准-单个流通溯码打码
  [Setup]     C208.setup
  [Teardown]  C208.teardown

  C208.teststeps


通用标准-流通批量打码
  [Setup]     C209.setup
  [Teardown]  C209.teardown

  C209.teststeps


通用标准-流通唯码打码
  [Setup]     C210.setup
  [Teardown]  C210.teardown

  C210.teststeps


通用标准-主体码溯码打码
  [Setup]     C211.setup
  [Teardown]  C211.teardown

  C211.teststeps


通用标准-主体码唯码打码
  [Setup]     C212.setup
  [Teardown]  C212.teardown

  C212.teststeps
