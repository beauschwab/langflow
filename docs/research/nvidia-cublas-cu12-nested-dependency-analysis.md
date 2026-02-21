# Dependency Analysis: nvidia-cublas-cu12 Nested Dependency

## Summary

The package **`sentence-transformers`** (declared directly in `pyproject.toml`) is the top-level Langflow dependency that carries a nested (transitive) dependency on `nvidia-cublas-cu12`.

## Repository locations reviewed

- `/home/runner/work/langflow/langflow/pyproject.toml`
- `/home/runner/work/langflow/langflow/uv.lock`

## Full dependency chain

```
sentence-transformers (>=2.3.1)  [pyproject.toml line 200]
  └─ torch (2.4.1)
       ├─ nvidia-cublas-cu12 (12.1.3.1)          ← direct dep (linux/x86_64 only)
       ├─ nvidia-cudnn-cu12 (9.1.0.70)
       │    └─ nvidia-cublas-cu12 (12.1.3.1)     ← nested dep
       └─ nvidia-cusolver-cu12 (11.4.5.107)
            └─ nvidia-cublas-cu12 (12.1.3.1)     ← nested dep
```

## Key findings

| Package | Version | Relationship to `nvidia-cublas-cu12` | Declared in `pyproject.toml` |
|---------|---------|---------------------------------------|------------------------------|
| `sentence-transformers` | 3.4.1 | **Transitive** (via `torch`) | ✅ Yes (`>=2.3.1`) |
| `torch` | 2.4.1 | Direct + nested (via `nvidia-cudnn-cu12` and `nvidia-cusolver-cu12`) | ❌ No (pulled in by `sentence-transformers`) |
| `nvidia-cudnn-cu12` | 9.1.0.70 | Direct | ❌ No |
| `nvidia-cusolver-cu12` | 11.4.5.107 | Direct | ❌ No |

The NVIDIA CUDA libraries are gated by a platform marker (`platform_machine == 'x86_64' and sys_platform == 'linux'`) so they are only resolved on Linux x86_64 systems.

## Notes

- `torch` is not listed in `pyproject.toml` directly; it arrives as a dependency of `sentence-transformers`.
- If the goal is to avoid pulling in CUDA libraries (e.g., for a CPU-only environment), pinning `torch` to a CPU-only wheel (e.g., `torch+cpu`) or replacing `sentence-transformers` with a lighter embedding provider would be the appropriate remediation.
