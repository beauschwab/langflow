from importlib import metadata

from langflow.utils.version import _compute_non_prerelease_version, _get_version_info, get_version_info


def test_version():
    info = get_version_info()
    assert info["version"] is not None
    assert info["main_version"] is not None
    assert info["package"] is not None


def test_compute_main():
    assert _compute_non_prerelease_version("1.0.10.post0") == "1.0.10"
    assert _compute_non_prerelease_version("1.0.10.a1") == "1.0.10"
    assert _compute_non_prerelease_version("1.0.10.b112") == "1.0.10"
    assert _compute_non_prerelease_version("1.0.10.rc0") == "1.0.10"
    assert _compute_non_prerelease_version("1.0.10.dev9") == "1.0.10"
    assert _compute_non_prerelease_version("1.0.10") == "1.0.10"


def test_novaflow_name_is_supported(monkeypatch):
    def mock_version(package_name):
        if package_name == "novaflow":
            return "1.0.0"
        msg = f"Package not found: {package_name}"
        raise metadata.PackageNotFoundError(msg)

    monkeypatch.setattr(metadata, "version", mock_version)
    info = _get_version_info()
    assert info["package"] == "Novaflow"
