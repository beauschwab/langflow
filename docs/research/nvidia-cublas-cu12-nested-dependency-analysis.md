# Dependency Analysis: Packages with Nested `nvidia-*` Dependencies

## Summary

The package **`sentence-transformers`** (declared directly in `pyproject.toml`) is the root cause that pulls in all `nvidia-*` CUDA libraries transitively via `torch`. `langflow-base` (the workspace sub-package also declared in `pyproject.toml`) inherits the same chain through its own dependency on `sentence-transformers`.

> **Note:** `langchain-nvidia-ai-endpoints` and `llama-index-embeddings-nvidia` contain "nvidia" in their names but are API-only clients (HTTP-based) and do **not** depend on any `nvidia-*` CUDA packages.

## Repository locations reviewed

- `/home/runner/work/langflow/langflow/pyproject.toml`
- `/home/runner/work/langflow/langflow/uv.lock`

## All `nvidia-*` packages resolved in the lock file

| Package | Version |
|---------|---------|
| `nvidia-cublas-cu12` | 12.1.3.1 |
| `nvidia-cuda-cupti-cu12` | 12.1.105 |
| `nvidia-cuda-nvrtc-cu12` | 12.1.105 |
| `nvidia-cuda-runtime-cu12` | 12.1.105 |
| `nvidia-cudnn-cu12` | 9.1.0.70 |
| `nvidia-cufft-cu12` | 11.0.2.54 |
| `nvidia-curand-cu12` | 10.3.2.106 |
| `nvidia-cusolver-cu12` | 11.4.5.107 |
| `nvidia-cusparse-cu12` | 12.1.0.106 |
| `nvidia-nccl-cu12` | 2.20.5 |
| `nvidia-nvjitlink-cu12` | 12.8.93 |
| `nvidia-nvtx-cu12` | 12.1.105 |

All are gated by a platform marker (`platform_machine == 'x86_64' and sys_platform == 'linux'`), so they are only resolved on Linux x86_64 systems.

## Packages that directly depend on any `nvidia-*` package

| Package | Version | Direct `nvidia-*` dependency |
|---------|---------|-------------------------------|
| `torch` | 2.4.1 | `nvidia-cublas-cu12`, `nvidia-cuda-cupti-cu12`, `nvidia-cuda-nvrtc-cu12`, `nvidia-cuda-runtime-cu12`, `nvidia-cudnn-cu12`, `nvidia-cufft-cu12`, `nvidia-curand-cu12`, `nvidia-cusolver-cu12`, `nvidia-cusparse-cu12`, `nvidia-nccl-cu12`, `nvidia-nvtx-cu12` |
| `nvidia-cudnn-cu12` | 9.1.0.70 | `nvidia-cublas-cu12` |
| `nvidia-cusolver-cu12` | 11.4.5.107 | `nvidia-cublas-cu12`, `nvidia-cusparse-cu12`, `nvidia-nvjitlink-cu12` |
| `nvidia-cusparse-cu12` | 12.1.0.106 | `nvidia-nvjitlink-cu12` |

## Full transitive dependency chain from `pyproject.toml`

```
sentence-transformers (>=2.3.1)   [pyproject.toml line 200]
  └─ torch (2.4.1)
       ├─ nvidia-cublas-cu12 (12.1.3.1)
       ├─ nvidia-cuda-cupti-cu12 (12.1.105)
       ├─ nvidia-cuda-nvrtc-cu12 (12.1.105)
       ├─ nvidia-cuda-runtime-cu12 (12.1.105)
       ├─ nvidia-cudnn-cu12 (9.1.0.70)
       │    └─ nvidia-cublas-cu12
       ├─ nvidia-cufft-cu12 (11.0.2.54)
       ├─ nvidia-curand-cu12 (10.3.2.106)
       ├─ nvidia-cusolver-cu12 (11.4.5.107)
       │    ├─ nvidia-cublas-cu12
       │    ├─ nvidia-cusparse-cu12 (12.1.0.106)
       │    │    └─ nvidia-nvjitlink-cu12 (12.8.93)
       │    └─ nvidia-nvjitlink-cu12
       ├─ nvidia-cusparse-cu12
       ├─ nvidia-nccl-cu12 (2.20.5)
       └─ nvidia-nvtx-cu12 (12.1.105)

langflow-base (==0.2.0)           [pyproject.toml line 22 — workspace member]
  └─ sentence-transformers → torch → (same nvidia-* tree as above)
```

## `pyproject.toml` packages with a transitive `nvidia-*` dependency

| Package declared in `pyproject.toml` | Version | Path to `nvidia-*` |
|--------------------------------------|---------|---------------------|
| `sentence-transformers` | ≥2.3.1 (resolved: 3.4.1) | `sentence-transformers` → `torch` → `nvidia-*` |
| `langflow-base` | ==0.2.0 (workspace) | `langflow-base` → `sentence-transformers` → `torch` → `nvidia-*` |

## Notes

- `torch` is not listed in `pyproject.toml` directly; it arrives as a dependency of `sentence-transformers`.
- If the goal is to avoid pulling in CUDA libraries (e.g., for a CPU-only environment), pinning `torch` to a CPU-only wheel (e.g., `torch+cpu`) or replacing `sentence-transformers` with a lighter embedding provider would be the appropriate remediation.
