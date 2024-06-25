from xdspy.utils import dotdict
import xdspy
import random


class Example(dotdict):
    def __init__(self, *args, **kwargs):
        assert len(args) <= 1
        super().__init__()
        if len(args):
            assert len(args) == 1
            self.update(args[0])
        self.update(**kwargs)

    def copy(self, **kwargs):
        the_copy = Example(**{**dict(self), **kwargs})

        return the_copy

    def demos_at(self, fn):
        def at(d):
            try:
                # print("HERE")
                return fn(d).without("augmented")
            except:
                # print("NOT HERE")
                return {}

        demos = [d.copy(**at(d)) for d in self.demos]
        print(demos)
        return self.copy(demos=demos)


def sample(train, k: int):
    branch_idx = (
        hasattr(xdspy.settings, "branch_idx")
        and isinstance(xdspy.settings.branch_idx, int)
        and xdspy.settings.branch_idx
    )
    branch_idx = branch_idx or 0
    rng = random.Random(branch_idx)
    shuffled_train = list(train)
    rng.shuffle(shuffled_train)

    subset = shuffled_train[:k]
    subset = [xdspy.Example(x) for x in subset]
    # subset = [x for x in subset]

    return subset
