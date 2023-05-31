

class CostCalculator:

    pricing_data: dict[str, dict[str, float]] = {   
        "gpt-4": {"prompt_cost": 0.03, "completion_cost": 0.06, "per_tokens": 1000},
        "gpt-4-0314": {"prompt_cost": 0.03, "completion_cost": 0.06, "per_tokens": 1000},
        "gpt-4-32k": {"prompt_cost": 0.06, "completion_cost": 0.12, "per_tokens": 1000},
        "gpt-4-32k-0314": {"prompt_cost": 0.06, "completion_cost": 0.12, "per_tokens": 1000},
        "gpt-3.5-turbo": {"prompt_cost": 0.002, "completion_cost": 0.002, "per_tokens": 1000},
        "gpt-3.5-turbo-0301": {"prompt_cost": 0.002, "completion_cost": 0.002, "per_tokens": 1000},
        "text-davinci-003": {"cost": 0.02, "per_tokens": 1000},
        "text-curie-001": {"cost": 0.002, "per_tokens": 1000},
        "text-babbage-001": {"cost": 0.0005, "per_tokens": 1000},
        "text-ada-001": {"cost": 0.0004, "per_tokens": 1000},
        "text-embedding-ada-002": {"cost": 0.0004, "per_tokens": 1000},
        "last_updated": "2023-04-12",
        "data_sources": [
            "https://openai.com/pricing",
            "https://platform.openai.com/docs/models/model-endpoint-compatibility"
        ]
    }

    def calculate_cost_for_tokens(self, tokens, price, per_tokens):
        return (float(tokens) / per_tokens) * price

    def calculate_cost(self, usage: dict, kwargs: dict):
        """
        Calculate cost & usage for a single round trip (request -> response)
        """
        model = kwargs.get("model") or kwargs.get("model_name")
        
        prompt_tokens = usage["prompt_tokens"]
        completion_tokens = usage["completion_tokens"]
        total_tokens = usage["total_tokens"]
        assert total_tokens == prompt_tokens + completion_tokens, "Total tokens does not match prompt + completion tokens"

        # prepare pricing data
        model_pricing_data = self.pricing_data[model]
        per_tokens = model_pricing_data["per_tokens"]

        if "prompt_cost" in model_pricing_data:
            """Model differentiates between prompt and completion costs"""
            prompt_price = model_pricing_data["prompt_cost"]
            completion_price = model_pricing_data["completion_cost"]

            prompt_cost = self.calculate_cost_for_tokens(prompt_tokens, prompt_price, per_tokens)
            completion_cost = self.calculate_cost_for_tokens(completion_tokens, completion_price, per_tokens)
            total_cost = prompt_cost + completion_cost
        else:
            """Model has a single cost for all tokens"""
            price = model_pricing_data["cost"]
            total_cost = self.calculate_cost_for_tokens(total_tokens, price, per_tokens)

        # messages = request["messages"] + response["messages"]

        return total_cost

        # cost_summary = {
        #     "model": model,
        #     "usage": {"prompt_tokens": prompt_tokens, "completion_tokens": completion_tokens, "total_tokens": total_tokens },
        #     "cost": total_cost,
        #     "messages": messages
        # }
        
        # return cost_summary, model_pricing_data
