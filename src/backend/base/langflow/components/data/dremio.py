from __future__ import annotations

from pathlib import Path

import pyarrow.flight as flight

from langflow.custom import Component
from langflow.io import BoolInput, IntInput, MessageTextInput, MultilineInput, Output, SecretStrInput, StrInput
from langflow.schema.dataframe import DataFrame


class DremioExecutorComponent(Component):
    """Execute SQL queries against a Dremio environment via the FlightSQL endpoint.

    Returns query results as a :class:`~langflow.schema.dataframe.DataFrame`.
    Requires the ``pyarrow`` package (``pip install pyarrow``).
    """

    display_name = "Dremio SQL"
    description = "Execute SQL queries against Dremio via the FlightSQL endpoint and return results as a DataFrame."
    documentation = "https://docs.dremio.com/cloud/sonar/query-data/flight/"
    icon = "database"
    name = "DremioExecutor"

    inputs = [
        StrInput(
            name="host",
            display_name="Host",
            required=True,
            info="Hostname or IP address of the Dremio server.",
            value="localhost",
        ),
        IntInput(
            name="port",
            display_name="Port",
            required=True,
            info="FlightSQL port. Default is 32010.",
            value=32010,
        ),
        StrInput(
            name="username",
            display_name="Username",
            required=True,
            info="Dremio username.",
        ),
        SecretStrInput(
            name="password",
            display_name="Password",
            required=True,
            info="Dremio password or personal access token.",
        ),
        MultilineInput(
            name="query",
            display_name="SQL Query",
            required=True,
            info="SQL query to execute.",
        ),
        BoolInput(
            name="tls",
            display_name="Use TLS",
            value=False,
            info="Enable TLS (encrypted) connection to Dremio.",
        ),
        MessageTextInput(
            name="tls_root_certs",
            display_name="TLS Root Certificates Path",
            required=False,
            info=(
                "Optional path to a PEM file containing trusted CA certificates. "
                "Only used when 'Use TLS' is enabled."
            ),
            value="",
            advanced=True,
        ),
    ]

    outputs = [
        Output(display_name="DataFrame", name="dataframe", method="execute_query"),
    ]

    def execute_query(self) -> DataFrame:
        location = f"grpc+{'tls' if self.tls else 'tcp'}://{self.host}:{self.port}"

        client_kwargs: dict = {}
        if self.tls and self.tls_root_certs:
            cert_path = Path(self.tls_root_certs)
            if not cert_path.is_file():
                msg = f"TLS root certificates file not found: {self.tls_root_certs}"
                raise FileNotFoundError(msg)
            client_kwargs["tls_root_certs"] = cert_path.read_bytes()

        client = flight.FlightClient(location, **client_kwargs)
        try:
            token_pair = client.authenticate_basic_token(self.username, self.password)
            headers = [token_pair]

            options = flight.FlightCallOptions(headers=headers)
            info = client.get_flight_info(
                flight.FlightDescriptor.for_command(self.query.encode()),
                options,
            )
            reader = client.do_get(info.endpoints[0].ticket, options)
            table = reader.read_all()
        finally:
            client.close()

        result = DataFrame(table.to_pandas())
        self.status = f"{len(result)} rows returned"
        return result
