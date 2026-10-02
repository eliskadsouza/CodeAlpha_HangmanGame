import random
import streamlit as st

# ASCII Art Visuals for the 6 wrong guess stages
HANGMAN_PICS = [
    """
       +---+
       |   |
           |
           |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
           |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
       |   |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|   |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|\\  |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|\\  |
      /    |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|\\  |
      / \\  |
           |
    =========
    """,
]

# Predefined word list with hints (Bonus Feature)
WORDS = {
    "PYTHON": "A popular programming language",
    "GALAXY": "A massive system of stars and planets",
    "JUNGLE": "A dense tropical forest",
    "RHYTHM": "A strong, repeated pattern of movement or sound",
    "WIZARD": "A person with magical powers",
}


def start_new_game():
    word, hint = random.choice(list(WORDS.items()))
    st.session_state.word = word
    st.session_state.hint = hint
    st.session_state.guessed_letters = []
    st.session_state.attempts_left = 6
    st.session_state.game_over = False
    st.session_state.won = False


# Initialize Session State
if "word" not in st.session_state:
    start_new_game()

# Streamlit Page Config
st.set_page_config(page_title="Hangman Game", page_icon="🎯", layout="centered")

st.title("🎯 Classic Hangman Game")
st.write("Guess the word one letter at a time before the gallows are built!")

# Sidebar Info & Controls
with st.sidebar:
    st.header("⚙️ Controls")
    if st.button("🔄 New Game", use_container_width=True):
        start_new_game()
        st.rerun()

    st.markdown("---")
    st.markdown("**💡 Hint:** " + st.session_state.hint)

# Game Display Logic
wrong_guesses = [
    l for l in st.session_state.guessed_letters if l not in st.session_state.word
]
incorrect_count = len(wrong_guesses)
st.session_state.attempts_left = 6 - incorrect_count

# Display Hangman ASCII Art
st.code(HANGMAN_PICS[incorrect_count], language="text")

# Display Secret Word Progress
display_word = " ".join(
    [
        letter if letter in st.session_state.guessed_letters else "_"
        for letter in st.session_state.word
    ]
)
st.markdown(f"### Word: `{display_word}`")

# Game Status Metrics
col1, col2 = st.columns(2)
with col1:
    st.metric("Attempts Remaining", st.session_state.attempts_left)
with col2:
    st.write(
        "**Guessed Letters:**",
        ", ".join(st.session_state.guessed_letters) or "None",
    )

# Check Win/Loss
if "_" not in display_word:
    st.success(f"🎉 Congratulations! You guessed the word: **{st.session_state.word}**")
    st.session_state.game_over = True
elif st.session_state.attempts_left <= 0:
    st.error(f"💀 Game Over! The correct word was **{st.session_state.word}**.")
    st.session_state.game_over = True

# User Input Controls
if not st.session_state.game_over:
    st.markdown("---")
    letter_input = st.text_input(
        "Enter a single letter:", max_chars=1, key="input_box"
    ).upper()

    if st.button("Submit Guess") and letter_input:
        if not letter_input.isalpha():
            st.warning("Please enter a valid alphabet letter.")
        elif letter_input in st.session_state.guessed_letters:
            st.warning(f"You already guessed '{letter_input}'. Try another one!")
        else:
            st.session_state.guessed_letters.append(letter_input)
            st.rerun()