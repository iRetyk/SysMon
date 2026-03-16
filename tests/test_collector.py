from src import get_cpu_usage
import pytest

@pytest.mark.parametrize("mock_per_core,mock_total", [
    ([0.0, 0.0, 0.0, 0.0], 0.0),
        ([10.0, 20.0, 30.0, 40.0], 25.0),
        ([100.0, 100.0, 100.0, 100.0], 100.0),
        ([0.0, 50.0, 50.0, 100.0], 50.0),
        ([1.0, 2.0, 3.0, 4.0], 2.5),
        ([33.3, 33.3, 33.4], 33.3),
        ([0.0], 0.0),
        ([100.0, 0.0, 50.0, 25.0], 43.8),
])
def test_cpu(mocker,mock_per_core,mock_total):
    mocker.patch("src.collector.psutil.cpu_percent",return_value=mock_per_core)
    
    per_core,total = get_cpu_usage(2)
    
    assert per_core == mock_per_core
    assert total == mock_total


def test_cpu_empty_list(mocker):
    mocker.patch("src.collector.psutil.cpu_percent",return_value=[])
    
    with pytest.raises(RuntimeError):
        get_cpu_usage(2)
    