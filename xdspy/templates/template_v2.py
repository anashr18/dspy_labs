from collections import namedtuple
from typing import Any
import xdspy
from icecream import ic

# class TemplateV2:
Field = namedtuple("Field", "name seperator input_variable output_variable description")


def passages2text(passages):
    if isinstance(passages) is str:
        return passages

    assert type(passages) in [list, tuple]

    if len(passages) == 1:
        return f"«{passages[0]}»"

    return "\n".join([f"[{idx+1}] «{txt}»" for idx, txt in enumerate(passages)])


def format_answers(answers):
    if isinstance(answers, list):
        if len(answers) >= 1:
            return str(answers[0]).strip()
        elif len(answers) == 0:
            raise ValueError("No answers found")
        elif isinstance(answers, str):
            return answers
        else:
            raise ValueError("Unable to parse answers")


class TemplateV2:
    def __init__(
        self,
        template,
        format_handlers={
            "passages": passages2text,
            "context": passages2text,
            "answer": format_answers,
            "answers": format_answers,
        },
    ):
        self.format_handlers = format_handlers
        self.fields = []
        pass

    def query(self, example, is_demo=False):
        result = []
        # ic(self.fields)
        # ic(example)
        if not is_demo:
            has_value = [
                field.input_variable in example
                and example[field.input_variable] is not None
                and example[field.input_variable] != ""
                for field in self.fields
            ]
            # ic(has_value)
            # adding a field
            for i in range(1, len(has_value)):
                # ic(any(has_value[i:]))
                if has_value[i - 1] and not any(has_value[i:]):
                    example[self.fields[i].input_variable] = ""
                    break
            # ic(example)

            for field in self.fields:
                if (
                    field.input_variable in example
                    and example[field.input_variable] is not None
                ):
                    if field.input_variable in self.format_handlers:
                        format_handler = self.format_handlers[field.input_variable]
                    else:

                        def format_handler(x):
                            # ic(x)
                            return " ".join(x.split())

                    result.append(
                        f"{field.name}{field.seperator}{format_handler(example[field.input_variable])}"
                    )
            # ic(result)
        if self._has_augmented_guidelines() and (
            "augmented" in example and example.augmented
        ):
            return "\n\n".join(result)
        else:
            return "\n".join(result)

    def _has_augmented_guidelines(self):
        return len(self.fields) > 3 or any(
            field.seperator == "\n" for field in self.fields
        )

    def _guidlines(self):
        result = "Follow the following format. \n\n"

        example = xdspy.Example()
        for field in self.fields:
            example[field.input_variable] = field.description
        ic(example)
        result += self.query(example)
        return result

    def __call__(self, example: xdspy.Example):
        """
        template is dict of instruction and fields(question, answer)
        example is dict of question and demos(question, answer)
        Fields which are part of template are consist of
        input_variable, output_variable, seperator, prefix, desc
        """
        example = xdspy.Example(example)
        # for key, value in example.items():
        #     print(key, value)

        if self.fields[-1].input_variable in example:
            del example[self.fields[-1].input_variable]
        rdemos = [self.query(demo) for demo in example.demos]
        query = self.query(example)
        # return query
        rdemos = "\n\n".join(rdemos)
        # return rdemos
        if len(rdemos) > 1:
            rdemos_and_query = "\n\n".join([rdemos, query])
        # return rdemos_and_query
        ic(self._guidlines())
        parts = [self.instruction, self._guidlines(), rdemos_and_query]
        return parts
