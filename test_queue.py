import pytest  
from task_queue import TaskQueue, Resources, Task

def test_smoke():
    taskQueue = TaskQueue()
    resources = Resources(1000, 4, 0)
    task = Task(1, 1, resources, 'content', 'result')
    taskQueue.add_task(task)
    assert taskQueue.count() == 1
    task = taskQueue.get_task(Resources(10, 1, 0))
    assert task is None
    task = taskQueue.get_task(resources)
    assert task is not None
    assert taskQueue.count() == 0

def test_priority():
    taskQueue = TaskQueue()
    resources = Resources(1000, 4, 0)
    taskQueue.add_task(Task(1, 1, Resources(1000, 4, 0), 'content', 'result'))
    taskQueue.add_task(Task(2, 2, Resources(1000, 4, 0), 'content', 'result'))
    taskQueue.add_task(Task(3, 1, Resources(1000, 4, 0), 'content', 'result'))
    task = taskQueue.get_task(resources)
    assert task.id == 2

@pytest.mark.parametrize( "task_cpu, task_ram, task_gpu, av_cpu, av_ram, av_gpu, is_return",  
    [  
        (4, 100, 1, 4, 100, 1, True),
        (4, 100, 1, 3, 100, 1, False),
        (4, 100, 1, 4, 99, 1, False),
        (4, 100, 1, 4, 100, 0, False)
    ]) 
def test_filter_cases(task_cpu, task_ram, task_gpu, av_cpu, av_ram, av_gpu, is_return):
    taskQueue = TaskQueue()
    taskQueue.add_task(Task(1, 1, Resources(task_ram, task_cpu, task_gpu), 'content', 'result'))
    task = taskQueue.get_task(Resources(av_ram, av_cpu, av_gpu))
    if is_return:
        assert task is not None
    else:
        assert task is None

