import xdspy


def generate(template, **kwargs):
    generator = xdspy.settings.lm

    def do_generate(example: xdspy.Example, stage):
        assert stage is not None
        example = example.demos_at(lambda d: d[stage])

    return do_generate


[
    {
        "question": "Which award did the first book of Gary Zukav receive?",
        "answer": ["U.S. National Book Award", "National Book Award"],
    },
    {
        "question": "The heir to the Du Pont family fortune sponsored what wrestling team?",
        "answer": ["Foxcatcher", "Team Foxcatcher", "Foxcatcher Team"],
    },
    {
        "question": "Who was the director of the 2009 movie featuring Peter Outerbridge as William Easton?",
        "answer": ["Kevin Greutert"],
    },
    {
        "question": 'Who produced the album that included a re-recording of "Lithium"?',
        "answer": ["Butch Vig"],
    },
    {
        "question": "What city was the victim of Joseph Druces working in?",
        "answer": ["Boston, Massachusetts", "Boston"],
    },
    {
        "question": "In what year was the star of To Hell and Back born?",
        "answer": ["1925"],
    },
]
