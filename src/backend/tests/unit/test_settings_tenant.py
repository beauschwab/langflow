from langflow.services.settings.base import Settings


def test_tenant_isolation_flag_default_disabled():
    settings = Settings()
    assert settings.tenant_isolation_enabled is False

