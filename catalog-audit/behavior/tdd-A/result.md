# 姓名规范化任务结果

- UTC 开始时间：不晚于 2026-11-10T05:23:21Z（最初读取已在该时间前发生；未记录更精确的开始时刻）。
- 先读取 `TASK.md`、`names.py`、指定的 ponytail Skill 和全局细则第 4 节；在本目录内搜索 Python 调用方，只发现 `names.py` 中的定义。
- 按 ponytail full 使用 Python 标准库；先新建 `test_names.py`，覆盖空字符串、纯空白（含制表符、换行和全角空格）、中英文、大小写及内部空格。
- 下列首次测试在修改 `names.py` 之前运行；退出码 1，确认空字符串和纯空白未按要求抛错。记录时刻不晚于 2026-11-10T05:23:49Z。

## 测试 1：修复前

命令：`python3 -B -m unittest -v test_names`

```text
test_empty_string_is_rejected (test_names.NormalizeNameTests) ... FAIL
test_nonempty_names_are_trimmed_and_preserved (test_names.NormalizeNameTests) ... ok
test_whitespace_only_is_rejected (test_names.NormalizeNameTests) ... 
======================================================================
FAIL: test_empty_string_is_rejected (test_names.NormalizeNameTests)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/USER/Documents/skills/evaluations/2026-11-10-skill-effectiveness/catalog-audit/behavior/tdd-A/test_names.py", line 9, in test_empty_string_is_rejected
    normalize_name('')
AssertionError: ValueError not raised

======================================================================
FAIL: test_whitespace_only_is_rejected (test_names.NormalizeNameTests) (name='  ')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/USER/Documents/skills/evaluations/2026-11-10-skill-effectiveness/catalog-audit/behavior/tdd-A/test_names.py", line 15, in test_whitespace_only_is_rejected
    normalize_name(name)
AssertionError: ValueError not raised

======================================================================
FAIL: test_whitespace_only_is_rejected (test_names.NormalizeNameTests) (name='\t\n')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/USER/Documents/skills/evaluations/2026-11-10-skill-effectiveness/catalog-audit/behavior/tdd-A/test_names.py", line 15, in test_whitespace_only_is_rejected
    normalize_name(name)
AssertionError: ValueError not raised

======================================================================
FAIL: test_whitespace_only_is_rejected (test_names.NormalizeNameTests) (name='\u3000')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/USER/Documents/skills/evaluations/2026-11-10-skill-effectiveness/catalog-audit/behavior/tdd-A/test_names.py", line 15, in test_whitespace_only_is_rejected
    normalize_name(name)
AssertionError: ValueError not raised

----------------------------------------------------------------------
Ran 3 tests in 0.001s

FAILED (failures=4)
```

- 在 `names.py` 中先去除首尾空白，再对空结果抛出 `ValueError('name required')`；非空结果原样返回。

## 测试 2：修复后

命令：`python3 -B -m unittest -v test_names`；退出码 0。

```text
test_empty_string_is_rejected (test_names.NormalizeNameTests) ... ok
test_nonempty_names_are_trimmed_and_preserved (test_names.NormalizeNameTests) ... ok
test_whitespace_only_is_rejected (test_names.NormalizeNameTests) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.000s

OK
```

- 新建并保留的交付文件：`/Users/USER/Documents/skills/evaluations/2026-11-10-skill-effectiveness/catalog-audit/behavior/tdd-A/test_names.py`（本任务自动测试）及 `/Users/USER/Documents/skills/evaluations/2026-11-10-skill-effectiveness/catalog-audit/behavior/tdd-A/result.md`（本任务记录）。
- 测试使用 `-B`，未产生 Python 字节码缓存；没有创建或删除一次性中间文件。`TASK.md` 未修改。
- UTC 结束时间：2026-11-10T05:24:34Z。
