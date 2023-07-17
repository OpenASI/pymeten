from pymeten import checkit, showit, sizeit, timeit
import numpy as np

size = 100
arr_cpu = np.random.randint(0, 255, size=(size,size))

def test_show():
    showit(arr_cpu)

def test_size():
    bytes = sizeit(arr_cpu)
    assert bytes == 80000

def test_time():
    timeit(lambda: arr_cpu + 1)

def test_check():
    assert checkit(lambda: np.allclose(arr_cpu, arr_cpu))
