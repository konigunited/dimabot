import os
import pytest

from bot.config import BotConfig, ConfigError


def test_bot_config_from_env_reads_values(monkeypatch):
    monkeypatch.setenv("DIMABOT_TOKEN", "123:abc")
    monkeypatch.setenv("DIMABOT_FINAL_LINK", "https://example.com")
    monkeypatch.delenv("DIMABOT_ADMIN_CHAT_ID", raising=False)

    config = BotConfig.from_env()

    assert config.token == "123:abc"
    assert config.final_link == "https://example.com"
    assert config.admin_chat_id is None


def test_bot_config_validates_admin_chat_id(monkeypatch):
    monkeypatch.setenv("DIMABOT_TOKEN", "token")
    monkeypatch.setenv("DIMABOT_FINAL_LINK", "https://example.com")
    monkeypatch.setenv("DIMABOT_ADMIN_CHAT_ID", "42")

    config = BotConfig.from_env()
    assert config.admin_chat_id == 42


def test_missing_required_variables_raise(monkeypatch):
    monkeypatch.delenv("DIMABOT_TOKEN", raising=False)
    monkeypatch.delenv("DIMABOT_FINAL_LINK", raising=False)

    with pytest.raises(ConfigError):
        BotConfig.from_env()


def test_invalid_admin_chat_id(monkeypatch):
    monkeypatch.setenv("DIMABOT_TOKEN", "token")
    monkeypatch.setenv("DIMABOT_FINAL_LINK", "https://example.com")
    monkeypatch.setenv("DIMABOT_ADMIN_CHAT_ID", "not-int")

    with pytest.raises(ConfigError):
        BotConfig.from_env()
