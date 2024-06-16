# search-engine
A search engine takes a given search phrase or word and finds pages on the internet that are relevant, ranks the pages, and then displays the pages in the order of ranking. In this program, we will search through the 2D list of metadata but before performing our searches, we will preprocess the data into dictionaries.

All article metadata can be fetched by calling the wiki.article_metadata(). It returns a 2D list where each individual "row" represents a single article. Each article is represented as a list with the following information provided in this exact order:

  1. Article title (string)

  2. Author name (string)

  3. Timestamp of when the article was published (int). The timestamp is stored as the # of seconds since January 1st, 1970 (also known as Unix/Epoch Time)

  4. The number of characters in the article (int)

  5. A list of keywords that are related to the article content (list of strings)

To demonstrate, here is a potential example row in the 2D list:

['Spongebob - the legacy', 'Mr Jake', 1172208041, 5569, ['Spongebob', 'cartoon', 'pineapple', 'tv', 'sponge', 'nickelodean', 'legacy']]
