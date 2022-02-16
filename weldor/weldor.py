import sys

import string        as st
import math          as mt
import random        as rd
import collections   as cx
import heapq         as hq
import pkg_resources as pr
import readline      as rl


__version__ = 'v2.7.2022'

__author__ = 'ah'


# Alphabets
GREEN  = '*'
YELLOW = '+'
SILVER = '-'
feedbackset = {GREEN, YELLOW, SILVER}
wordbaseset = set(st.ascii_lowercase)

# Messages
winmessg = (
        'ig we win!',
        'good game!',
        'AIs rule!',
        'GG!',
        'easy peasy!',
        'haha!',
        'awesome sauce!',
        'to the victor go the spoils!',
        'poggers!',
        'pogchamp!',
        'no sweat!',
        'no grind!',
        'get rekt!',
        'peace!')

lossmessg = (
    'bad feedback?',
    'a typo somewhere?',
    'word list changed?',
    'how did we lose?',
    'the best-laid plans went astray?'
    'you messed up?')


def get_dict(filepath):
    '''
    Extract all words from dictionary
    located at

    :: filepath
       type - string
       desc - text file containing
              words in each line
    '''

    # Define variables
    wordbase = set()  # Set of words in filepath (unique)
    wordlen  = None   # Length of each word (constant)
    badfile  = False  # Is the dictionary file valid?

    # Process dictionary file
    with open(filepath) as infile:
        for line in infile:

            # Trim spaces and lower
            word = line.strip().lower()

            # Not a newline / EOF .. hence a word
            if word:

                # Are all chars in word legal?
                if set(word) <= wordbaseset:

                    # Do we have a constant length?
                    if wordlen is None:
                        # No, we record the first
                        # word's length
                        wordlen = len(word)

                    # Is the length valid / compatible?
                    if len(word) == wordlen:
                        wordbase.add(word)
                    else:
                        badfile = True

                # Illegal chars in word!
                else:
                    badfile = True

            # We encountered a bad file..
            if badfile:
                raise ValueError(
                    f'Unequal length or invalid word {word}')

    # Convert wordbase to list
    wordbase = list(wordbase)
    # And, then shuffle it!
    rd.shuffle(wordbase)

    # Return result
    return wordbase

def get_index():
    '''
    Load Wordle index words.
    These are answers.
    '''
    return get_dict(
        filepath=pr.resource_filename(
            'weldor',
            'wordbase/index.txt'))

def get_shell():
    '''
    Load Wordle shell words.
    These are valid guesses.
    '''
    return set(get_dict(
        filepath=pr.resource_filename(
            'weldor',
            'wordbase/shell.txt')))

def get_compatibility(p, q):
    '''
    Compute the compatibility b/w
    a potentially chosen word p,
    and the proposed word q.

    :: p
       type - string
       desc - secret word
    :: q
       type - string
       desc - proposed word
    '''

    # Define Structures
    compat     = [SILVER] * len(p) # Position-wise compatibility
    notcovered = cx.Counter(p)     # Letters in p not covered by q
    seconds    = []                # Second-pass analysis locations

    # Extract green matches
    # First-pass analysis
    for i in range(len(p)):

        # We have a match!
        if q[i] == p[i]:

            # Record location as green
            compat[i] = GREEN

            # Letter q[i] covers p
            # so decrease its count
            notcovered[q[i]] -= 1

        else:
            # Letter q[i] either yellow or silver
            seconds.append(i)

    # Extract yellows and silvers
    # Second-pass analysis
    for i in seconds:

        # Letter q[i] definitely in p
        # but not at the right location
        if notcovered[q[i]]:

            # So, its a yellow letter
            compat[i] = YELLOW
            # Decrease its count
            notcovered[q[i]] -= 1

        else:
            # Hence, its silver
            compat[i] = SILVER

    # Return result
    return ''.join(compat)

def stream_pairs(space):
    '''
    Stream word pair indices from
    the full search space.

    :: space
       type - tuple
       desc - integer indices of words
              in index currently valid
    '''
    return ((i,j) for i in space for j in space)

def get_entropy_heap(index, space):
    '''
    Compute and return the entropy
    max heap of all words in space.

    :: index
       type - list
       desc - a list of allowed words
    :: space
       type - tuple
       desc - integer indices of words
              in index currently valid
    '''

    # Define variables
    outcome_dict = {} # Outcome dictionary
    entropy_heap = [] # Entropy heap
    messg = ''   # Temporary message string
    clean = 0    # Console cleaning length
    spacecount = len(space) # Number of words in space

    # Build outcome dictionary
    for i,j in stream_pairs(space):

        # Fetch a pair of words (exhaustively)
        p,q = index[i], index[j]

        # Have we seen the porposed word?
        if not j in outcome_dict:
            outcome_dict[j] = cx.Counter()

        # Record q's unique outcome with
        # potential secret word p
        outcome_dict[j][
            get_compatibility(
                p=p,
                q=q)] += 1

        # Show some update
        if i == j:
            messg = f'  analyzing: {q}'
            clean = max(clean, len(messg))
            print(messg, end='\r')

    # Clean console
    print(' '*clean, end='\r')

    # Build entropy list
    while outcome_dict:

        # Pop a word and its outcome counter
        j,outcounter = outcome_dict.popitem()

        # Initialize entropy to zero
        h = 0.

        # Consume outcome counter
        while outcounter:

            # Pop the an unique outcome count
            _,outcount = outcounter.popitem()

            # What is the probability of this outcome?
            p  = outcount / spacecount

            # Add the entropy of this outcome
            h += p * mt.log(p, 2) # this is still negative

        # Store the result (min-heap!)
        entropy_heap.append((h,j))

        # Show some update
        messg = f' entropy({index[j]}) = {h:.2f}'
        clean = max(clean, len(messg))
        print(messg, end='\r')

    # Clear console
    print(' '*clean, end='\r')

    # Heapify result
    hq.heapify(entropy_heap)

    # Return result
    return entropy_heap

