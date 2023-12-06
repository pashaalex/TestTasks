"""
Task description:
* Requires a task queue with priorities and resource limits.
* Each task has a priority and the required amount of resources to process it.
* Publishers create tasks with specified resource limits, and put them in a task queue.
* Consumer receives the highest priority task that satisfies available resources.
* The queue is expected to contain thousands of tasks.
* Write a unit test to demonstrate the operation of the queue.
"""
from dataclasses import dataclass

@dataclass
class Resources:
    ram: int
    cpu_cores: int
    gpu_count: int

@dataclass
class Task:
    id: int
    priority: int
    resources: Resources
    content: str
    result: str

class TaskQueue:
    task_list = []
    def add_task(self, task: Task):
        self.task_list.append(task)
        pass

    def get_task(self, available_resources: Resources) -> Task:
        if len(self.task_list) == 0: return None
        task_result: Task = None
        task_index: int = -1
        for task_id in range(len(self.task_list)):
            task: Task = self.task_list[task_id]            
            if (task.resources.cpu_cores <= available_resources.cpu_cores
                and task.resources.gpu_count <= available_resources.gpu_count
                and task.resources.ram <= available_resources.ram):
                if task_result != None and task_result.priority > task.priority:
                    continue
                task_result = task
                task_index = task_id
        if task_index == -1: return None
        return self.task_list.pop(task_index)

    def count(self) -> int:
        return len(self.task_list)
