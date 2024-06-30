import xdspy

# from xdspy.templates import TemplateV2


def generate(template, **kwargs):
    generator = xdspy.settings.lm

    def do_generate(example: xdspy.Example, stage):
        assert stage is not None
        # find the stage for example 'qa'
        example = example.demos_at(lambda d: d[stage])

        # TemplateV2(template)

        prompt = template(example)
        return prompt
        # print(prompt)

    return do_generate


# {
#     "question": "Who has a broader scope of profession: E. L. Doctorow or Julia Peterkin?",
#     "demos": [
#         {
#             "question": "Which award did the first book of Gary Zukav receive?",
#             "answer": ["U.S. National Book Award", "National Book Award"],
#         },
#         {
#             "question": "The heir to the Du Pont family fortune sponsored what wrestling team?",
#             "answer": ["Foxcatcher", "Team Foxcatcher", "Foxcatcher Team"],
#         },
#     ],
# }
#     Field(
#         name="Final Answer:",
#         seperator=" ",
#         input_variable="answer",
#         output_variable="answer",
#         description="${a short factoid answer, often between 1 and 5 words}",
#     )
