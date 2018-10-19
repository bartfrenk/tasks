import logging
import sys

import schema as s

from tasks.base import task, TaskSchema
from tasks.composite import TaskGraph
from tasks import cli
import tasks.executors as ex
import tasks.channels as ch


@task(
    settings={
        "number_of_cv_folds": s.Integer(
            "Number of folds used in cross-validation"),
        "training_set_size": s.Float(
            "Fraction of the data set used for training")},
    inputs={
        "raw_data": s.DataFrame("")},
    outputs={
        "cleaned_data": s.DataFrame("")})
def preprocess(settings, inputs):
    return {"cleaned_data": inputs["raw_data"]}

@task(
    settings={
        "number_of_cv_folds": s.Integer(""),
        "training_set_size": s.Float("")},
    inputs={
        "cleaned_data": s.DataFrame("")},
    outputs={
        "model": s.DataFrame("")})
def postprocess(settings, inputs):
    return {"model": inputs["cleaned_data"]}

@task(
    settings={},
    inputs={
        "sql": s.Text("The query to execute")},
    outputs={
        "raw_data": s.DataFrame("The raw data")})
def extract_data(settings, inputs):
    return {"raw_data": "xxx"}


@task(
    settings={
        "backend": {"host": s.Text("Host running the backend"),
                    "port": s.Integer("Port on which the backend listens")}},
    inputs={},
    outputs={"sql": s.Text("The resulting query")})
def make_query(settings, inputs):
    return {"sql": "select * from table"}


executor = ex.SequentialExecutor(ch.InMemoryChannel())
graph = TaskGraph(extract_data, make_query, preprocess, postprocess)
inputs = {}
settings = {
    "preprocess": {
        "number_of_cv_folds": 1,
        "training_set_size": 0.5},
    "postprocess": {
        "number_of_cv_folds": 1,
        "training_set_size": 0.5},
    "make_query": {
        "backend": {"host": "localhost",
                    "port": 1234}}}
graph.label = "TestTaskGraph"

stream = logging.StreamHandler(sys.stdout)
stream.setLevel(logging.INFO)

ex.log.setLevel(logging.INFO)
if not ex.log.hasHandlers():
    ex.log.addHandler(stream)
ch.log.setLevel(logging.INFO)
if not ch.log.hasHandlers():
    ch.log.addHandler(stream)



def f():
    try:
        return executor.execute(graph, settings, inputs)
    except ex.ExecutionException as exc:
        print(exc)


if __name__ == "__main__":
    parser = cli.new_parser(graph.schema)
    arguments = parser.parse_args()
    print(arguments)
