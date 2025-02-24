# 工具
class BaseTool:
    def __init__(self, name, function_name, description, params):
        self.name = name
        self.function_name = function_name
        self.description = description
        self.params = params

    def describe(self):
        """Return a detailed description of the tool."""
        return {
            "name": self.name,
            "function_name": self.function_name,
            "description": self.description,
            "parameters": self.params
        }

    def run_function(self):
        """Run the associated function with the given parameters."""
        function_to_run = globals().get(self.function_name)
        if function_to_run:
            try:
                return function_to_run(**self.params)
            except TypeError as e:
                raise ValueError(
                    f"Invalid parameters for function {self.function_name}: {e}")
        else:
            raise NameError(f"Function {self.function_name} is not defined")

