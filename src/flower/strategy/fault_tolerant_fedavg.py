# Copyright 2020 Adap GmbH. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Fault-tolerant variant of FedAvg strategy."""


from typing import Callable, List, Optional, Tuple

from flower.typing import Weights

from .aggregate import aggregate, weighted_loss_avg
from .fedavg import FedAvg


class FaultTolerantFedAvg(FedAvg):
    """Configurable FedAvg strategy implementation."""

    # pylint: disable-msg=too-many-arguments,too-many-instance-attributes
    def __init__(
        self,
        fraction_fit: float = 0.1,
        fraction_eval: float = 0.1,
        min_fit_clients: int = 1,
        min_eval_clients: int = 1,
        min_available_clients: int = 1,
        eval_fn: Optional[Callable[[Weights], Optional[Tuple[float, float]]]] = None,
        min_completion_rate_fit: float = 0.5,
        min_completion_rate_evaluate: float = 0.5,
    ) -> None:
        super().__init__(
            min_fit_clients=min_fit_clients,
            min_eval_clients=min_eval_clients,
            fraction_fit=fraction_fit,
            fraction_eval=fraction_eval,
            min_available_clients=min_available_clients,
            eval_fn=eval_fn,
        )
        self.completion_rate_fit = min_completion_rate_fit
        self.completion_rate_evaluate = min_completion_rate_evaluate

    def on_aggregate_fit(
        self, results: List[Tuple[Weights, int]], failures: List[BaseException]
    ) -> Optional[Weights]:
        """Aggregate fit results using weighted average."""
        if not results:
            return None
        # Check if enough results are available
        completion_rate = len(results) / (len(results) + len(failures))
        if completion_rate < self.completion_rate_fit:
            # Not enough results for aggregation
            return None
        return aggregate(results)

    def on_aggregate_evaluate(
        self, results: List[Tuple[int, float]], failures: List[BaseException]
    ) -> Optional[float]:
        """Aggregate evaluation losses using weighted average."""
        if not results:
            return None
        # Check if enough results are available
        completion_rate = len(results) / (len(results) + len(failures))
        if completion_rate < self.completion_rate_evaluate:
            # Not enough results for aggregation
            return None
        return weighted_loss_avg(results)
