import pytest
from langflow import __main__
from langflow.__main__ import app
from langflow.services import deps


@pytest.fixture(scope="module")
def default_settings():
    return [
        "--backend-only",
        "--no-open-browser",
    ]


def test_components_path(runner, default_settings, tmp_path):
    # create a "components" folder
    temp_dir = tmp_path / "components"
    temp_dir.mkdir(exist_ok=True)

    result = runner.invoke(
        app,
        ["run", "--components-path", str(temp_dir), *default_settings],
    )
    assert result.exit_code == 0, result.stdout
    settings_service = deps.get_settings_service()
    assert str(temp_dir) in settings_service.settings.components_path


def test_superuser(runner):
    result = runner.invoke(app, ["superuser"], input="admin\nadmin\n")
    assert result.exit_code == 0, result.stdout
    assert "Superuser created successfully." in result.stdout


def test_show_version_uses_package_name(monkeypatch):
    monkeypatch.setattr(__main__, "get_version_info", lambda: {"package": "Novaflow", "version": "9.9.9"})
    captured = {}

    def fake_echo(message):
        captured["message"] = message

    monkeypatch.setattr(__main__.typer, "echo", fake_echo)
    with pytest.raises(__main__.typer.Exit):
        __main__.show_version(value=True)
    assert captured["message"] == "novaflow 9.9.9"