def extract_proposal(entropy_heap):
    '''
    Extract top 5 words from entropy
    max heap for user.

    :: entropy_heap
       type - list
       desc - a heap of all words and
              their negative entropies
    '''

    # Proposal extraction loop
    proposal = []
    while entropy_heap:

        # Extract highest entropy word
        h,j = hq.heappop(entropy_heap)

        # Adjust entropy (negate the negative)
        h = -h if h < 0. else 0.

        # Define result tuple
        r = (j,h,'bits')

        # We already have some proposa
        if proposal:

            # We have an equal entropy
            # proposal ... let's take it!
            if h == proposal[-1][1]:
                proposal.append(r)

            else:
                # We have less than 5 words
                # so we continue extraction
                if len(proposal) <= 5:
                    proposal.append(r)

                else:
                    # Adjust entropy result
                    h = -h if h < 0. else 0

                    # Store it back in the heap
                    hq.heappush(entropy_heap, (h,j))

                    # Break out!
                    break

         # We didn't propose anything
        else:
            # So, let's propose the first
            # word in the heap
            proposal.append(r)

    # Return result
    return proposal

def get_proposal_coverage(index, proposal):
    '''
    Compute the differential coverage
    dictionary of proposa list.

    :: index
       type - list
       desc - a list of allowed words
    :: proposal
       type - list
       desc - a list of top word indicess
              and their entropies
    '''

    # Extract coverage
    coverage = cx.Counter()
    for j,_,__ in proposal:
        # Each unique letter from proposed
        # word needs to be eliminated later
        coverage.update(set(index[j]))

    # Extract differential coverage
    coverage = {
        letter:count for letter,count in coverage.items() \
            if count < len(proposal)} # that is letter differential

    # Return result
    return coverage

def get_cover_score(word, coverage):
    '''
    Return the cover score of a word
    for a given coverage dictionary
    '''
    score = 0
    for c in set(word):
        if c in coverage:
            score += coverage[c]
    return score

def get_covers(source, index, coverage):
    '''
    Get cover words from source that
    maximize the differential coverage
    according to coverage dictionary.

    :: source
       type - generator
       desc - a stream of source words
              to evaluate for cover
     :: index
       type - list
       desc - a list of allowed words
    :: coverage
       type - dictionary
       desc - a dictionary of letters
              and their differential
              coverage count / score
    '''

    # Define variables
    cover_score = 0
    cover_words = []

    # Evaluation loop
    for j in source:

        # Fetch word
        word = index[j]

        # Compute the current coverage score
        # of a word from the source stream
        current_score = get_cover_score(
            word=word,
            coverage=coverage)

        # Is it better than anything before?
        if current_score > cover_score:
            # Update records
            cover_score = current_score
            cover_words = [j]

        # Equally good as current best!
        elif current_score == cover_score:
            # Retain if we have less than
            # 5 words for coverage
            if len(cover_words) < 5:
                cover_words.append(j)

    # Return result
    return cover_words, cover_score

def extract_hard_covers(
    entropy_heap,
    index,
    coverage):
    '''
    Return hard-mode compatible
    cover words from entropy heap.

    :: entropy_heap
       type - list
       desc - a heap of all words and
              their negative entropies
    :: index
       type - list
       desc - a list of allowed words
    :: coverage
       type - dictionary
       desc - a dictionary of letters
              and their differential
              coverage count / score
    '''
    return get_covers(
        source=(entropy_heap.pop()[1] for _ in range(len(entropy_heap))),
        index=index,
        coverage=coverage)

def get_soft_covers(
    index,
    space,
    coverage):
    '''
    Return global compatible cover words
    from index, but may not be hard-mode
    compatible for plays.

    :: index
       type - list
       desc - a list of allowed words
    :: space
       type - tuple
       desc - integer indices of words
              in index currently valid
    :: coverage
       type - dictionary
       desc - a dictionary of letters
              and their differential
              coverage count / score
    '''
    return get_covers(
        source=set(range(len(index)))-space,
        index=index,
        coverage=coverage)

