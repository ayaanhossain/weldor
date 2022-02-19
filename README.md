<h1 align="center">
    <a href="https://github.com/ayaanhossain/weldor/">
        <img src="https://raw.githubusercontent.com/ayaanhossain/repfmt/main/weldor/img/logo.svg"  alt="weldor" width="270" class="center"/>
    </a>
</h1>

<p align="center">
  <a href="#weldor-in-Action">weldor in Action!</a> •
  <a href="#Installation">Installation</a> •
  <a href="#World-of-Wordle">World of Wordle</a> •
  <a href="#Modifying-weldor">Modifying weldor</a> •
  <a href="#License">License</a>
</p>


`weldor` is a simple reactive AI designed to assist you in playing [Wordle](https://www.powerlanguage.co.uk/wordle/) and [some of its derivatives](https://www.cnet.com/tech/gaming/wordle-spinoffs-other-word-games-to-try-if-you-cant-get-enough/). Rather than just giving you [a single answer with the highest entropy](https://www.nme.com/news/gaming-news/wordle-fan-uses-maths-to-find-the-statistically-best-word-to-try-first-3156632) at each step, `weldor` combines [a classic combinatorics concept](https://en.wikipedia.org/wiki/Set_cover_problem) to give you multiple choices for your turns. By reducing Wordle variants to a game of deduction that still allows for gambling, rather than memorization or recall, `weldor` allows the player to both enjoy and win these games in a few rounds. You can also [change the dictionary](#Modifying-weldor) used by `weldor` for other variants.

<p align="center">
    <a href="https://replit.com/@bioalgorithmist/weldor#.replit">
        <img src="https://raw.githubusercontent.com/ayaanhossain/repfmt/main/weldor/img/replit.svg"  alt="You can try `weldor` live on repl.it at https://replit.com/@bioalgorithmist/weldor#.replit" width="170" class="center"/>
    </a>
</p>


## `weldor` in Action!

```python
 $ weldor              # type in "weldor" in your terminal and press ENTER to start

 weldor v2.7.2022      # program and version
 by ah                 # author

 guile (played)        # let's say you played "guile"
 ---*+                 # (feedback must have silvers as "-", greens as "*" and yellows as "+")
 newly (secret)        # "---*+" is then the encoded feedback if the secret was "newly" (true?)

 enter word: no idea   # weldor asks you to enter a word, but you say "no idea"

  try these?           # weldor then searches the space and proposes the following words
   - shirt (15 hcov)   #
   - first (15 hcov)   # the words and their information scores
   - skirt (15 hcov)   # are presented in sorted order for your
   - wrist (15 hcov)   # evaluation
   - strip (15 hcov)   #
   - arise (5.82 bits) # words selected based on high entropy are scored in bits and help
   - trace (5.83 bits) # in quickly eliminating large sections of the search space,
   - irate (5.83 bits) # while cover words are scored by differential alphabet coverage
   - crate (5.83 bits) #
   - slate (5.86 bits) # however, these are only suggestions,
   - raise (5.88 bits) # and you're free to ignore them

 enter word: grate     # instead of choosing "irate" or "crate" you play "grate" (the defiance!)
   feedback: -----     # and you're faced with all silvers in response (lol)

  try these?           # analyzing the outcome, weldor suggests the following
   - solid (19 hcov)   #
   - spoil (5.39 bits) # words with cover scores (scov and hcov) are selected to eliminate
   - slick (5.39 bits) # as many high entropy words as possible (tie-breaker); hcov words
   - noisy (5.40 bits) # are hard-mode compliant, but scov words may not be so
   - could (5.42 bits) #
   - lousy (5.42 bits) # you can opt to play a cover word with high value when the high
   - slimy (5.42 bits) # entropy words are very similar to each other in composition

 enter word: solid     # you decide to play "solid" which does a solid job of differentially
   feedback: -++--     # eliminating all words selected based on entropy

  try these?           # another round of suggestions from weldor!
   - knoll (6 hcov)    #
   - flown (2.16 bits) #     what the heck is a knoll?? is that a real word?
   - clock (2.16 bits) #
   - blown (2.25 bits) # the high entropy words are starting to look
   - flock (2.50 bits) # similar in composition, so maybe play another
   - clown (2.50 bits) # cover? or maybe not, they're not all the same
   - block (2.50 bits) # if you look at it carefully ... ?

 enter word: flock     # you choose flock ...
   feedback: -+*-+     # and enter the feedback from Wordle

  try this!!           # and et voila!
   - knoll (0.00 bits) # that just leaves you with one word to try and win this
   - pogchamp!         # (but maybe you could have won earlier with knoll..)

 weldor out!           # so long, weldor
```

## Installation

`weldor` is pure-python, and requires `Python 3.6` or above. It was developed and tested using Ubuntu Linux on [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/about) but it should also be compatible with macOS.

> Note: there may be some issues related to the GNU `readline` library on macOS which `weldor` needs to enable the use of `←`, `↑`, `→` and `↓` keys for selecting the words from suggested lists.

Installation is very easy with `pip`.

On your terminal, just use `pip` like so
```bash
$ pip install --upgrade weldor
```
and that should be it!

**Uninstallation** of `weldor` is easily done using
```bash
$ pip uninstall weldor
```

## World of Wordle

Since its release Wordle has garnered the attention of everyone everywhere. Variants have emerged.

* [Wordle](https://www.nytimes.com/games/wordle/index.html). The classic, with one secret word you have to guess daily. The goal is to solve the puzzle in 6 attempts or less. `weldor` can be used directly here.

* [Wordle Archive](https://metzger.media/games/wordle-archive/). A collection of all past Wordle games published so far. Also features a [randomized Wordle](https://metzger.media/games/wordle-archive/?random=play) as well as a [Word Race](https://metzger.media/games/word-race). Use `weldor` to beat others in races.

* [Absurdle](https://qntm.org/files/absurdle/absurdle.html). An adversarial version of Wordle that is designed to prolong the game. I am not exactly sure, but, Absurdle tries to eliminate your proposed words as much as possible, as long as there are other words it can switch to from the one it selected initially that are all compatible with previously generated colored feedback. The best strategy here with `weldor` is to not always play the highest entropy word at each step, but play a couple of random/fun ones that might throw the adversary off a little bit.

* [Dordle](https://zaratustra.itch.io/dordle). A randomized version of Wordle in which you have to guess two different words by proposing a single five-letter word for both. Definitely a good version to play with `weldor`. My strategy here is to start two separate `weldor` sessions, play the same word with both but based on the two feedback, continue with the word that has the highest entropy from both sessions combined.

* [Quordle](https://www.quordle.com/). Similar to Dordle, but you gotta guess 4 words with a single proposal. So, you'd need 4× `weldor` sessions.

* [Word Master](https://octokatherine.github.io/word-master/) and [hello wordl](https://hellowordl.net/). Unlimited Wordle clones. The hello wordl variant allows the use of different length words, which means you'll need to modify the dictionaries `weldor` uses under the hood (see next section). Check [this repo](https://github.com/dwyl/english-words) to obtain a collection of 466,000+ English words of various length. You'll need to write your own code to filter for words of a certain length.

* [Lewdle](https://www.lewdlegame.com/). Like Wordle, but with lewd words. I know where to find the dictionary, but I don't think I need `weldor` for this variant.

* [A host of topical clones](https://github.com/cwackerfuss/react-wordle). There are so many custom Wordle variants that use custom dictionaries, beyond just the ones from the English language, including [Numble](https://rbrignall.github.io/numble/) and [Nerdle](https://nerdlegame.com/). For Nerdle in particular, one can enumerate all 1,139,062,500 possible equations, evaluate them for mathematical correctness, and then save the filtered ones in a plaintext dictionary. For others, you might have to go through the game's page source or open reddit threads.


## Modifying `weldor`

To modify `weldor`, you'll need to clone this repository.
```bash
$ git clone https://github.com/ayaanhossain/weldor.git
```

Once cloned, you can replace the two dictionaries, inside `/weldor/weldor/wordbase/`, named [shell.txt](https://github.com/ayaanhossain/weldor/blob/main/weldor/wordbase/shell.txt) and [index.txt](https://github.com/ayaanhossain/weldor/blob/main/weldor/wordbase/index.txt).
```bash
$ ll weldor/weldor/wordbase
total 92
drwxrwxrwx 1 owner owner  4096 Feb 7 23:55 ./
drwxrwxrwx 1 owner owner  4096 Feb 7 23:55 ../
-rwxrwxrwx 1 owner owner 13889 Feb 7 23:55 index.txt*
-rwxrwxrwx 1 owner owner 74597 Feb 7 23:55 shell.txt*
```

The `shell.txt` file stores all guesses that are valid, but not really the answers, while `index.txt` file stores the answers -- direct Wordle clones use this discrimination.

If your variant does not have separated concepts of `shell` and `index`, then put your word list as an `index.txt`, and leave the `shell.txt` blank.

Please also feel free to change the logic in `propose_words(...)` function inside `weldor.py` (or anything else for that matter) to suit your needs as well as modify the `wordbaseset` variable to include your alphabets. If you come up with some cool modification to `weldor`, I'd love to hear about it ([open an issue](https://github.com/ayaanhossain/weldor/issues), maybe?).

Once you've modified `weldor`, simply use
```bash
$ python setup.py install
```
from the main directory to install your modified version.


## License

`weldor` (c) 2022 Ayaan Hossain.

`weldor` is an **open-source software** under MIT License.

See [LICENSE](https://github.com/ayaanhossain/weldor/blob/main/LICENSE) file for more details.
