from xdspy.templates import passage2text, format_answers, Field


class Type:
    def __init__(self, prefix, desc, format=None, aliases=[], **kwargs):
        self.prefix = prefix
        self.desc = desc
        self.format = format
        self.aliases = aliases
        self.kwargs = kwargs

        # assert aliases ==[]

    def __call__(self, **kwargs):
        kwargs = {**self.__dict__, **kwargs}
        return Type(**kwargs)


class Template:
    def __init__(self, instruction, **kwargs):
        self.instruction = instruction

        self.fields = []
        self.format_handlers = {"context": passage2text, "answers": format_answers}

        for key, value in kwargs.items():
            print(key, value)
            prefix = value.prefix
            seperator = (
                " " if prefix.rstrip() == prefix else prefix[len(prefix.rstrip()) :]
            )
            field = Field(
                name=prefix.strip(),
                description=value.desc,
                input_variable=key,
                output_variable=key,
                seperator=seperator,
            )
            self.fields.append(field)

            if value.format:
                for name in [key, *value.aliases]:
                    # print(key, name, value)
                    self.format_handlers[name] = value.format
