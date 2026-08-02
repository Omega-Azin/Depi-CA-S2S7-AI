"""
Task-1, Task-2, Task-3, Task-4 solved separately in Python.
"""

import re


# =====================================================================
# TASK 1 — Email Validation / Parsing
# =====================================================================

def validate_and_parse_email(email: str):
    """
    - Valid email  : exactly one '@' and at least one '.' after the '@'.
    - Username     : part before '@'.
    - Domain       : part between '@' and the LAST '.'.
    - Domain type  : '.com' -> Commercial Domain
                      '.edu' -> Educational Domain
                      else   -> Other Domain
    """
    # --- Input Validation ---
    if email.count("@") != 1:
        return "Invalid email"

    username, rest = email.split("@")
    if "." not in rest:
        return "Invalid email"

    # --- Extract Username ---
    # (already have it: `username`)

    # --- Extract Domain (between '@' and the LAST '.') ---
    last_dot_index = rest.rfind(".")
    domain = rest[:last_dot_index]

    # --- Check Domain Ending ---
    if rest.endswith(".com"):
        domain_type = "Commercial Domain"
    elif rest.endswith(".edu"):
        domain_type = "Educational Domain"
    else:
        domain_type = "Other Domain"

    return {
        "username": username,
        "domain": domain,
        "domain_type": domain_type,
    }


# =====================================================================
# TASKS 2, 3, 4 — Decoding Messages
#
# Pattern used in every message:
#   junk_symbols + "word1 WORD2" + junk_symbols/digits
#
# Decoding steps:
#   1. Strip everything that is not a letter or a space -> "core" text.
#   2. Reverse the first word (it was written backwards).
#   3. Apply a vowel substitution to the second (all-caps) word,
#      using the mapping given in that specific task's instructions.
#   4. Join the two words back together.
# =====================================================================

def _extract_core(message: str) -> str:
    """Keep only letters and spaces, collapse extra whitespace."""
    core = re.sub(r"[^A-Za-z ]+", "", message)
    return core.strip()


def _reverse_first_word(word: str) -> str:
    return word[::-1]


def _apply_vowel_map(word: str, vowel_map: dict) -> str:
    return "".join(vowel_map.get(ch, ch) for ch in word)


def decode_message(message: str, vowel_map: dict) -> str:
    """Generic decoder driven by a task-specific vowel map."""
    core = _extract_core(message)
    words = core.split()

    first_word_decoded = _reverse_first_word(words[0])
    second_word_decoded = _apply_vowel_map(words[1], vowel_map)

    return f"{first_word_decoded} {second_word_decoded}"


# ---- Task 2 -----------------------------------------------------------
# "EPGTQ" -> no vowels changed in this example (map left empty on purpose,
# exactly as described in the task: "No vowels to change.")
TASK2_VOWEL_MAP = {}

def decode_task2(message: str) -> str:
    return decode_message(message, TASK2_VOWEL_MAP)


# ---- Task 3 -----------------------------------------------------------
# "PLIO" -> I->E, O->U  =>  "PLEU"
TASK3_VOWEL_MAP = {"I": "E", "O": "U"}

def decode_task3(message: str) -> str:
    return decode_message(message, TASK3_VOWEL_MAP)


# ---- Task 4 -----------------------------------------------------------
# "EPUVT" -> E->A, U->O  =>  "APOVT"
TASK4_VOWEL_MAP = {"E": "A", "U": "O"}

def decode_task4(message: str) -> str:
    return decode_message(message, TASK4_VOWEL_MAP)


# =====================================================================
# DEMO / TESTS
# =====================================================================
if __name__ == "__main__":
    print("=== TASK 1 ===")
    for test_email in ["Amit_ml@gmail.edu", "bad_email.com", "a@b@c.com", "user@site.com"]:
        print(f"{test_email!r:30} -> {validate_and_parse_email(test_email)}")

    print("\n=== TASK 2 ===")
    msg2 = "###!!@mocleW EPGTQ!!!6789"
    print(f"Input : {msg2}")
    print(f"Output: {decode_task2(msg2)}")

    print("\n=== TASK 3 ===")
    msg3 = "&&&**$gnirtS PLIO!!@1234"
    print(f"Input : {msg3}")
    print(f"Output: {decode_task3(msg3)}")

    print("\n=== TASK 4 ===")
    msg4 = "##$$$@!yalpstcejorp EPUVT****9887"
    print(f"Input : {msg4}")
    print(f"Output: {decode_task4(msg4)}")
