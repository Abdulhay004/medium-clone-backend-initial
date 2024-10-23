"""Helper plugin for pytester; should not be loaded on its own."""

# This plugin contains assertions used by pytester. pytester cannot
# contain them itself, since it is imported by the `pytest` module,
# hence cannot be subject to assertion rewriting, which requires a
# module to not be already imported.
from typing import Dict
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union

from _pytest.reports import CollectReport
from _pytest.reports import TestReport


def assertoutcome(
    outcomes: Tuple[
        Sequence[TestReport],
        Sequence[Union[CollectReport, TestReport]],
        Sequence[Union[CollectReport, TestReport]],
    ],
    passed: int = 0,
    skipped: int = 0,
    failed: int = 0,
) -> None:
    __tracebackhide__ = True

    realpassed, realskipped, realfailed = outcomes
    obtained = {
        "passed": len(realpassed),
        "skipped": len(realskipped),
        "failed": len(realfailed),
    }
    expected = {"passed": passed, "skipped": skipped, "failed": failed}
    assert obtained == expected, outcomes


def assert_outcomes(
    outcomes: Dict[str, int],
    passed: int = 0,
    skipped: int = 0,
    failed: int = 0,
    errors: int = 0,
    xpassed: int = 0,
    xfailed: int = 0,
    warnings: Optional[int] = None,
    deselected: Optional[int] = None,
) -> None:
    """Assert that the specified outcomes appear with the respective
    numbers (0 means it didn't occur) in the text output from a test run."""
    __tracebackhide__ = True

    obtained = {
        "passed": outcomes.get("passed", 0),
        "skipped": outcomes.get("skipped", 0),
        "failed": outcomes.get("failed", 0),
        "errors": outcomes.get("errors", 0),
        "xpassed": outcomes.get("xpassed", 0),
        "xfailed": outcomes.get("xfailed", 0),
    }
    expected = {
        "passed": passed,
        "skipped": skipped,
        "failed": failed,
        "errors": errors,
        "xpassed": xpassed,
        "xfailed": xfailed,
    }
    if warnings is not None:
        obtained["warnings"] = outcomes.get("warnings", 0)
        expected["warnings"] = warnings
    if deselected is not None:
        obtained["deselected"] = outcomes.get("deselected", 0)
        expected["deselected"] = deselected
    assert obtained == expected
