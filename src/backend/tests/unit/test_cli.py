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


class _FakeResponse:
    def __init__(self, *, json_data=None, text="", status_code=200, headers=None, content=b""):
        self._json_data = json_data
        self.text = text
        self.status_code = status_code
        self.headers = headers or {}
        self.content = content

    def json(self):
        return self._json_data

    def raise_for_status(self):
        if self.status_code >= 400:
            request = __main__.httpx.Request("GET", "http://localhost")
            response = __main__.httpx.Response(self.status_code, request=request, text=self.text)
            raise __main__.httpx.HTTPStatusError("error", request=request, response=response)


class _FakeClient:
    def __init__(self, responses):
        self._responses = responses

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def get(self, _url, _headers=None):
        if not self._responses["GET"]:
            msg = "No mocked GET responses remaining."
            raise AssertionError(msg)
        return self._responses["GET"].pop(0)

    def post(self, _url, _files=None, _headers=None, _params=None, _json=None):
        if not self._responses["POST"]:
            msg = "No mocked POST responses remaining."
            raise AssertionError(msg)
        return self._responses["POST"].pop(0)


def test_io_state_command(runner, monkeypatch):
    responses = {
        "GET": [
            _FakeResponse(json_data=[{"id": 1}, {"id": 2}]),
            _FakeResponse(json_data=[{"id": "a"}]),
            _FakeResponse(json_data=[{"id": "f1"}, {"id": "f2"}, {"id": "f3"}]),
            _FakeResponse(json_data=[{"id": "v1"}]),
        ],
        "POST": [],
    }
    monkeypatch.setattr(__main__.httpx, "Client", lambda timeout: _FakeClient(responses))
    result = runner.invoke(app, ["io", "state", "--base-url", "http://localhost:7860"])
    assert result.exit_code == 0, result.stdout
    assert "Langflow State Snapshot" in result.stdout
    assert "flows" in result.stdout
    assert "folders" in result.stdout


def test_io_snapshot_command_yaml(runner, monkeypatch, tmp_path):
    output = tmp_path / "snapshot.yaml"
    responses = {
        "GET": [
            _FakeResponse(json_data=[{"id": 1}]),
            _FakeResponse(json_data=[{"id": "agent"}]),
            _FakeResponse(json_data=[{"id": "folder"}]),
            _FakeResponse(json_data=[{"id": "variable"}]),
        ],
        "POST": [],
    }
    monkeypatch.setattr(__main__.httpx, "Client", lambda timeout: _FakeClient(responses))
    result = runner.invoke(app, ["io", "snapshot", "--output", str(output), "--base-url", "http://localhost:7860"])
    assert result.exit_code == 0, result.stdout
    content = output.read_text(encoding="utf-8")
    assert "flows:" in content
    assert "agents:" in content


def test_io_import_flows_command(runner, monkeypatch, tmp_path):
    input_file = tmp_path / "flow.yaml"
    input_file.write_text("name: demo\n", encoding="utf-8")
    responses = {
        "GET": [],
        "POST": [_FakeResponse(json_data=[{"id": "flow-1"}])],
    }
    monkeypatch.setattr(__main__.httpx, "Client", lambda timeout: _FakeClient(responses))
    result = runner.invoke(
        app,
        ["io", "import-flows", "--file-path", str(input_file), "--base-url", "http://localhost:7860"],
    )
    assert result.exit_code == 0, result.stdout
    assert "Imported 1 flow(s)." in result.stdout
