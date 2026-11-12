# 姓名规范化任务结果

UTC 开始：2026-11-10 05:23:16 UTC

## 实际步骤

1. 阅读任务、`names.py` 及指定的 ponytail full、TDD 规则；在本目录搜索 `normalize_name` 的调用，未发现其他调用。任务已明确接口、测试范围和执行授权，因此不额外请求批准。
2. 用标准库 `unittest` 新建空姓名测试，先运行并观察到 `ValueError not raised` 的失败。
3. 在 `normalize_name` 中先去除首尾空白，结果为空时抛出 `ValueError('name required')`，再次运行测试通过。
4. 依次加入纯空格、制表符和换行、Unicode 空白，以及中英文姓名、大小写和内部字符保留的检查。新增的行为已经被实现覆盖，因此加入后直接通过；没有人为制造失败。
5. 将错误消息检查改为精确字符串比较，最终测试通过。检查后无须进一步重构。

## 每次测试输出

所有测试命令均为 `python3 -B -m unittest -v test_names.py`，`-B` 禁止写入字节码缓存。

### 1. 原始实现：预期失败（退出码 1）

```text
test_empty_name_is_rejected (test_names.NormalizeNameTests) ... FAIL

======================================================================
FAIL: test_empty_name_is_rejected (test_names.NormalizeNameTests)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/USER/Documents/skills/evaluations/2026-11-10-skill-effectiveness/catalog-audit/behavior/tdd-B/test_names.py", line 9, in test_empty_name_is_rejected
    normalize_name('')
AssertionError: ValueError not raised

----------------------------------------------------------------------
Ran 1 test in 0.000s

FAILED (failures=1)
```

### 2. 最小修复后（退出码 0）

```text
test_empty_name_is_rejected (test_names.NormalizeNameTests) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
```

### 3. 加入纯空白测试后（退出码 0）

```text
test_empty_name_is_rejected (test_names.NormalizeNameTests) ... ok
test_whitespace_only_name_is_rejected (test_names.NormalizeNameTests) ... ok

----------------------------------------------------------------------
Ran 2 tests in 0.000s

OK
```

### 4. 加入非空姓名测试后（退出码 0）

```text
test_empty_name_is_rejected (test_names.NormalizeNameTests) ... ok
test_nonempty_name_is_trimmed_and_preserved (test_names.NormalizeNameTests) ... ok
test_whitespace_only_name_is_rejected (test_names.NormalizeNameTests) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.000s

OK
```

### 5. 精确检查异常消息后（退出码 0）

```text
test_empty_name_is_rejected (test_names.NormalizeNameTests) ... ok
test_nonempty_name_is_trimmed_and_preserved (test_names.NormalizeNameTests) ... ok
test_whitespace_only_name_is_rejected (test_names.NormalizeNameTests) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.000s

OK
```

UTC 结束：
2026-11-10 05:24:56 UTC
