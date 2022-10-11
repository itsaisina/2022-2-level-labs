"""
Co-occurrence-driven keyword extraction starter
"""

from pathlib import Path
from lab_2_keywords_cooccurrence.main import (extract_phrases,
                                              extract_candidate_keyword_phrases,
                                              calculate_frequencies_for_content_words,
                                              calculate_word_degrees,
                                              calculate_word_scores,
                                              calculate_cumulative_score_for_candidates,
                                              get_top_n,
                                              extract_candidate_keyword_phrases_with_adjoining,
                                              calculate_cumulative_score_for_candidates_with_stop_words,
                                              generate_stop_words,
                                              load_stop_words)


def read_target_text(file_path: Path) -> str:
    """
    Utility functions that reads the text content from the file
    :param file_path: the path to the file
    :return: the text content of the file
    """
    with open(file_path, 'r', encoding='utf-8') as target_text_file:
        return target_text_file.read()


def text_processing(text, stop_words):
    candidate_keyword_phrases, frequencies_for_content_words, word_degrees, word_scores, cumulative_score, \
        candidate_keyword_phrases_with_adjoining = [None for not_def in range(6)]
    phrases = extract_phrases(text)
    if phrases:
        candidate_keyword_phrases = extract_candidate_keyword_phrases(phrases, stop_words)

    if candidate_keyword_phrases:
        frequencies_for_content_words = calculate_frequencies_for_content_words(candidate_keyword_phrases)

    if candidate_keyword_phrases and frequencies_for_content_words:
        word_degrees = calculate_word_degrees(candidate_keyword_phrases, list(frequencies_for_content_words.keys()))

    if word_degrees and frequencies_for_content_words:
        word_scores = calculate_word_scores(word_degrees, frequencies_for_content_words)

    if candidate_keyword_phrases and word_scores:
        cumulative_score = calculate_cumulative_score_for_candidates(candidate_keyword_phrases, word_scores)

    if cumulative_score:
        print(get_top_n(cumulative_score, 5, 3))

    if candidate_keyword_phrases and phrases:
        candidate_keyword_phrases_with_adjoining = extract_candidate_keyword_phrases_with_adjoining(
                                                   candidate_keyword_phrases, phrases)

    if candidate_keyword_phrases_with_adjoining and word_scores and stop_words:
        calculate_cumulative_score_for_candidates_with_stop_words(candidate_keyword_phrases_with_adjoining, word_scores,
                                                                  stop_words)


if __name__ == "__main__":
    # finding paths to the necessary utils
    PROJECT_ROOT = Path(__file__).parent
    ASSETS_PATH = PROJECT_ROOT / 'assets'

    # reading list of stop words
    STOP_WORDS_PATH = ASSETS_PATH / 'stop_words.txt'
    with open(STOP_WORDS_PATH, 'r', encoding='utf-8') as fd:
        stop_words = fd.read().split('\n')

    # reading the text from which keywords are going to be extracted
    TARGET_TEXT_PATH_GENOME = ASSETS_PATH / 'genome_engineering.txt'
    TARGET_TEXT_PATH_ALBATROSS = ASSETS_PATH / 'albatross.txt'
    TARGET_TEXT_PATH_PAIN_DETECTION = ASSETS_PATH / 'pain_detection.txt'
    TARGET_TEXT_PATH_GAGARIN = ASSETS_PATH / 'gagarin.txt'

    corpus = {
        'gagarin': read_target_text(TARGET_TEXT_PATH_GAGARIN),
        'albatross': read_target_text(TARGET_TEXT_PATH_ALBATROSS),
        'genome_engineering': read_target_text(TARGET_TEXT_PATH_GENOME),
        'pain_detection': read_target_text(TARGET_TEXT_PATH_PAIN_DETECTION)
    }

    for exact_text in corpus:
        text_processing(corpus[exact_text], stop_words)

    LOADED_STOP_WORDS = load_stop_words(ASSETS_PATH / 'stopwords.json')

    if LOADED_STOP_WORDS:
        text_processing(read_target_text(ASSETS_PATH / 'polish.txt'), LOADED_STOP_WORDS)

    UNKNOWN_TEXT = read_target_text(ASSETS_PATH / 'unknown.txt')
    STOP_WORDS_IN_UNKNOWN_TEXT = list(generate_stop_words(UNKNOWN_TEXT, 10))
    if STOP_WORDS_IN_UNKNOWN_TEXT:
        text_processing(UNKNOWN_TEXT, STOP_WORDS_IN_UNKNOWN_TEXT)

    RESULT = True
    assert RESULT, 'Keywords are not extracted'
