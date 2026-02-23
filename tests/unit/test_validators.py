"""Tests unitarios para el módulo de quality."""
from src.quality.validators import CheckResult, CheckStatus


def test_check_result_to_dict():
    """CheckResult se serializa correctamente."""
    r = CheckResult(
        check_name="test_check",
        layer="bronze",
        table_name="test_table",
        status=CheckStatus.PASSED,
        metric_value=100.0,
        threshold=50.0,
        message="All good",
    )
    d = r.to_dict()
    assert d["status"] == "passed"
    assert d["metric_value"] == 100.0
    assert "checked_at" in d


def test_check_status_values():
    """CheckStatus tiene los valores esperados."""
    assert CheckStatus.PASSED.value == "passed"
    assert CheckStatus.FAILED.value == "failed"
    assert CheckStatus.WARNING.value == "warning"
    assert CheckStatus.ERROR.value == "error"
