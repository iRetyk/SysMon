from src import get_cpu_usage



def test_cpu(mocker):
    mocker.patch("src.collector.psutil.cpu_percent",return_value=[10.0,20.0,30.0,40.0])
    
    per_core,total = get_cpu_usage(2)
    
    assert per_core == [10.0,20.0,30.0,40.0]
    assert total == 25.0