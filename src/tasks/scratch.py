import schema as s

from tasks.base import task, TaskSchema
from tasks.composite import TaskGraph
from tasks import cli


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
    settings={
        "core": {"host": s.Text("Core host"),
                 "port": s.Integer("Core port")}},
    inputs={
        "sql": s.Text("The query to execute")},
    outputs={
        "raw_data": s.DataFrame("The raw data")})
def extract_data(settings, inputs):
    pass


@task(
    settings={
        "backend": {"host": s.Text("Host running the backend"),
                    "port": s.Integer("Port on which the backend listens")
                    }},
    inputs={},
    outputs={"sql": s.Text("The resulting query")})
def make_query(settings, inputs):
    pass


sch = TaskSchema.empty()

sch.append(preprocess.schema, key="preprocess")
sch.append(postprocess.schema, key="postprocess")


graph = TaskGraph(preprocess, postprocess)
inputs ={"raw_data": "hello"}
settings = {
    "preprocess": {
        "number_of_cv_folds": 1,
        "training_set_size": 0.5},
    "postprocess": {
        "number_of_cv_folds": 1,
        "training_set_size": 0.5}}

def f():
    try:
        return graph.execute(settings, inputs)
    except Exception as exc:
        print(exc)


if __name__ == "__main__":
    parser = cli.new_parser(graph.schema)
    arguments = parser.parse_args()
    print(arguments)
