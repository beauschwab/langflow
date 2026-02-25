from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from langflow.components.data import DremioExecutorComponent
from langflow.schema.dataframe import DataFrame

_FLIGHT_MODULE = "langflow.components.data.dremio.flight"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_component(**kwargs):
    defaults = {
        "host": "dremio.example.com",
        "port": 32010,
        "username": "testuser",
        "password": "testpass",
        "query": "SELECT 1 AS col",
        "tls": False,
        "tls_root_certs": "",
    }
    defaults.update(kwargs)
    return DremioExecutorComponent(**defaults)


def _make_flight_mocks(rows: list[dict]) -> tuple:
    """Return (mock_flight_module, mock_client) pre-configured with *rows* as query result."""
    arrow_table = MagicMock()
    arrow_table.to_pandas.return_value = pd.DataFrame(rows)

    reader = MagicMock()
    reader.read_all.return_value = arrow_table

    endpoint = MagicMock()
    endpoint.ticket = MagicMock()

    info = MagicMock()
    info.endpoints = [endpoint]

    token_pair = ("authorization", "Bearer token123")

    mock_client = MagicMock()
    mock_client.authenticate_basic_token.return_value = token_pair
    mock_client.get_flight_info.return_value = info
    mock_client.do_get.return_value = reader

    mock_flight = MagicMock()
    mock_flight.FlightClient.return_value = mock_client
    mock_flight.FlightDescriptor.for_command.return_value = MagicMock()
    mock_flight.FlightCallOptions.return_value = MagicMock()

    return mock_flight, mock_client


# ---------------------------------------------------------------------------
# execute_query – success paths
# ---------------------------------------------------------------------------


def test_execute_query_returns_dataframe():
    component = _make_component()
    rows = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
    mock_flight, _ = _make_flight_mocks(rows)

    with patch(_FLIGHT_MODULE, mock_flight):
        result = component.execute_query()

    assert isinstance(result, DataFrame)
    assert list(result.columns) == ["id", "name"]
    assert len(result) == 2


def test_execute_query_status_set():
    component = _make_component()
    rows = [{"val": 42}]
    mock_flight, _ = _make_flight_mocks(rows)

    with patch(_FLIGHT_MODULE, mock_flight):
        component.execute_query()

    assert "1 rows" in component.status


def test_execute_query_uses_correct_location_no_tls():
    component = _make_component(host="myhost", port=12345, tls=False)
    mock_flight, _ = _make_flight_mocks([{"x": 1}])

    with patch(_FLIGHT_MODULE, mock_flight):
        component.execute_query()

    mock_flight.FlightClient.assert_called_once_with("grpc+tcp://myhost:12345")


def test_execute_query_uses_tls_location():
    component = _make_component(host="secure.dremio.io", port=32010, tls=True)
    mock_flight, _ = _make_flight_mocks([{"x": 1}])

    with patch(_FLIGHT_MODULE, mock_flight):
        component.execute_query()

    call_args = mock_flight.FlightClient.call_args
    assert "grpc+tls://secure.dremio.io:32010" in call_args[0]


def test_execute_query_closes_client_on_success():
    component = _make_component()
    mock_flight, mock_client = _make_flight_mocks([{"a": 1}])

    with patch(_FLIGHT_MODULE, mock_flight):
        component.execute_query()

    mock_client.close.assert_called_once()


def test_execute_query_closes_client_on_error():
    component = _make_component()
    mock_flight, mock_client = _make_flight_mocks([])
    mock_client.authenticate_basic_token.side_effect = RuntimeError("auth failed")

    with patch(_FLIGHT_MODULE, mock_flight):
        with pytest.raises(RuntimeError, match="auth failed"):
            component.execute_query()

    mock_client.close.assert_called_once()


# ---------------------------------------------------------------------------
# TLS certificate loading
# ---------------------------------------------------------------------------


def test_execute_query_loads_tls_cert(tmp_path):
    cert_file = tmp_path / "ca.pem"
    cert_file.write_bytes(b"FAKE CERT")

    component = _make_component(tls=True, tls_root_certs=str(cert_file))
    mock_flight, _ = _make_flight_mocks([{"x": 1}])

    with patch(_FLIGHT_MODULE, mock_flight):
        component.execute_query()

    mock_flight.FlightClient.assert_called_once_with(
        "grpc+tls://dremio.example.com:32010",
        tls_root_certs=b"FAKE CERT",
    )


def test_execute_query_raises_if_cert_not_found():
    component = _make_component(tls=True, tls_root_certs="/nonexistent/ca.pem")
    mock_flight, _ = _make_flight_mocks([])

    with patch(_FLIGHT_MODULE, mock_flight):
        with pytest.raises(FileNotFoundError, match="TLS root certificates file not found"):
            component.execute_query()


# ---------------------------------------------------------------------------
# Frontend node defaults
# ---------------------------------------------------------------------------


def test_dremio_component_defaults():
    component = DremioExecutorComponent()
    node = component.to_frontend_node()["data"]["node"]

    assert node["display_name"] == "Dremio SQL"
    assert "query" in node["template"]
    assert "host" in node["template"]
    assert "port" in node["template"]
    assert node["template"]["port"]["value"] == 32010
    assert node["template"]["tls"]["value"] is False
