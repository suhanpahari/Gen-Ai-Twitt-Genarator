import streamlit as st
from few_shot import FewShotPosts
from post_gen import generate_post
import random

# Trending Hashtags Dictionary
trending_hashtags = {
    "business": [
        "#business", "#digitalmarketing", "#entrepreneur", "#marketing", "#fyp",
        "#motivation", "#success", "#smallbusiness", "#money", "#viral",
        "#entrepreneurship", "#onlinebusiness", "#mindset", "#trending", "#love",
        "#businessowner", "#socialmediamarketing", "#finance", "#startup", "#investment"
    ],
    "education": [
        "#education", "#learning", "#studyabroad", "#motivation", "#school",
        "#study", "#students", "#trending", "#student", "#stockmarket",
        "#love", "#reels", "#explore", "#india", "#business", "#knowledge",
        "#science", "#college", "#stockmarkettrade", "#university"
    ],
    "technology": [
        "#technology", "#tech", "#ai", "#innovation", "#artificialintelligence", "#business",
        "#cybersecurity", "#apple", "#programming", "#coding", "#engineering", "#samsung",
        "#iphone", "#education", "#trending", "#science", "#mobile", "#smartphone", "#gadgets", "#software"
    ],
    "personalbranding": [
        "#personalbranding", "#digitalmarketing", "#branding", "#marketing", "#passiveincome",
        "#personalbrand", "#socialmediamarketing", "#digitalproducts", "#business", "#entrepreneurship",
        "#entrepreneur", "#onlinebusiness", "#socialmedia", "#success", "#win", "#wifimoney",
        "#contentcreator", "#sidehustle", "#motivation", "#ecommerce"
    ]
}

# Options for length and language
length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Hinglish"]

# Main app layout
def main():
    st.title("X (Twitter) Post Generator: ")
    st.markdown("Generate professional Twitt with just a few clicks.")

    # Sidebar for input filters
    st.sidebar.header("Customize Your Post")
    
    # Get predefined list of topics from FewShotPosts class
    fs = FewShotPosts()
    tags = fs.get_tags()  # Assuming this returns a list of trending topics or user-chosen tags

    # Sidebar filters
    selected_tag = st.sidebar.selectbox("Select a Topic", options=tags , help="Choose the main topic for your post.")
    selected_length = st.sidebar.selectbox("Select Post Length", options=length_options, help="Choose the desired length.")
    selected_language = st.sidebar.selectbox("Select Language", options=language_options, help="Choose the language for your post.")
    
    # Hashtag Category Filter: Multiple categories can be selected
    selected_categories = st.sidebar.multiselect("Select Hashtag Categories", 
                                                options=list(trending_hashtags.keys()), 
                                                help="Select categories to generate hashtags from.")
    
    # Hashtag Number Selection: User selects how many hashtags they want
    num_hashtags = st.sidebar.slider("Select Number of Hashtags", min_value=1, max_value=20, value=5, help="Choose how many hashtags to generate.")

    # Custom hashtag input for multiple hashtags
    custom_hashtags_input = st.sidebar.text_area("Enter custom hashtags (optional)", 
                                                 help="Add custom hashtags, separated by commas (e.g. #CustomTag, #AnotherTag)")

    # Main section
    st.header("Your Generated Twitt")

    if st.button("Generate Post"):
        if selected_tag and selected_length and selected_language:
            try:
                # Generate the LinkedIn post using the selected options
                post = generate_post(selected_length, selected_language, selected_tag)
                st.success("Here's your Twitt:")
                #st.write(post)

                # Generate hashtags based on the selected categories and custom input
                hashtags = generate_hashtags(selected_categories, num_hashtags, custom_hashtags_input)
                #st.write(f"Suggested Hashtags: {', '.join(hashtags)}")

                # Format and append hashtags to the post
                post_with_hashtags = format_post_with_hashtags(post, hashtags)
                #st.write("Post with Hashtags:")
                st.write(post_with_hashtags)

            except Exception as e:
                st.error(f"An error occurred while generating the post: {e}")
        else:
            st.warning("Please ensure all fields are selected before generating a post.")
            
    # Footer
    st.markdown("""
        <hr>
        <div style="text-align:center;">
            <small>Created by @shm</small>
        </div>
        """, unsafe_allow_html=True)


def generate_hashtags(categories, num_hashtags, custom_hashtags_input):
    """
    Generates hashtags based on the selected categories and optional custom words.
    """
    # Collect hashtags from the selected categories
    selected_hashtags = []
    for category in categories:
        selected_hashtags.extend(trending_hashtags.get(category, []))

    # If custom hashtags are provided, split by commas and add each as a hashtag
    if custom_hashtags_input:
        custom_hashtags = [f"#{hashtag.strip().replace(' ', '')}" for hashtag in custom_hashtags_input.split(',') if hashtag.strip()]
        selected_hashtags.extend(custom_hashtags)

    # Ensure there are no duplicates
    selected_hashtags = list(set(selected_hashtags))

    # If more hashtags are requested than available, adjust the selection
    if len(selected_hashtags) < num_hashtags:
        return selected_hashtags

    return random.sample(selected_hashtags, num_hashtags)


def format_post_with_hashtags(post, hashtags):
    """
    Formats the post by adding the hashtags in a new line.
    Ensures no trailing commas are added if empty hashtags are given.
    """
    # Combine both default and custom hashtags
    formatted_hashtags = " ".join([hashtag for hashtag in hashtags if hashtag.strip()])  # Removes empty or malformed hashtags
    
    # Add hashtags to the post with a line break
    return f"{post}{formatted_hashtags}"



# Run the app
if __name__ == "__main__":
    main()
