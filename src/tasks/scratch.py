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
    return inputs

@task(
    settings={
        "number_of_cv_folds": s.Integer(""),
        "training_set_size": s.Float("")},
    inputs={
        "cleaned_data": s.DataFrame("")},
    outputs={
        "model": s.DataFrame("")})
def postprocess(settings, inputs):
    return inputs

@task(
    settings={
        "core": {"host": s.Text("Core host"),
                 "port": s.Int("Core port")}},
    inputs={
        "sql": s.Text("The query to execute")},
    outputs={
        "raw_data": s.DataFrame("The raw data")})
def extract_data(settings, inputs):
    pass


@task(
    settings={
        "backend": {"host": s.Text("Host running the backend"),
                    "port": s.Int("Port on which the backend listens")
                    }},
    inputs={},
    outputs={"sql": s.Text("The resulting query")})
def make_query(settings, inputs):
    pass


sch = TaskSchema.empty()

sch.append(preprocess.schema, key="preprocess")
sch.append(postprocess.schema, key="postprocess")


res = preprocess.execute(
    {"number_of_cv_folds": 1,
     "training_set_size": 0.5},
    {"raw_data": "hello"})

graph = TaskGraph(preprocess, postprocess)


if __name__ == "__main__":
    parser = cli.new_parser(graph.schema)
    arguments = parser.parse_args()
    print(arguments)
