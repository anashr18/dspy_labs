from collections import namedtuple

# class TemplateV2:
Field = namedtuple("Field", "name seperator input_variable output_variable description")


def passage2text(passages):
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
