from helpers import config as config_helper
from speaker.message_type import MessageType


def test_load_ok():
    assert config_helper.load_config("./test_mocks/config.toml") is not None


def test_load_not_found():
    assert config_helper.load_config("./test_mocks/does_not_exist.toml") is None


def test_validate_ok():
    settings = config_helper.load_config("./test_mocks/config.toml")
    assert settings is not None
    assert (
        config_helper.find_missing_field(
            settings["speaking"]["message_patterns"], MessageType
        )
        is None
    )


def test_validate_not_ok():
    settings = config_helper.load_config("./test_mocks/config.toml")
    assert settings is not None
    assert (
        config_helper.find_missing_field(
            settings["listening"]["replacements"], MessageType
        )
        == "Ok"
    )
