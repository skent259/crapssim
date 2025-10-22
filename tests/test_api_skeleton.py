import types


def test_package_imports():
    import crapssim_api  # noqa
    assert hasattr(crapssim_api, "__version__")


def test_create_app_callable():
    from crapssim_api.http import create_app

    app = create_app()
    assert callable(app), "ASGI app should be callable"


def test_error_codes_present():
    from crapssim_api.errors import ApiErrorCode

    required = {
        "ILLEGAL_TIMING",
        "ILLEGAL_AMOUNT",
        "UNSUPPORTED_BET",
        "LIMIT_BREACH",
        "INSUFFICIENT_FUNDS",
        "TABLE_RULE_BLOCK",
        "BAD_ARGS",
        "INTERNAL",
    }
    have = {e.name for e in ApiErrorCode}
    assert required.issubset(have)


def test_rng_determinism():
    from crapssim_api.rng import SeededRNG

    a = SeededRNG(123)
    b = SeededRNG(123)
    seq_a = [a.randint(1, 6) for _ in range(10)]
    seq_b = [b.randint(1, 6) for _ in range(10)]
    assert seq_a == seq_b
