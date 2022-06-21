import os
from typing import Tuple

from aws_lambda_powertools import Logger, Metrics, Tracer


def init_monitoring() -> Tuple[Logger, Metrics, Tracer]:
    """initialize logger, metrics and tracer"""
    env = os.environ.get("DEPLOY_ENV", "feature")
    _logger = Logger()
    _logger.append_keys(env=env)
    _metrics = Metrics()
    _metrics.set_default_dimensions(env=env)
    _tracer = Tracer()

    return _logger, _metrics, _tracer
