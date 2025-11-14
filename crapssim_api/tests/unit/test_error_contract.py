import json

import pytest

pytest.importorskip("fastapi")
pytest.importorskip("pydantic")

from crapssim_api.errors import ApiError
from crapssim_api.http import start_session


def test_bad_args_seed_type():
    with pytest.raises(ApiError) as e:
        start_session({"spec": {"table_profile": "default"}, "seed": "abc"})
    assert e.value.code == "BAD_ARGS"


def test_unsupported_bet():
    from crapssim_api.errors import unsupported_bet

    with pytest.raises(ApiError):
        raise unsupported_bet("fire not supported")


def test_table_rule_block(tmp_path):
    from crapssim_api.errors import table_rule_block

    with pytest.raises(ApiError):
        raise table_rule_block("max odds beyond cap")
