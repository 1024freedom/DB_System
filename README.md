# DB_System


# 第一部分：需求分析

## 2.1 需求背景

1.  **传统管理方式低效：**

多数学校仍依赖纸质档案或分散的excel表格管理学生、课程、成绩等数据，存在信息孤岛、重复录入、易出错等问题。

例如：学生选课手工登记，容易导致课程容量超限或时间冲突等问题

1.  **数据协同困难：**

教师、学生、管理人员之间信息传递依赖微信群或线下通知等形式，缺乏效率性和透明度。

例如：学生无法实时查看各种信息，需手动登记考勤等信息

1.  **资源调配问题：**

教室、实验室、实验设备等资源的调配依赖人工协调，效率低下且易出错，同时也容易导致冲突和浪费

1.  **技术与政策支持：**

数据库技术和开发框架的普及，为系统开发提供可靠的技术支持，同时国家的教育信息化政策如：教育部《教育信息化2.0行动计划》提出“构建智慧教育新生态”，要求学校推进数字化管理。

## 2.2 需求概述

1.  **核心目标：**

- 实现教学管理全流程数字化：

将学生信息、课程安排、成绩管理、资源调配等业务迁移到线上，消除纸质流程，提高工作效率。

- 提升数据准确性与安全性：

通过数据库的完整性约束和权限控制等，减少人为的错误与非法操作，减少数据错误的事故的发生概率。

- 支持多角色协同工作：

为教师、学生、管理员提供统一的平台，实现数据共享和高效协作。

- 模块化编程，分层调用：  
    使用python分层调用数据库，实现各种函数的封装，提高项目的可维护性与可扩展性

1.  **运行环境：**

- 操作系统：windows 11 23H2
- 数据库：MySQL 5.7.44版本

1.  **条件与限制：  
    因时间和工程量的原因未实现前端**

**数据库系统中创建各种表名后系统中全显示为小写，导致部分驼峰命名法的表名因系统的默认设置被干扰**

## 2.3角色职责描述

|     |     |     |
| --- | --- | --- |
| 用户  | 职责  | 权限  |
| 学生  | 查看选课记录 | 不可对成绩等核心数据进行操作，可修改自己的联系方式 |
|       | 查询可选课程、进行选课、退选等 |
|       |查看教务信息、预约记录等 |
|       |预约实验室、借用设备或图书 |
| 教师  | 管理所授课程信息（课程名称、学分、教材等）、为学生分配班级 | 仅能操作自己负责的课程相关数据<br><br>不可修改其他教师课程或学生个人信息 |
|       |录入或修改学生成绩、查看成绩警告名单、登记考勤状态。 |
|       |发布作业，设置考试安排 |
|       |预约实验室或教室 |
| 管理员 | 管理所有用户账户（学生、教师、管理员）的增删改查 | 拥有最高权限，但需遵守规则，操作记录需要留痕 |
|        |维护基础数据（班级、教室、教材、设备等） |
|        |监控系统日志、处理异常操作（如删除违规记录） |
|        |生成统计报表（如班级成绩分布、设备借用率） |
|     |     |     |

## 2.4 系统功能模块2.4.1 确定执行者

学生，教师，管理员

## 2.4.2 确定用例

**用例图：**

## 2.4.3 模块文档

