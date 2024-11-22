from llm_add import llm
from few_shot import FewShotPosts

few_shot = FewShotPosts()

def get_length_str(length):
    """
    Maps the length category to a descriptive string for post length.
    """
    length_map = {
        "Short": "1 to 5 lines",
        "Medium": "6 to 10 lines",
        "Long": "11 to 15 lines",
    }
    return length_map.get(length, "6 to 10 lines")  # Default to Medium if invalid input


def generate_post(length, language, tag):
    """
    Generates a LinkedIn post based on the provided length, language, and topic (tag).
    """
    # Validate inputs
    if not length or not language or not tag:
        raise ValueError("Length, language, and tag must be provided.")

    # Create prompt
    prompt = get_prompt(length, language, tag)

    try:
        # Invoke the LLM to generate a response
        response = llm.invoke(prompt)
        return response.content.strip()  # Remove any extra whitespace
    except Exception as e:
        raise RuntimeError(f"Failed to generate post: {e}")


def get_prompt(length, language, tag):
    """
    Constructs a prompt for generating a LinkedIn post with optional examples.
    """
    # Convert length to descriptive string
    length_str = get_length_str(length)

    # Base prompt
    prompt = f"""
    Generate a LinkedIn post using the information below. No preamble.
    1) Topic: {tag}
    2) Length: {length_str}
    3) Language: {language}
    If Language is Hinglish, it means a mix of Hindi and English. 
    The script for the generated post should always be in English.
    """

    # Retrieve example posts for few-shot learning
    examples = few_shot.get_filtered_posts(length, language, tag)

    if examples:
        prompt += "\n4) Use the writing style as per the following examples:"
        for i, post in enumerate(examples[:2]):  # Use up to 2 examples
            prompt += f"\n\nExample {i + 1}:\n{post['text']}"

    return prompt


if __name__ == "__main__":
    try:
        # Example usage
        post = generate_post("Medium", "English", "Mental Health")
        print("Generated LinkedIn Post:")
        print(post)
    except Exception as e:
        print(f"An error occurred: {e}")