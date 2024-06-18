import openai
from openai import OpenAI
from icecream import ic
import backoff


class GPT3:
    def __init__(self, model=None, api_key=None) -> None:
        self.kwargs = {
            "model": model,
            "temperature": 0.0,
            "max_tokens": 150,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "n": 1,
        }
        self.history = []

    def basic_request(self, prompt, **kwargs):
        raw_kwargs = kwargs
        kwargs = {**self.kwargs, "prompt": prompt, **kwargs}
        response = self.gpt3_request_v2(**kwargs)
        # print(response)

        history = {
            "prompt": prompt,
            "response": response,
            "kwargs": kwargs,
            "raw_kwargs": raw_kwargs,
        }
        self.history.append(history)
        return response

    def gpt3_request_v2(self, **kwargs):
        client = OpenAI(
            # This is the default and can be omitted
            # api_key=os.environ.get("OPENAI_API_KEY"),
        )
        completion = client.completions.create(
            **kwargs
            # model="gpt-3.5-turbo",
            # prompt=prompt,
            # messages=[
            #     {
            #         "role": "user",
            #         "content": "Say this is a test",
            #     }
            # ],
        )
        return completion
        # return client.chat.completions.create(**kwargs)

    def __call__(self, prompt, only_completed=True, return_sorted=True, **kwargs):
        # assert only_completed, 'for now'
        # assert

        if kwargs.get("n", 1) > 1:
            kwargs = {**kwargs, "logprobs": 5}

        response = self.request(prompt, **kwargs)
        # ic(response)
        choices = response.choices
        # ic(choices)

        completed_choices = [c for c in choices if c.finish_reason != "length"]
        # ic(completed_choices)
        if only_completed and len(completed_choices):
            choices = completed_choices

        completions = [c.text for c in choices]
        # ic(completions)

        if return_sorted and kwargs.get("n", 1) > 1:
            scored_completions = []
            for c in choices:
                tokens, logprobs = (
                    c.logprobs.tokens,
                    c.logprobs.token_logprobs,
                )

                if "<|endoftext|>" in tokens:
                    index = tokens.index("<|endoftext|>") + 1
                    tokens, logprobs = tokens[:index], logprobs[:index]

                avglog = sum(logprobs) / len(logprobs)
                scored_completions.append((avglog, c.text))

            scored_completions = sorted(scored_completions, reverse=True)
            completions = [c for _, c in scored_completions]
        return completions

    def inspect_history(self, n=1):
        last_prompt = None
        printed = []

        for x in reversed(self.history[-100:]):
            prompt = x["prompt"]

            if prompt != last_prompt:
                printed.append((prompt, x["response"].choices))
            last_prompt = prompt

            if len(printed) > n:
                break
        for prompt, choices in reversed(printed):
            print("\n\n\n")
            print(prompt, end="")
            self.print_green(choices[0].text, end="")

            if len(choices) > 1:
                self.print_red(f" \t (and {len(choices)-1} other completions)", end="")
            print("\n\n\n")

    def print_green(self, text, end="\n"):
        print("\x1b[32m" + str(text) + "\x1b[0m", end=end)

    def print_red(self, text, end="\n"):
        print("\x1b[31m" + str(text) + "\x1b[0m", end=end)
        pass

    def backoff_hdlr(details):
        # Handler from https://pypi.org/project/backoff/
        print(
            f"Backing off {details['wait']:0.1f} seconds after {details['tries']} tries "
            f"calling function {details['target']} with args {details['args']} and kwargs "
            f"{details['kwargs']}"
        )

    @backoff.on_exception(
        backoff.expo,
        (
            openai.RateLimitError,
            openai.APIError,
        ),
        max_time=1000,
        on_backoff=backoff_hdlr,
    )
    def request(self, prompt, **kwargs):
        return self.basic_request(prompt, **kwargs)