|     |     |     |     |
| --- | --- | --- | --- |
| **模块类别** | **功能** | **子功能** | **功能描述** |
| 学生信息管理 | 信息维护 | 新增学生 | 管理员通过表单录入学生学号、姓名、性别等基本信息，数据存入Students表 |
|             |编辑学生信息 | 修改学生联系方式、班级分配（需校验班级容量），更新Students表的对应字段 |
|             |删除学生信息 | 删除学生记录（级联删除关联的数据如选课、成绩等），触发DELETE操作并记录日志 |
|             |批量处理 | 数据导入/导出 | 支持Excel格式批量导入学生信息，或导出所有数据进行备份 |
|             |权限控制 | 学生信息的可见性 | 教师可导出所带班级的学生信息 |
| 课程管理 | 课程维护 | 新增/编辑课程 | 管理员或教师设置课程名称、学分、绑定授课教师，数据存入Courses表 |
|         |课程时间冲突校验 | 排课时检查同一教室同一时间段 是否已被占用 |
|         |教材关联 | 绑定教材 | 为课程指定教材（从Textbooks表中选择），支持一对多关系 |
|         |查询统计 | 课程容量监控 | 实时显示选课人数与课程最大容量，预警超限情况 |
| 选课管理 | 选课操作 | 学生在线选课 | 学生从可选课程列表中选择，系统校验时间冲突和课程容量，写入Enrollments表 |
|          |退课  | 删除选课记录更新Enrollments表 |
|          |查询服务 | 选课记录查询 | 查看选课情况，支持分页 |
|          |冲突处理 | 自动冲突提示 | 检测学生已选课程与新选课程的时间重叠，弹出警告 |
| 成绩管理 | 成绩录入 | 单条成绩录入 | 教师为指定学生和课程输入成绩，校验数值范围（0~100），更新Grades表 |
|         |批量导入成绩 | 通过Excel模板批量上传成绩数据，自动匹配学号和课程 |
|         |统计分析 | 成绩分布可视化 | 生成班级/课程的成绩分布图（如平均分、标准差），支持导出PDF/Excel |
|         |挂科预警 | 自动标记低于及格线的成绩，生成警示名单 |
| 考勤与作业管理 | 考勤登记 | 课堂考勤记录 | 教师按课程登记学生出勤状态（出勤/迟到/缺勤），数据写入Attendance表 |
|               |考勤统计报表 | 生成学生出勤率报表，按学生筛选 |
|               |作业管理 | 作业发布 | 教师设置作业标题、截止时间、满分，数据存入Assignments表 |
| 资源管理 | 实验室预约 | 预约申请 | 教师选择实验室、时间，系统校验冲突后写入LabReservations表 |
|          |预约查询与取消 | 教师查看预约记录，支持取消未开始的预约 |
|          |设备借用 | 借用  | 学生借用设备，更新EquipmentLoans表状态 |
|          |图书借阅 | 借阅登记 | 学生输入学号和书号完成借阅，数据写入BookBorrows表并扣减库存 |
| 权限与日志管理 | 权限控制 | 角色权限分配 | 管理员为用户分配角色（学生/教师/管理员），设置可访问的模块和操作权限 |
|                |动态权限调整 | 通过JSON字段扩展权限（如临时开放实验室预约权限给特定学生） |
|               |日志记录 | 操作日志跟踪 | 记录用户登录、数据修改等操作，存储到SystemLogs表，支持按时间或用户查询 |
|               |数据变更审计 | 通过OperationRecords表跟踪数据变更前后状态，支持回滚误操作 |
|     |     |     |     |
|     |     |     |     |

## 2.5 页面图设计

#### 图1 主页面和用户注册登录页面图

#### 图2 角色菜单页面图

#### 图3 预约管理页面图

#### 图4 借用管理页面图

#### 图5 成绩管理页面图

#### 图6 选课页面图

#### 图7 课程管理页面图

#### 图8 考勤与作业管理页面图

## 2.6 非功能需求

1.  **性能需求**

- **响应时间：**

普通查询操作（如学生查询成绩）响应时间<=1秒

复杂统计（如生成班级成绩报表）响应时间<=5秒

- **并发能力：**

支持100用户同时在线操作，关键功能（选课、成绩录入）支持1000并发请求

- **吞吐量：**

系统峰值处理能力>=200请求/秒

1.  **安全性需求**

- **数据安全：**

敏感信息（如密码）使用哈希加密存储

- **访问控制：**

用户权限严格遵循最小权限原则（如学生不可访问成绩录入功能等）

关键操作（删除数据）需二次确认并记录操作人ip地址

- **防攻击**：防止SQL注入，所有输入字段需做合法性检验

