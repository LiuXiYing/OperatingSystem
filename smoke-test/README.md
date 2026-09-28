# 流程验证用文件（不是作业）

这个目录是**教师端自动审核流程的冒烟测试**，用来验证：

1. `PR 信息收集`（`pr-check.yml`）能被 PR 触发
2. `PR 自动审核`（`pr-review.yml`）能被上一步的 `workflow_run` 触发（这是最容易静默失败的一环）
3. 审核器能读到 `.github/course-review.yml` 与 `.github/students.yml`
4. 审核结论能回帖到 PR，并按决策类型发邮件

预期结果：PR 作者（教师账号）不在学生名单中，决策为 `MANUAL_REVIEW`，
理由 `UNKNOWN_GITHUB_USER`（未登记 GitHub 账号）。

验证完成后本分支会被删除，PR 会被关闭，**不会合并进 main**。
