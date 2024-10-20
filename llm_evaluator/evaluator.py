import os
from openai import OpenAI
import time


class CFGAcceptanceExperiment:
    def __init__(self, model: str = "gpt-3.5-turbo"):
        """
        Initializes the CFGAcceptanceExperiment instance.

        Parameters:
        model (str): The model to be used for the experiment.
        """
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model

    def cfg_acceptance_checker(self, cfg: str, string: str) -> dict:
        """
        Uses the OpenAI API to determine if a string can be generated by a given CFG.

        Parameters:
        cfg (str): The context-free grammar rules.
        string (str): The string to be checked.

        Returns:
        dict: A dictionary containing 'result' (True/False), 'raw_response' (API response), and 'error' (if any).
        """
        # Construct the messages for the chat-based completion
        # Reason2Conclude
        # messages = [
        #     {
        #         "role": "system",
        #         "content": "You are a CFG analyzer that determines if a string can be derived from a given context-free grammar.",
        #     },
        #     {
        #         "role": "user",
        #         "content": f"""
        #         Task: Determine if the given string can be derived from the following CFG.

        #         Context-Free Grammar (CFG):
        #         {cfg}

        #         String to Check:
        #         "{string}"

        #         Follow the CFG rules exactly and return 'True' if the string can be derived, else 'False'.
        #         """,
        #     },
        # ]
        # PureGuess
        messages = [
            {
                "role": "system",
                "content": "You are a guesser that determines if a string can be derived from a given context-free grammar (CFG) purely based on instinct, without any reasoning or analysis.",
            },
            {
                "role": "user",
                "content": f"""
                Task: Make a guess whether the given string can be derived from the following CFG.

                Context-Free Grammar (CFG):
                {cfg}

                String to Check:
                "{string}"

                Return 'True' or 'False' based solely on your guess. No reasoning is required.
                """,
            },
        ]
        # Guess2Explain
        # messages = [
        #     {
        #         "role": "system",
        #         "content": "You are a guesser that determines if a string can be derived from a given context-free grammar (CFG). First, make a guess, and then provide an explanation for your guess.",
        #     },
        #     {
        #         "role": "user",
        #         "content": f"""
        #         Task: First make a guess whether the given string can be derived from the following CFG.

        #         Context-Free Grammar (CFG):
        #         {cfg}

        #         String to Check:
        #         "{string}"

        #         Return 'True' or 'False' based on your guess. After that, explain the reasoning behind your guess.
        #         """,
        #     },
        # ]
        try:
            # Call the OpenAI chat completions API
            response = self.client.chat.completions.create(
                messages=messages,
                model=self.model,
            )
            # Extract and clean the raw response
            raw_response = response.choices[0].message.content.strip()
            # Check for 'true' and 'false' in the response
            if "true" in raw_response.lower() and "false" in raw_response.lower():
                result = None  # Both True and False exist in the response
            elif "true" in raw_response.lower():
                result = True
            elif "false" in raw_response.lower():
                result = False
            else:
                result = None  # Neither True nor False found
            return {
                "result": result,
                "raw_response": raw_response,
                "error": None,
            }
        except Exception as e:
            # Handle any exception that occurred during the API call
            return {
                "result": None,
                "raw_response": None,
                "error": str(e),
            }

    def run_experiment(self, test_cases: list):
        """
        Runs the experiment with a given set of test cases.

        Parameters:
        test_cases (list): A list of test cases, where each test case is a dictionary with 'cfg' and 'string'.

        Yields:
        dict: The result for each test case, including the raw API response.
        """
        retry_delay = 1  # Initial delay in seconds
        for i, case in enumerate(test_cases):
            success = False
            while not success:
                try:
                    print(f"Running test case {i + 1}/{len(test_cases)}...")
                    result = self.cfg_acceptance_checker(
                        case["cfg"], case["string"]
                    )
                    yield {
                        "cfg": case["cfg"],
                        "string": case["string"],
                        "label": case["label"],
                        "result": result["result"],
                        "raw_response": result["raw_response"],
                        "error": result["error"],
                    }
                    success = True
                except Exception as e:
                    print(
                        f"Error encountered: {e}. Retrying in {retry_delay} seconds..."
                    )
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                    if retry_delay > 128:
                        return None


# 使用示例：
if __name__ == "__main__":
    # Initialize the experiment with the model
    experiment = CFGAcceptanceExperiment(model="gpt-3.5-turbo")

    # Define a list of test cases
    test_cases = [
        {
            "cfg": """
            S -> aSb | ε
            """,
            "string": "aabb",
            "label": True,
        },
        {
            "cfg": """
            S -> aS | b
            """,
            "string": "aaab",
            "label": True,
        },
        {
            "cfg": """
            S -> AB
            A -> aA | ε
            B -> bB | ε
            """,
            "string": "aabbb",
            "label": True,
        },
    ]

    # Run the experiment
    for result in experiment.run_experiment(test_cases):
        # Print the result of each test case as it is processed
        print(f"\nTest Case:")
        print(f"CFG: {result['cfg']}")
        print(f"Input String: {result['string']}")
        print(f"Parsed Result: {result['result']}")
        print(f"Raw Response: {result['raw_response']}")
        print(f"Error: {result['error']}")