1.  **可用性需求**

- **容错性：**

用户输入错误时，系统需提供明确提示（如“课程容量已满，请重新选择）

1.  **可维护性需求：**

- **日志与监控：**

所有数据库操作记录到OperationRecords表，系统异常时自动发送邮件通知管理员

- **模块化设计：**

功能模块独立开发，数据库调用分层编码（数据访问层、业务逻辑层、表示层），尽量实现各层的高聚合、低耦合，方便后续的优化和功能扩展。

## 2.7 故障处理

1.  **容错设计：**

- **输入容错：**

表单字段自动校验格式（如手机号必须为11位数字）

无效操作拦截（如学生重复选课时提示“已选该课程”）

- **事务管理：**

关键流程（如选课）使用数据库事务，出现异常时支持事务回滚，确保操作原子性

1.  **异常处理：**

- **异常信息显示：**

异常信息逐层抛出，在表示层显示出异常信息

- **异常监控：**

通过SystemLogs表记录错误码、时间、操作人，支持快速定位问题

## 2.8其他需求

1.  **法律与合规性：**

- **数据隐私：**

遵循《个人信息保护法》，学生信息未经授权不得向第三方披露

- **审计合规：**

操作日志保留较长时间，满足教育行业审计要求

1.  **可测试性需求：**

- **测试数据：**

使用工具或程序生成模拟数据（批量生成万条以上记录）

- **测试接口：**

开放测试环境API，支持自动化测试

# 第二部分：概念结构设计

## 3.1 画出整体E-R图

Ps:因页面篇幅问题，部分信息未呈现，图中只呈现了关键信息

# 第三部分：逻辑结构设计

## 关系模型的设计依据

所有关系模型至少符合3NF

**一对一的关系：**

**例如教师与实验室的预约关系，通过另建表的方式将教师唯一标识和实验室唯一标识等相关信息对照联系起来**

**一对多的关系：**

**例如课程与教材的绑定关系，通过外键互指的方式联系起来**

**多对多的关系：**

**例如学生与课程之间的考勤关系，学生与课程之间的选课关系通过另建表的方式储存相关的信息，以ID作为唯一标识，避免数据冗余**

## 4.2 根据E-R图转换成的关系模式

#### 学生表

