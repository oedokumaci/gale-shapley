"""Tests that verify the library can be imported cleanly."""

from importlib.metadata import version


def test_import_gale_shapley() -> None:
    """Importing the package should work without config files or optional deps."""
    import gale_shapley

    assert hasattr(gale_shapley, "__version__")
    assert gale_shapley.__version__ == version("gale-shapley")


def test_public_api_exports() -> None:
    """All documented public API names should be importable."""
    from gale_shapley import (
        Algorithm,
        MatchingResult,
        Person,
        Proposer,
        Responder,
        StabilityResult,
        check_stability,
        create_matching,
        find_blocking_pairs,
        is_individually_rational,
    )

    assert Algorithm is not None
    assert MatchingResult is not None
    assert Person is not None
    assert Proposer is not None
    assert Responder is not None
    assert StabilityResult is not None
    assert check_stability is not None
    assert create_matching is not None
    assert find_blocking_pairs is not None
    assert is_individually_rational is not None
