class Int: pass
class Bool: pass
class Object: pass
class DataFrame: pass

@task(
    settings_desc=Descriptor(
        validation_size=int,
        number_of_cv_folds=int,
        split_dataset=bool,
        label_encoders=object,
        one_hot_encoders=object
    ),
    inputs_desc=Descriptor(
        clean_date=DataFrame
    ),
    outputs_desc=Descriptor(
        test_set=DataFrame,
        validation_set=DataFrame,
        full_data=DataFrame
    ))
def preprocess(settings, inputs):
    pass


parser = cli_arg_parser(preprocess)
writer = cli_out_writer(preprocess)



# _settings_desc = "<settings>"

# _inputs_desc = "<inputs>"

# _outputs_desc = "<outputs>"

class TaskException(Exception):
    pass


class Task:
    def __init__(self, execute_fn, settings_desc, inputs_desc, outputs_desc):
        """Create a new task.

        :param execute_fn: The actual computation to execute.  This is a
            function that accepts two arguments: the settings, and the inputs,
            and return an object that conforms to the outputs descriptor.
        :param settings_desc: A descriptor for the settings of this
            computation.
        :param inputs_desc: A descriptor for the inputs for the computation.
            Note that the distinction between settings and inputs is purely
            conceptual from the standpoint of the computation.
        :param outputs_desc: A descriptor for the outputs of the computation.
        """
        self._execute_fn = execute_fn
        self.settings_desc = settings_desc
        self.inputs_desc = inputs_desc
        self.outputs_desc = outputs_desc
        self._settings = None

    @classmethod
    def new(cls, execute_fn, settings_desc, inputs_desc, outputs_desc):
        return cls(execute_fn, settings_desc, inputs_desc, outputs_desc)

    def __call__(self, inputs):
        if not self.settings:
            raise TaskException("Need to initialize task")
        # TODO: Add validation of inputs
        self._execute_fn(self.settings, inputs)

    @property
    def settings(self):
        return self._settings

    @settings.setter
    def settings(self, value):
        # TODO: Add validation of settings
        self._settings = value

    def __repr__(self):
        return "<{}: {}({})>".format(
            self.__class__.__name__,
            self._execute_fn.func_name,
            self.settings)

class DescriptorProperty:
    def __init__(self):
        pass


class Descriptor:
    def __init__(self, **kwargs):
        """Creates a new descriptor.

        A descriptor is a schema for key-value data.  It may serve to validate
        data, to automatically create command line parsers, etc.
        """
        self._properties = {}
        for (name, value) in kwargs.items():
            setattr(self, name, value)

    def __setitem__(self, key, value):
        if not isinstance(value, DescriptorProperty):
            raise ValueError("'{}' should be a '{}'".format(
                value, DescriptorProperty.__class__.__name__))
        self._properties[key] = value

    def __getitem__(self, key):
        return self._properties[key]

    def __iter__(self):
        return iter(self._properties)

    def items(self):
        return self._properties.items()

    def validate(self, data):
        pass

    @staticmethod
    def merge(*descs):
        result = Descriptor()
        for desc in descs:
            for (name, prop) in desc.items():
                result[name] = prop
        return result


task = Task.new(preprocess, _settings_desc, _inputs_desc, _outputs_desc)
# class DescriptorArgParser(ArgParser):
#     pass


# def new_command_line_parser(task):
#     pass

# class Setting:

#     def __init__(self, ty):
#         pass

# class Input:
#     pass

# class Output:
#     pass

# class PreprocessData(Task):

#     def execute(self, inputs):
#         pass

#     validation_size = Setting(int)
#     number_of_cv_folds = Setting(int)
#     split_dataset = Setting(bool)

#     one_hot_encoder = Input()
#     clean_data = Input()
#     label_encoders = Input()

#     feature_labels = Output()
#     ml_data_training = Output()

#     def execute(self, **inputs):
#         pass

# @classmethod
# def settings(self):
#     return dict(
#         validation_size=Setting(int),
#         number_of_cv_folds=Setting(int),
#         split_dataset=Setting(bool)
#     )

# pass

# preprocess_cli = CommandLineJob()

# def create_arg_parser(task):
#     pass

# class Composition(Task):

#     def __init__(self, settings, *tasks):
#         self._tasks = tasks

#     def setting(self):
#         pass