|     |     |     |
| --- | --- | --- |
| **属性名** | **约束** | **说明** |
| **StudentID** | **primary key auto_increment** | **学生为一标识** |
| **Name** | **NOT NULL** | **姓名** |
| **Gender** | **男或女 NOT NULL** | **性别** |
| **BirthDate** | **NOT NULL** | **出生日期** |
| **Phone** | **UNIQUE** | **联系电话** |
| **ClassID** | **INDEX \`idx_class\` (\`ClassID\`),**<br><br>**CONSTRAINT \`fk_student_class\` FOREIGN KEY (\`ClassID\`) REFERENCES \`Classes\` (\`ClassID\`)**<br><br>**ON DELETE SET NULL** | **所属班级ID** |

#### 2.教师表

|     |     |     |
| --- | --- | --- |
| **属性名** | **约束** | **说明** |
| **TeacherID** | **primary key auto_increment** | **教师唯一标识** |
| **Name** | **NOT NULL** | **姓名** |
| **Title** |     | **职称** |

#### 3.课程表

|     |     |     |
| --- | --- | --- |
| **属性名** | **约束** | **说明** |
| **CourseID** | **primary key auto_increment** | **课程唯一标识** |
| **CourseName** | **NOT NULL** | **课程名称** |
| **Credit** | **NOT NULL** | **学分** |
| **TeacherID** | **INDEX \`idx_teacher\` (\`TeacherID\`),**<br><br>**CONSTRAINT \`fk_course_teacher\`**<br><br>**FOREIGN KEY (\`TeacherID\`) REFERENCES \`Teachers\` (\`TeacherID\`)**<br><br>**ON DELETE SET NULL** | **授课教师ID** |
| **Capacity** | **DEFAULT 150** | **课程容量** |
| **Day** | **tinyint NOT NULL** | **（1-7）对应周一到周日** |
| **StartTime** | **time NOT NULL** | **课程开始时间** |
| **EndTime** | **time NOT NULL** | **课程结束时间** |

#### 4.班级表

|     |     |     |
| --- | --- | --- |
| **属性名** | **约束** | **说明** |
| **ClassID** | **primary key auto_increment** | **班级唯一标识** |
| **ClassName** | **NOT NULL** | **班级名称** |
| **Major** | **NOT NULL** | **所属专业** |
| **Capacity** | **DEFAULT 40** | **班级最大容量** |
| **CapacityNow** | **DEFAULT 0** | **班级当前已容纳的学生** |

#### 5.教室表

|     |     |     |
| --- | --- | --- |
| **属性名** | **约束** | **说明** |
| **ClassroomID** | **primary key auto_increment** | **教室唯一标识** |
| **Location** | **NOT NULL** | **教室位置** |
| **Type** | **普通教室或实验室** | **教室类型** |
| **Capacity** | **NOT NULL** | **最大容量** |

#### 6.教材表

|     |     |     |
| --- | --- | --- |
| **属性名** | **约束** | **说明** |
| **TextbookID** | **primary key auto_increment** | **教材唯一标识** |
| **Title** | **NOT NULL** | **教材名称** |
| **Author** | **NOT NULL** | **作者** |
| **Publisher** |     | **出版社** |
| **CourseID** | **INDEX \`idx_course\` (\`CourseID\`),**<br><br>**CONSTRAINT \`fk_textbook_course\`**<br><br>**FOREIGN KEY (\`CourseID\`) REFERENCES \`Courses\` (\`CourseID\`)**<br><br>**ON DELETE SET NULL** | **关联课程ID** |

#### 7.选课表

|     |     |     |
| --- | --- | --- |
| **属性名** | **约束** | **说明** |
| **EnrollmentID** | **primary key auto_increment** | **选课记录ID** |
| **StudentID** | **NOT NULL**<br><br>**INDEX \`idx_student\` (\`StudentID\`),**<br><br>**CONSTRAINT \`fk_enrollment_student\`**<br><br>**FOREIGN KEY (\`StudentID\`) REFERENCES \`Students\` (\`StudentID\`)**<br><br>**ON DELETE CASCADE,** | **学生ID** |
| **CourseID** | **NOT NULL**<br><br>**INDEX \`idx_course\` (\`CourseID\`),**<br><br>**CONSTRAINT \`fk_enrollment_course\`**<br><br>**FOREIGN KEY (\`CourseID\`) REFERENCES \`Courses\` (\`CourseID\`)**<br><br>**ON DELETE CASCADE** | **课程ID** |

#### 8.成绩表

|     |     |     |
| --- | --- | --- |
| **属性名** | **约束** | **说明** |
| **GradeID** | **primary key auto_increment** | **成绩记录ID** |
| **StudentID** | **NOT NULL**<br><br>**INDEX \`idx_student_course\` (\`StudentID\`, \`CourseID\`),**<br><br>**CONSTRAINT \`fk_grade_student\`**<br><br>**FOREIGN KEY (\`StudentID\`) REFERENCES \`Students\` (\`StudentID\`)**<br><br>**ON DELETE CASCADE,** | **学生ID** |
| **CourseID** | **NOT NULL**<br><br>**CONSTRAINT \`fk_grade_course\`**<br><br>**FOREIGN KEY (\`CourseID\`) REFERENCES \`Courses\` (\`CourseID\`)**<br><br>**ON DELETE CASCADE** | **课程ID** |
| **Score** |     | **成绩** |
|     |     |     |

#### 9.考勤表

|     |     |     |
| --- | --- | --- |
| **属性名** | **约束** | **说明** |
| **AttendanceID** | **primary key auto_increment** | **考勤记录ID** |
| **StudentID** | **NOT NULL** | **学生ID** |
| **CourseID** | **NOT NULL** | **课程ID** |
| **Date** | **NOT NULL** | **考勤日期** |
| **Status** | **出勤/迟到/缺勤** | **考勤状态** |

#### 10.作业表

|     |     |     |
| --- | --- | --- |
| **属性名** | **约束** | **说明** |
| **AssignmentID** | **primary key auto_increment** | **作业ID** |
| **CourseID** | **NOT NULL** | **关联课程ID** |
| **Title** | **NOT NULL** | **作业标题** |
| **Deadline** | **NOT NULL** | **提交截止时间** |
| **MaxScore** | **DEFAULT 100** | **作业满分** |

#### 11.考试安排表

|     |     |     |
| --- | --- | --- |
| **属性名** | **约束** | **说明** |
| **ExamID** | **primary key auto_increment** | **考试ID** |
| **CourseID** | **NOT NULL** | **关联课程ID** |
| **ClassroomID** | **NOT NULL** | **考场ID** |
| **StartTime** | **DATETIME NOT NULL** | **考试开始时间** |
| **EndTime** | **DATETIME NOT NULL** | **考试结束时间** |

#### 12.实验室预约表

|     |     |     |
| --- | --- | --- |
| **属性名** | **约束** | **说明** |
| **ReservationID** | **primary key auto_increment** | **预约ID** |
| **TeacherID** | **NOT NULL**<br><br>**INDEX \`idx_teacher\` (\`TeacherID\`),**<br><br>**CONSTRAINT \`fk_reservation_teacher\`**<br><br>**FOREIGN KEY (\`TeacherID\`) REFERENCES \`Teachers\` (\`TeacherID\`)**<br><br>**ON DELETE CASCADE,** | **预约教师ID** |
| **LabID** | **NOT NULL**<br><br>**INDEX \`idx_lab\` (\`LabID\`),**<br><br>**CONSTRAINT \`fk_reservation_lab\`**<br><br>**FOREIGN KEY (\`LabID\`) REFERENCES \`Classrooms\` (\`ClassroomID\`)**<br><br>**ON DELETE CASCADE** | **实验室ID** |
| **StartTime** | **DATETIME NOT NULL** | **预约开始时间** |
| **EndTime** | **DATETIME NOT NULL** | **预约结束时间** |

#### 13.设备借用表

|     |     |     |
| --- | --- | --- |
| **属性名** | **约束** | **说明** |
| **LoanID** | **primary key auto_increment** | **借用记录ID** |
| **StudentID** | **NOT NULL**<br><br>**INDEX \`idx_student\` (\`StudentID\`),**<br><br>**CONSTRAINT \`fk_loan_student\`**<br><br>**FOREIGN KEY (\`StudentID\`) REFERENCES \`Students\` (\`StudentID\`)**<br><br>**ON DELETE CASCADE** | **借用人ID** |
| **EquipmentID** | **NOT NULL** | **设备ID** |
| **BorrowDate** | **NOT NULL** | **借用日期** |
| **ReturnDate** |     | **归还日期** |

#### 14.图书借阅表

|     |     |     |
| --- | --- | --- |
| **属性名** | **约束** | **说明** |
| **BorrowID** | **primary key auto_increment** | **借阅ID** |
| **StudentID** | **NOT NULL**<br><br>**INDEX \`idx_student\` (\`StudentID\`),**<br><br>**CONSTRAINT \`fk_borrow_student\`**<br><br>**FOREIGN KEY (\`StudentID\`) REFERENCES \`Students\` (\`StudentID\`)**<br><br>**ON DELETE CASCADE** | **借阅人ID** |
| **BookID** | **NOT NULL** | **图书ID** |
| **BorrowDate** | **NOT NULL** | **借阅日期** |
| **DueDate** | **NOT NULL** | **应还日期** |

#### 15.用户权限表

|     |     |     |
| --- | --- | --- |
| **属性名** | **约束** | **说明** |
| **UserID** | **Primary key** | **用户ID（关联学生/教师表）** |
| **Role** | **学生/教师/管理员** | **角色** |
| **Permissions** | **JSON** | **权限列表（JSON格式存储权限树结构）** |
| **Password** | **NOT NULL** | **密码** |

#### 16.权限树表

|     |     |     |
| --- | --- | --- |
| **属性名** | **约束** | **说明** |
| **PermissionID** | **VARCHAR(50) PRIMARY KEY** | **权限唯一标识符** |
| **ParentID** | **VARCHAR(50) DEFAULT NULL**<br><br>**FOREIGN KEY (ParentID) REFERENCES PermissionTree(PermissionID) ON DELETE CASCADE** | **父节点ID** |
| **Name** | **VARCHAR(100) NOT NULL** | **权限名称** |
| **Description** | **TEXT** | **权限描述** |
| **Type** | **Module/Page/action** | **节点类型** |
|     |     |     |
|     |     |     |

#### 17.角色默认权限表

|     |     |     |
| --- | --- | --- |
| **属性名** | **约束** | **说明** |
| **Role** | **学生/教师/管理员** | **角色** |
| **DefaultPermissions** | **JSON** | **默认权限列表（JSON格式存储权限树结构）** |
|     |     |     |

#### 18.系统日志表

|     |     |     |
| --- | --- | --- |
| **属性名** | **约束** | **说明** |
| **LogID** | **primary key auto_increment** | **日志ID** |
| **UserID** | **NOT NULL** | **操作用户ID** |
| **Action** | **NOT NULL** | **操作类型（如插入、删除）** |
| **Timestamp** | **DEFAULT CURRENT_TIMENSTAMP** | **操作时间** |
| **Details** |     | **操作详情** |

#### 19.操作记录表

|     |     |     |
| --- | --- | --- |
| **属性名** | **约束** | **说明** |
| **RecordID** | **primary key auto_increment** | **记录ID** |
| **TableName** | **NOT NULL** | **操作的表名** |
| **OperationType** | **INSERT/UPDATE/DELETE** | **操作类型** |
| **OldData** | **JSON** | **操作前数据** |
| **NewData** | **JSON** | **操作后数据** |
| **Timestamp** | **DEFAULT CURRENT_TIMENSTAMP** | **操作时间** |

#### 20.图书表

|     |     |     |
| --- | --- | --- |
| **属性名** | **约束** | **说明** |
| **BookID** | **primary key auto_increment** | **图书ID** |
| **BookName** | **NOT NULL** | **图书名** |
| **Author** | **NOT NULL** | **作者** |
| **Publisher** | **NOT NULL** | **出版社** |
| **Reserve** | **NOT NULL** | **库存** |

#### 21.设备表

|     |     |     |
| --- | --- | --- |
| **属性名** | **约束** | **说明** |
| **EquipmentID** | **primary key auto_increment** | **设备ID** |
| **EquipmentName** | **NOT NULL** | **设备名** |
| **Reserve** | **NOT NULL** | **库存** |

## 4.3数据库调用分层编码设计

**分层设计：**

- **Cli:表示层** 用户交互、菜单显示、输入验证、结果显示、调用services层 ，接收并显示异常信息
- **Services：业务逻辑层** 业务规则处理、事务协调、调用Dao层，接收并抛出异常信息
- **Dao：数据操作层** 纯数据操作 SQL执行、分页处理、基础CRUD操作，抛出异常
- **项目结构概览**

以“学生选课”、“课程容量监控”和“操作记录表”为例说明：

- 学生选课

- 课程容量监控

- 操作记录

## 4.4 代码实现

### 4.4.1表中输入的记录

使用python脚本生成模拟数据，插入基本信息表中，因其他表的数据是基于基本表产生的，故未生成剩余其他表的模拟数据

模拟数据生成测试结果图：

### 4.4.2其他模块：

- **数据库连接使用连接池提高性能**

- **安全工具**

- **一些可共用的数据操作类：（分页查询，查找，获取）**
