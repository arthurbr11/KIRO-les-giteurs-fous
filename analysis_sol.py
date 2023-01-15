import numpy as np
import json


class Job:
    def __init__(self, index, task_sequence, release_date, due_date, weight):
        self.index = index
        self.task_sequence = task_sequence
        self.release_date = release_date
        self.due_date = due_date
        self.weight = weight

    def show(self):
        print("Job with index {} task sequence {} release date {} due date {} weight {}\n".format(self.index,
                                                                                                  self.task_sequence,
                                                                                                  self.release_date,
                                                                                                  self.due_date,
                                                                                                  self.weight))


class Task:
    def __init__(self, index, processing_time, machines):
        self.index = index
        self.processing_time = processing_time
        self.machines = machines  # list of machine indices on which this task can be performed

    def show(self):
        print('Task with index {} processing time {} and machines {}\n'.format(self.index, self.processing_time,
                                                                               self.machines))


class Instance:
    def __init__(self, nb_operators, alpha, beta, jobs, tasks, operators):
        self.nb_operators = nb_operators
        self.alpha = alpha  # unit penalty
        self.beta = beta  # tardiness
        self.jobs = jobs
        self.tasks = tasks
        self.operators = operators  # operators[i-1, m-1] = list of operators that can operate task i on machine m

    def nb_jobs(self):
        return len(self.jobs)

    def nb_tasks(self):
        return len(self.tasks)

    def nb_machines(self):
        return np.shape(self.operators)[1]

    def show(self):
        print('Instance with {} operators, unit penalty {}, tardiness {} and \n'.format(self.nb_operators, self.alpha,
                                                                                        self.beta))
        print("Jobs : \n")
        for j in range(self.nb_jobs()):
            self.jobs[j].show()
        print("Tasks: \n")
        for t in range(self.nb_tasks()):
            self.tasks[t].show()
        print("Operators: \n")
        print(self.operators)


class Solution:
    def __init__(self, starts, machines, operators):
        self.starts = starts
        self.machines = machines
        self.operators = operators

    def __eq__(self, other):
        if self.starts != other.starts or self.machines != other.machines or self.operators != other.operators:
            return False
        return True


"""
    is_feasible(solution::Solution, instance::Instance; verbose=true)
Check if `solution` is feasible for `instance`.
Prints some warnings when solution is infeasible and `verbose` is `true`.
"""


def is_feasible(solution, instance, verbose=True):
    starts, machines, operators = solution.starts, solution.machines, solution.operators

    n = instance.nb_tasks()
    if n != len(starts) or n != len(machines) or n != len(operators):
        if verbose:
            print("Not all tasks are in the solution")
        return False

    # Check job related constraints
    for job in instance.jobs:
        current_time = job.release_date
        for task_index in job.task_sequence:
            task = instance.tasks[task_index]
            start_time = starts[task_index]
            # start time should occur after end of previous task (constraints 4 and 5)
            if start_time < current_time:
                if verbose:
                    print(
                        f'Task {task_index + 1} started before previous one (or before the release date if it is the '
                        f'first one)')
                return False
            current_time += task.processing_time

            machine_index = machines[task_index]
            # the task needs to be compatible with the chosen machine
            if machine_index not in task.machines:
                if verbose:
                    print(f'Machine {machine_index + 1} is not compatible with task {task_index + 1}')
                return False

            operator = operators[task_index]
            # the chosen machine should be compatible with the chosen operator
            if operator not in instance.operators[task_index, machine_index]:
                if verbose:
                    print(f'Operator {operator + 1} cannot operate machine {machine_index + 1}')
                return False

    # A machine cannot operate two tasks at the same time (constraint 7)
    for m in range(instance.nb_machines()):
        tasks_with_m = sorted([i for i in range(n) if (machines[i] == m)], key=lambda task: starts[task])
        m_time = 0
        for i in tasks_with_m:
            if starts[i] < m_time:
                if verbose:
                    print(f'Two tasks (including {i + 1}) at the same time on machine {m + 1}')
                return False
            m_time = starts[i] + instance.tasks[i].processing_time
    # An operator cannot operate two tasks at the same time (constraint 7)
    for o in range(instance.nb_operators):
        tasks_with_o = sorted([i for i in range(n) if (operators[i] == o)], key=lambda task: starts[task])
        o_time = 0
        for i in tasks_with_o:
            if starts[i] < o_time:
                if verbose:
                    print(f'Two tasks at the same time with operator {o + 1} ({starts[i]}, {o_time})')
                return False
            o_time = starts[i] + instance.tasks[i].processing_time
    return True


"""
    job_cost(job_index::Int, solution::Solution, instance::Instance)
Compute the value of job `job_index` in the objective for `solution` in `instance`.
"""


def job_cost(job_index, solution, instance):
    alpha, beta, jobs, tasks = instance.alpha, instance.beta, instance.jobs, instance.tasks

    job = jobs[job_index]

    # Compute the job completion time
    last_task_index = job.task_sequence[-1]
    last_task = tasks[last_task_index]
    completion_time = solution.starts[last_task_index] + last_task.processing_time

    is_late = completion_time > job.due_date
    tardiness = 0
    if is_late:
        tardiness = completion_time - job.due_date
    return job.weight * (completion_time + alpha * is_late + beta * tardiness)


"""
    cost(solution::Solution, instance::Instance)
Compute the objective value of `solution` for given `instance`.
"""


def cost(solution, instance):
    return sum(job_cost(j, solution, instance) for j in range(instance.nb_jobs()))


"""
    read_instance(path::String)
Read instance from json file `path`.
"""


def read_instance(path):
    if not path.endswith('.json'):
        print("No json in your file")
        return
    with open(path, 'r') as f:
        data = json.load(f)
    parameters_data = data["parameters"]
    nb_tasks = parameters_data["size"]["nb_tasks"]
    nb_machines = parameters_data["size"]["nb_machines"]
    nb_operators = parameters_data["size"]["nb_operators"]
    alpha = parameters_data["costs"]["unit_penalty"]
    beta = parameters_data["costs"]["tardiness"]

    jobs_data = data["jobs"]
    jobs = [
        Job(
            index=job["job"],
            task_sequence=[i - 1 for i in job["sequence"]],
            release_date=job["release_date"],
            due_date=job["due_date"],
            weight=job["weight"],
        ) for job in jobs_data
    ]

    tasks_data = data["tasks"]
    tasks = [
        Task(
            index=task["task"] - 1,
            processing_time=task["processing_time"],
            machines=[l["machine"] - 1 for l in task["machines"]],
        ) for task in tasks_data
    ]

    operators = np.empty((nb_tasks, nb_machines), dtype=object)
    for task in tasks_data:
        i = task["task"]
        for machine in task["machines"]:
            m = machine["machine"]
            operator_list = [o - 1 for o in machine["operators"]]
            operators[i - 1, m - 1] = operator_list

    return Instance(nb_operators, alpha, beta, jobs, tasks, operators)


"""
    read_solution(path::String)
Read solution from json file `path`.
"""


def read_solution(path):
    if not path.endswith('.json'):
        print("No json in your file")
        return
    with open(path, 'r') as f:
        data = json.load(f)

    nb_tasks = len(data)
    starts = [0] * nb_tasks
    machines = [0] * nb_tasks
    operators = [0] * nb_tasks
    for task in data:
        task_index = task["task"]
        starts[task_index - 1] = task["start"]
        machines[task_index - 1] = task["machine"] - 1
        operators[task_index - 1] = task["operator"] - 1
    return Solution(starts, machines, operators)