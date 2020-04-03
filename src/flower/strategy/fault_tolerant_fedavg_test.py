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
"""FaultTolerantFedAvg tests."""


from typing import List, Optional, Tuple

from flower import Weights

from .fault_tolerant_fedavg import FaultTolerantFedAvg


def test_on_aggregate_fit_no_results_no_failures() -> None:
    """Test evaluate function."""
    # Prepare
    strategy = FaultTolerantFedAvg(min_completion_rate_fit=0.1)
    results: List[Tuple[Weights, int]] = []
    failures: List[BaseException] = []
    expected: Optional[Weights] = None

    # Execute
    actual = strategy.on_aggregate_fit(results, failures)

    # Assert
    assert actual == expected


def test_on_aggregate_fit_no_results() -> None:
    """Test evaluate function."""
    # Prepare
    strategy = FaultTolerantFedAvg(min_completion_rate_fit=0.1)
    results: List[Tuple[Weights, int]] = []
    failures: List[BaseException] = [Exception()]
    expected: Optional[Weights] = None

    # Execute
    actual = strategy.on_aggregate_fit(results, failures)

    # Assert
    assert actual == expected


def test_on_aggregate_fit_not_enough_results() -> None:
    """Test evaluate function."""
    # Prepare
    strategy = FaultTolerantFedAvg(min_completion_rate_fit=0.5)
    results: List[Tuple[Weights, int]] = [([], 1)]
    failures: List[BaseException] = [Exception(), Exception()]
    expected: Optional[Weights] = None

    # Execute
    actual = strategy.on_aggregate_fit(results, failures)

    # Assert
    assert actual == expected


def test_on_aggregate_fit_just_enough_results() -> None:
    """Test evaluate function."""
    # Prepare
    strategy = FaultTolerantFedAvg(min_completion_rate_fit=0.5)
    results: List[Tuple[Weights, int]] = [([], 1)]
    failures: List[BaseException] = [Exception()]
    expected: Optional[Weights] = []

    # Execute
    actual = strategy.on_aggregate_fit(results, failures)

    # Assert
    assert actual == expected


def test_on_aggregate_fit_no_failures() -> None:
    """Test evaluate function."""
    # Prepare
    strategy = FaultTolerantFedAvg(min_completion_rate_fit=0.99)
    results: List[Tuple[Weights, int]] = [([], 1)]
    failures: List[BaseException] = []
    expected: Optional[Weights] = []

    # Execute
    actual = strategy.on_aggregate_fit(results, failures)

    # Assert
    assert actual == expected


def test_on_aggregate_evaluate_no_results_no_failures() -> None:
    """Test evaluate function."""
    # Prepare
    strategy = FaultTolerantFedAvg(min_completion_rate_evaluate=0.1)
    results: List[Tuple[int, float]] = []
    failures: List[BaseException] = []
    expected: Optional[float] = None

    # Execute
    actual = strategy.on_aggregate_evaluate(results, failures)

    # Assert
    assert actual == expected


def test_on_aggregate_evaluate_no_results() -> None:
    """Test evaluate function."""
    # Prepare
    strategy = FaultTolerantFedAvg(min_completion_rate_evaluate=0.1)
    results: List[Tuple[int, float]] = []
    failures: List[BaseException] = [Exception()]
    expected: Optional[float] = None

    # Execute
    actual = strategy.on_aggregate_evaluate(results, failures)

    # Assert
    assert actual == expected


def test_on_aggregate_evaluate_not_enough_results() -> None:
    """Test evaluate function."""
    # Prepare
    strategy = FaultTolerantFedAvg(min_completion_rate_evaluate=0.5)
    results: List[Tuple[int, float]] = [(1, 2.3)]
    failures: List[BaseException] = [Exception(), Exception()]
    expected: Optional[float] = None

    # Execute
    actual = strategy.on_aggregate_evaluate(results, failures)

    # Assert
    assert actual == expected


def test_on_aggregate_evaluate_just_enough_results() -> None:
    """Test evaluate function."""
    # Prepare
    strategy = FaultTolerantFedAvg(min_completion_rate_evaluate=0.5)
    results: List[Tuple[int, float]] = [(1, 2.3)]
    failures: List[BaseException] = [Exception()]
    expected: Optional[float] = 2.3

    # Execute
    actual = strategy.on_aggregate_evaluate(results, failures)

    # Assert
    assert actual == expected


def test_on_aggregate_evaluate_no_failures() -> None:
    """Test evaluate function."""
    # Prepare
    strategy = FaultTolerantFedAvg(min_completion_rate_evaluate=0.99)
    results: List[Tuple[int, float]] = [(1, 2.3)]
    failures: List[BaseException] = []
    expected: Optional[float] = 2.3

    # Execute
    actual = strategy.on_aggregate_evaluate(results, failures)

    # Assert
    assert actual == expected
