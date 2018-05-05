# Youtube Comments Analyzer
### Youtube comments topics modeling and sentiment analyzer

Youtube Comments Analyzer is a Python scripted tool to collect and analyze Youtube's videos comments (in Arabic). Tool provides the service of sentiment analysis and topics modeling based on arguments submitted by user. 

## Table of contents

- [Installation](#installation)
- [Requirements](#requirements)
- [Usage example](#usage-example)
- [Adding new languages](#adding-new-languages)
- [Adding and overwriting words](#adding-and-overwriting-words)
- [API Reference](#api-reference)
- [How it works](#how-it-works)
- [Benchmarks](#benchmarks)
- [Validation](#validation)
- [Testing](#testing)

## Installation
Visit https://github.com/arghodayah/Youtube-Comments-Analyzer/archive/master.zip and download all files to your directory.

## Requirements
- many_stop_words==0.2.2
- httplib2==0.11.3
- gensim==3.4.0
- Flask==1.0.2 (For web endpoint only)
- nltk==3.2.5
- pymongo==3.6.1
- google_api_python_client==1.6.7

## Usage example
Usage: analyze.py Tool Arg1 Arg2

       Tool: 'topics' or 'sentiment'
       Arg1: topics=>Quantity of topics, sentiment=>'video' or 'text'
       Arg2: topics=>Videos IDs seperated by commas(,), sentiment=>Video ID or Text
- Comments Topics Modeling (Supports multiple videos)
```bash
python3 analyze.py topics <number of topics> <Youtube videos IDs separated by commas(,)>
```
- Comments Sentiment Analysis (Single video)
```bash
python3 analyze.py sentiment video <Youtube video ID>
```
- Text Sentiment Analysis
```bash
python3 analyze.py sentiment text '<Your text>'
```
- Sentiment Scores (Accuracy and F-Measure)
```bash
python3 analyze.py sentiment scores
```
- Text Sentiment Analysis (Web Endpoint)
```bash
python3 websentiment.py
```
## Adding new languages
You can add support for a new language by registering it using the `registerLanguage` method:

```js
var frLanguage = {
  labels: { 'stupide': -2 }
};
sentiment.registerLanguage('fr', frLanguage);

var result = sentiment.analyze('Le chat est stupide.', { language: 'fr' });
console.dir(result);    // Score: -2, Comparative: -0.5
```

You can also define custom scoring strategies to handle things like negation and emphasis on a per-language basis:
```js
var frLanguage = {
  labels: { 'stupide': -2 },
  scoringStrategy: {
    apply: function(tokens, cursor, tokenScore) {
      if (cursor > 0) {
        var prevtoken = tokens[cursor - 1];
        if (prevtoken === 'pas') {
          tokenScore = -tokenScore;
        }
      }
      return tokenScore;
    }
  }
};
sentiment.registerLanguage('fr', frLanguage);

var result = sentiment.analyze('Le chat n\'est pas stupide', { language: 'fr' });
console.dir(result);    // Score: 2, Comparative: 0.4
```

## Adding and overwriting words
You can append and/or overwrite values from AFINN by simply injecting key/value pairs into a sentiment method call:
```javascript
var options = {
  extras: {
    'cats': 5,
    'amazing': 2
  }
};
var result = sentiment.analyze('Cats are totally amazing!', options);
console.dir(result);    // Score: 7, Comparative: 1.75
```

## API Reference

#### `var sentiment = new Sentiment([options])`

| Argument | Type       | Required | Description                                                |
|----------|------------|----------|------------------------------------------------------------|
| options  | `object`   | `false`  | Configuration options _(no options supported currently)_   |

---

#### `sentiment.analyze(phrase, [options], [callback])`

| Argument | Type       | Required | Description             |
|----------|------------|----------|-------------------------|
| phrase   | `string`   | `true`   | Input phrase to analyze |
| options  | `object`   | `false`  | Options _(see below)_   |
| callback | `function` | `false`  | If specified, the result is returned using this callback function |


`options` object properties:

| Property | Type      | Default | Description                                                   |
|----------|-----------|---------|---------------------------------------------------------------|
| language | `string`  | `'en'`  | Language to use for sentiment analysis                        |
| extras   | `object`  | `{}`    | Set of labels and their associated values to add or overwrite |

---

#### `sentiment.registerLanguage(languageCode, language)`

| Argument     | Type     | Required | Description                                                         |
|--------------|----------|----------|---------------------------------------------------------------------|
| languageCode | `string` | `true`   | International two-digit code for the language to add                |
| language     | `object` | `true`   | Language module (see [Adding new languages](#adding-new-languages)) |

---

## How it works
### AFINN
AFINN is a list of words rated for valence with an integer between minus five (negative) and plus five (positive). Sentiment analysis is performed by cross-checking the string tokens(words, emojis) with the AFINN list and getting their respective scores. The comparative score is simply: `sum of each token / number of tokens`. So for example let's take the following:

`I love cats, but I am allergic to them.`

That string results in the following:
```javascript
{
    score: 1,
    comparative: 0.1111111111111111,
    tokens: [
        'i',
        'love',
        'cats',
        'but',
        'i',
        'am',
        'allergic',
        'to',
        'them'
    ],
    words: [
        'allergic',
        'love'
    ],
    positive: [
        'love'
    ],
    negative: [
        'allergic'
    ]
}
```

* Returned Objects
    * __Score__: Score calculated by adding the sentiment values of recongnized words.
    * __Comparative__: Comparative score of the input string.
    * __Token__: All the tokens like words or emojis found in the input string.
    * __Words__: List of words from input string that were found in AFINN list.
    * __Positive__: List of postive words in input string that were found in AFINN list.
    * __Negative__: List of negative words in input string that were found in AFINN list.

In this case, love has a value of 3, allergic has a value of -2, and the remaining tokens are neutral with a value of 0. Because the string has 9 tokens the resulting comparative score looks like:
`(3 + -2) / 9 = 0.111111111`

This approach leaves you with a mid-point of 0 and the upper and lower bounds are constrained to positive and negative 5 respectively (the same as each token! 😸). For example, let's imagine an incredibly "positive" string with 200 tokens and where each token has an AFINN score of 5. Our resulting comparative score would look like this:

```
(max positive score * number of tokens) / number of tokens
(5 * 200) / 200 = 5
```

### Tokenization
Tokenization works by splitting the lines of input string, then removing the special characters, and finally splitting it using spaces. This is used to get list of words in the string.

---

## Benchmarks
A primary motivation for designing `sentiment` was performance. As such, it includes a benchmark script within the test directory that compares it against the [Sentimental](https://github.com/thinkroth/Sentimental) module which provides a nearly equivalent interface and approach. Based on these benchmarks, running on a MacBook Pro with Node v6.9.1, `sentiment` is nearly twice as fast as alternative implementations:

```bash
sentiment (Latest) x 861,312 ops/sec ±0.87% (89 runs sampled)
Sentimental (1.0.1) x 451,066 ops/sec ±0.99% (92 runs sampled)
```

To run the benchmarks yourself:
```bash
npm run test:benchmark
```

---

## Validation
While the accuracy provided by AFINN is quite good considering it's computational performance (see above) there is always room for improvement. Therefore the `sentiment` module is open to accepting PRs which modify or amend the AFINN / Emoji datasets or implementation given that they improve accuracy and maintain similar performance characteristics. In order to establish this, we test the `sentiment` module against [three labelled datasets provided by UCI](https://archive.ics.uci.edu/ml/datasets/Sentiment+Labelled+Sentences).

To run the validation tests yourself:
```bash
npm run test:validate
```

### Rand Accuracy (AFINN Only)
```
Amazon:  0.70
IMDB:    0.76
Yelp:    0.67
```

### Rand Accuracy (AFINN + Additions)
```
Amazon:  0.72 (+2%)
IMDB:    0.76 (+0%)
Yelp:    0.69 (+2%)
```

---

## Testing
```bash
npm test
```

