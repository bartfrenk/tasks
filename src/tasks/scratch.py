from tasks.base import Node, TaskArgumentParser, command_line_app, Graph
from tasks.schema import Dict, Int, String


class TaskA(Node):

    _settings_schema = Dict(
        complexity=Int("The complexity settings")
    )
    _inputs_schema = Dict(
        source=String("The text to process")
    )
    _outputs_schema = Dict(
        trace=String("The resulting output"),
        confidence=Int("The confidence")
    )

    def execute(self, inputs):
        return {"trace": self.settings["complexity"] * inputs["source"]}



class TaskB(Node):

    _settings_schema = Dict()
    _inputs_schema = Dict(
        trace=String("The input")
    )
    _outputs_schema = Dict(
        xxx=String("Output")
    )

    def execute(self, inputs):
        return {"xxx": inputs["trace"]}

graph = Graph(TaskA(), TaskB())


class TaskC(Node):

    _settings_schema = Dict(
        saliency=Int("The saliency")
    )
    _inputs_schema = Dict(
        trace=String("The input"),
        xxx=String("Another input"),
        foo=Int("A foo")
    )
    _outputs_schema = Dict(
        yyy=String("Output")
    )

    def execute(self, inputs):
        return {"xxx": inputs["trace"] + str(self.settings["saliency"])}

graph = Graph(TaskA(), TaskB(), TaskC())


# This API is less verbose:
#
# @task(
#     settings=Properties(
#         complexity=Int("Complexity"),
#         number_of_cv_folds=Int("Number of folds used for cross validation")),
#     inputs=Properties(
#         source=String("Source")),
#     outputs=Properties(
#         dest=String("Destination")))
# def preprocess(self, inputs):
#     pass
#
# Also, using a class for each task type seems overkill.


pipeline = composite(collect, preprocess, select_features, train)

to_airflow_dag(pipeline)

if __name__ == "__main__":
    command_line_app(graph)