def propose_words(index, space):
    '''
    For all words in index, and the
    current search space, return a
    list of good quality words.

    :: index
       type - list
       desc - a list of allowed words
    :: space
       type - tuple
       desc - integer indices of words
              in index currently valid
    '''

    # Get entropy heap
    entropy_heap = get_entropy_heap(
        index=index,
        space=space)

    # Extract proposal
    proposal = extract_proposal(
        entropy_heap=entropy_heap)

    # Compute proposal coverage
    coverage = get_proposal_coverage(
        index=index,
        proposal=proposal)

    # Do we need to break cover?
    if len(proposal) > 1:

        # Extract hard cover
        hard_cover_words, cover_score = extract_hard_covers(
            entropy_heap=entropy_heap,
            index=index,
            coverage=coverage)

        # Otherwise, extract soft cover
        if not hard_cover_words:
            soft_cover_words, cover_score = get_soft_covers(
                index=index,
                space=space,
                coverage=coverage)

            # Extend proposal with soft covers
            proposal.extend(
                (w,cover_score,'scov') for w in soft_cover_words)

        else:
            # Extend proposal with hard covers
            proposal.extend(
                (w,cover_score,'hcov') for w in hard_cover_words)


    # Return result
    return proposal[::-1]

def shrink_space(index, space, word, feedback):
    '''
    Reduce the search space based on feedback
    on the proposed word.

    :: index
       type - list
       desc - a list of allowed words
    :: space
       type - tuple
       desc - integer indices of words
              in index currently valid
    :: word
       type - string
       desc - proposed / played word
    :: feedback
       type - string
       desc - string encoding the feedback
              from the Wordle-variant
    '''
    _space = set()
    for j in space:
        if get_compatibility(index[j], word) == feedback:
            _space.add(j)
    return _space

def display_suggestions(words, index):
    '''
    Display all proposed words in a nice
    format for user consumption.

    :: words
       type - list
       desc - a list of tuples containing
              the indexes of proposed words
              and their information values
    :: index
       type - list
       desc - a list of allowed words
    '''

    # Do we have words?
    if words:
        # Determine grammar
        thisval = 'these?' if len(words) > 1 else 'this!!'

        # Print suggestions
        print(f'\n  try {thisval}')
        for j,s,t in words:
            if t == 'bits':
                print(f'   - {index[j]} ({s:.2f} {t})')
            else:
                print(f'   - {index[j]} ({s} {t})')

            # Add words to history for scrolling
            rl.add_history(index[j])

        # Only one word proposed .. we won!
        if len(words) == 1:
            print(f'   - {rd.choice(winmessg)}')
            print('\n weldor out!\n')
            sys.exit(0)

        # Suggestion list completed
        else:
            print()

    # We don't .. game over!
    else:
        print(f'\n {rd.choice(lossmessg)}')
        print(' weldor out!\n')
        sys.exit(0)

def process_feedback(width):
    '''
    Parse the feedback from user.

    :: width
       type - integer
       desc - a valid feedback length
    '''

    # Feedback input loop
    while True:
        feedback = str(input('   feedback: '))

        # Feedback is valid?
        if set(feedback) <= feedbackset and \
           len(feedback) == width:
            # Return control to weldor REPL
            break

    # Feedback say's we won!
    if feedback.count(GREEN) == width:
        print(f'\n {rd.choice(winmessg)}')
        print(' weldor out!\n')
        sys.exit(0)

    # Return feedback for dictionary
    # elimination downstream
    return feedback

def weldor():
    '''
    weldor interactive REPL.
    '''

    # Print introduction
    print(f'\n weldor {__version__}')
    print(f' by {__author__}')

    # Load index and shell objects
    print(f'\n loading ...', end='\r')
    index = get_index()            # A list of all answer words
    width = len(index[0])          # Length of each word
    space = set(range(len(index))) # A set of all integer indices to index
    ixset = set(index)             # A set of all valid answer
    ixset.update(get_shell())      #   words and allowed guesses

    # Select a random compatible pair
    for i,j in stream_pairs(space):
        p = index[i] # A randomly selected word
        q = index[j] # A randomly proposed word
        c = get_compatibility(p, q)

        # All three symbols in compatibility
        # between p and q (useful for user)
        if set(c) == feedbackset:
            rl.add_history(p) # Add to history
            rl.add_history(q) # Add to history
            break

    # Display result
    print(f' {q} (played)')
    print(f' {c} ')
    print(f' {p} (secret)\n')

    # Have we helped the user?
    helped = False # No ...

    # weldor REPL
    while True:

        # Get an input word from user
        word = str(input(' enter word: ')).lower()

        # Is the word a valid guess?
        if word in ixset:
            # Ask for feedback and process it
            feedback = process_feedback(width)
            # Based on feedback, shrink search space
            space = shrink_space(index, space, word, feedback)
            # Display suggested words based on state space
            display_suggestions(
                words=propose_words(index, space), # Proposed list
                index=index)

        else:
            # Have we not helped the user?
            if not helped:
                # Now we have!
                helped = True
                # Display some suggestions (could be slow!)
                display_suggestions(
                    words=propose_words(index, space),
                    index=index)

if __name__ == '__main__':
    weldor()
