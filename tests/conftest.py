"""Global test fixtures."""

from collections.abc import Generator

import pytest


@pytest.fixture(scope="session", autouse=True)
def ray_cluster() -> Generator:
    """Start and stop a Ray cluster for all tests."""
    import ray

    ray.init(ignore_reinit_error=True, num_cpus=4)
    yield
    ray.shutdown()
