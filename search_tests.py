from search import keyword_to_titles, title_to_info, search, article_length,key_by_author, filter_to_author, filter_out, articles_from_year
from search_tests_helper import get_print, print_basic, print_advanced, print_advanced_option
from wiki import article_metadata
from unittest.mock import patch
from unittest import TestCase, main

class TestSearch(TestCase):

    ##############
    # UNIT TESTS #
    ##############

    def test_example_unit_test(self):
        dummy_keyword_dict = {
            'cat': ['title1', 'title2', 'title3'],
            'dog': ['title3', 'title4']
        }
        expected_search_results = ['title3', 'title4']
        self.assertEqual(search('dog', dummy_keyword_dict), expected_search_results)
    
    def test_keyword_to_titles(self):
        dummy_metadata_1 = [['List of Canadian musicians', 'Jack Johnson', 1181623340, 21023, ['canadian', 'canada', 'lee', 'jazz', 'and', 'rock']]]
        expected_result_1 = {
            'canadian': ['List of Canadian musicians'],
            'canada': ['List of Canadian musicians'],
            'lee': ['List of Canadian musicians'],
            'jazz': ['List of Canadian musicians'],
            'and': ['List of Canadian musicians'],
            'rock': ['List of Canadian musicians']
        }
        dummy_metadata_2 = [['List of Canadian musicians', 'Jack Johnson', 1181623340, 21023, ['canadian', 'canada', 'lee', 'jazz', 'and', 'rock']], ['French pop music', 'Mack Johnson', 1172208041, 5569, ['french', 'pop', 'music', 'the', 'france', 'and', 'radio']], ['Edogawa, Tokyo', 'jack johnson', 1222607041, 4526, ['edogawa', 'the', 'with', 'and', 'koiwa', 'kasai']]]
        expected_result_2 = {
            'canadian': ['List of Canadian musicians'],
            'canada': ['List of Canadian musicians'],
            'lee': ['List of Canadian musicians'],
            'jazz': ['List of Canadian musicians'],
            'and': ['List of Canadian musicians', 'French pop music', 'Edogawa, Tokyo'],
            'rock': ['List of Canadian musicians'],
            'french': ['French pop music'],
            'pop': ['French pop music'],
            'music': ['French pop music'],
            'the': ['French pop music', 'Edogawa, Tokyo'],
            'france': ['French pop music'],
            'radio': ['French pop music'],
            'edogawa': ['Edogawa, Tokyo'],
            'with' : ['Edogawa, Tokyo'],
            'koiwa': ['Edogawa, Tokyo'],
            'kasai': ['Edogawa, Tokyo']
        }
        
        self.assertEqual(keyword_to_titles(dummy_metadata_1), expected_result_1)
        self.assertEqual(keyword_to_titles(dummy_metadata_2), expected_result_2)
        self.assertEqual(keyword_to_titles([]), {})
    
    def test_title_to_info(self):
        dummy_metadata_1 = [['List of Canadian musicians', 'Jack Johnson', 1181623340, 21023, ['canadian', 'canada', 'lee', 'jazz', 'and', 'rock']]]
        expected_result_1 = {'List of Canadian musicians': {'author': 'Jack Johnson', 'timestamp': 1181623340, 'length': 21023}}
        dummy_metadata_2 = [['List of Canadian musicians', 'Jack Johnson', 1181623340, 21023, ['canadian', 'canada', 'lee', 'jazz', 'and', 'rock']], ['French pop music', 'Mack Johnson', 1172208041, 5569, ['french', 'pop', 'music', 'the', 'france', 'and', 'radio']], ['Edogawa, Tokyo', 'jack johnson', 1222607041, 4526, ['edogawa', 'the', 'with', 'and', 'koiwa', 'kasai']]]
        expected_result_2 = {'List of Canadian musicians': {'author': 'Jack Johnson', 'timestamp': 1181623340, 'length': 21023}, 'French pop music': {'author': 'Mack Johnson', 'timestamp': 1172208041, 'length': 5569}, 'Edogawa, Tokyo': {'author': 'jack johnson', 'timestamp': 1222607041, 'length': 4526}}
        self.assertEqual(title_to_info(dummy_metadata_1), expected_result_1)
        self.assertEqual(title_to_info(dummy_metadata_2), expected_result_2)
        self.assertEqual(title_to_info([]), {})
    
    def test_search(self):
        dummy_key_title = {
            'canadian': ['List of Canadian musicians'],
            'canada': ['List of Canadian musicians'],
            'lee': ['List of Canadian musicians'],
            'jazz': ['List of Canadian musicians'],
            'and': ['List of Canadian musicians', 'French pop music', 'Edogawa, Tokyo'],
            'rock': ['List of Canadian musicians'],
            'french': ['French pop music'],
            'pop': ['French pop music'],
            'music': ['French pop music'],
            'the': ['French pop music', 'Edogawa, Tokyo'],
            'france': ['French pop music'],
            'radio': ['French pop music'],
            'edogawa': ['Edogawa, Tokyo'],
            'with' : ['Edogawa, Tokyo'],
            'koiwa': ['Edogawa, Tokyo'],
            'kasai': ['Edogawa, Tokyo']
        }
        keyword_1 = 'the'
        keyword_2 = 'france'
        keyword_3 = 'France'
        keyword_4 = 'soccer'

        self.assertEqual(search(keyword_1, dummy_key_title), ['French pop music', 'Edogawa, Tokyo'])
        self.assertEqual(search(keyword_2, dummy_key_title), ['French pop music'])
        self.assertEqual(search(keyword_3, dummy_key_title), [])
        self.assertEqual(search(keyword_4, dummy_key_title), [])
        self.assertEqual(search(keyword_1, {}), [])
        self.assertEqual(search('', dummy_key_title), [])
        self.assertEqual(search('', {}), [])
    
    def test_article_length(self):
       dummy_title_info  = {'List of Canadian musicians': {'author': 'Jack Johnson', 'timestamp': 1181623340, 'length': 21023}, 'French pop music': {'author': 'Mack Johnson', 'timestamp': 1172208041, 'length': 5569}, 'Edogawa, Tokyo': {'author': 'jack johnson', 'timestamp': 1222607041, 'length': 4526}}
       dummy_article_title_1 = ['List of Canadian musicians', 'French pop music', 'Edogawa, Tokyo']
       dummy_article_title_2 = ['French pop music']
       dummy_article_title_3 = ['Black dog (ghost)']

       self.assertEqual(article_length(30000, dummy_article_title_1, dummy_title_info), dummy_article_title_1)
       self.assertEqual(article_length(20000, dummy_article_title_1, dummy_title_info), ['French pop music', 'Edogawa, Tokyo'])
       self.assertEqual(article_length(0, dummy_article_title_1, dummy_title_info), [])
       self.assertEqual(article_length(30000, [], dummy_title_info), [])
       self.assertEqual(article_length(30000, dummy_article_title_1, {}), [])
       self.assertEqual(article_length(30000, [], {}), [])
       self.assertEqual(article_length(-2, dummy_article_title_1, dummy_title_info), [])
       self.assertEqual(article_length(30000, dummy_article_title_2, dummy_title_info), dummy_article_title_2)
       self.assertEqual(article_length(30000, dummy_article_title_3, dummy_title_info), [])

    def test_key_by_author(self):
        dummy_title_info  = {'List of Canadian musicians': {'author': 'Jack Johnson', 'timestamp': 1181623340, 'length': 21023}, 'French pop music': {'author': 'Mack Johnson', 'timestamp': 1172208041, 'length': 5569}, 'Edogawa, Tokyo': {'author': 'jack johnson', 'timestamp': 1222607041, 'length': 4526}, 'The spastic song': {'author': 'Jack Johnson', 'timestamp': 2181651230, 'length': 21023}}
        dummy_article_title_1 = ['List of Canadian musicians', 'French pop music', 'Edogawa, Tokyo', 'The spastic song']
        expected_result_1 = {
            'Jack Johnson': ['List of Canadian musicians', 'The spastic song'],
            'Mack Johnson': ['French pop music'],
            'jack johnson': ['Edogawa, Tokyo']
        }
        dummy_article_title_2 = ['List of Canadian musicians', 'French pop music']
        expected_result_2 = {
            'Jack Johnson': ['List of Canadian musicians'],
            'Mack Johnson': ['French pop music']
        }

        self.assertEqual(key_by_author(dummy_article_title_1, dummy_title_info), expected_result_1)
        self.assertEqual(key_by_author([], dummy_title_info), {})
        self.assertEqual(key_by_author([], {}), {})
        self.assertEqual(key_by_author(dummy_article_title_1, {}), {})
        self.assertEqual(key_by_author(dummy_article_title_2, dummy_title_info), expected_result_2)
    
    def test_filter_to_author(self):
        dummy_title_info  = {'List of Canadian musicians': {'author': 'Jack Johnson', 'timestamp': 1181623340, 'length': 21023}, 'French pop music': {'author': 'Mack Johnson', 'timestamp': 1172208041, 'length': 5569}, 'Edogawa, Tokyo': {'author': 'jack johnson', 'timestamp': 1222607041, 'length': 4526}, 'The spastic song': {'author': 'Jack Johnson', 'timestamp': 2181651230, 'length': 21023}}
        article_list = ['List of Canadian musicians', 'French pop music', 'Edogawa, Tokyo', 'The spastic song']

        self.assertEqual(filter_to_author('Jack Johnson', article_list, dummy_title_info), ['List of Canadian musicians', 'The spastic song'])
        self.assertEqual(filter_to_author('Mack Johnson', article_list, dummy_title_info), ['French pop music'])
        self.assertEqual(filter_to_author('Sajan King', article_list, dummy_title_info), [])
        self.assertEqual(filter_to_author('Mack Johnson', article_list, {}), [])
        self.assertEqual(filter_to_author('Mack Johnson', [], dummy_title_info), [])
        self.assertEqual(filter_to_author('', article_list, dummy_title_info), [])
        self.assertEqual(filter_to_author('', [], {}), [])

    def test_filter_out(self):
        dummy_key_title = {
            'canadian': ['List of Canadian musicians'],
            'canada': ['List of Canadian musicians'],
            'lee': ['List of Canadian musicians'],
            'jazz': ['List of Canadian musicians'],
            'and': ['List of Canadian musicians', 'French pop music', 'Edogawa, Tokyo'],
            'rock': ['List of Canadian musicians'],
            'french': ['French pop music'],
            'pop': ['French pop music'],
            'music': ['French pop music'],
            'the': ['French pop music', 'Edogawa, Tokyo'],
            'france': ['French pop music'],
            'radio': ['French pop music'],
            'edogawa': ['Edogawa, Tokyo'],
            'with' : ['Edogawa, Tokyo'],
            'koiwa': ['Edogawa, Tokyo'],
            'kasai': ['Edogawa, Tokyo']
        }
        article_list = ['List of Canadian musicians', 'French pop music', 'Edogawa, Tokyo']

        self.assertEqual(filter_out('kasai', article_list, dummy_key_title), ['List of Canadian musicians', 'French pop music'])
        self.assertEqual(filter_out('and', article_list, dummy_key_title), [])
        self.assertEqual(filter_out('and', [], dummy_key_title), [])
        self.assertEqual(filter_out('', article_list, dummy_key_title), article_list)
        self.assertEqual(filter_out('destroy', article_list, dummy_key_title), article_list)
        self.assertEqual(filter_out('', [], dummy_key_title), [])
        self.assertEqual(filter_out('', [], {}), [])
        self.assertEqual(filter_out('the', article_list, dummy_key_title), ['List of Canadian musicians'])
        self.assertEqual(filter_out('the', article_list, {}), [])
    
    def test_articles_from_year(self):
        dummy_title_info  = {'List of Canadian musicians': {'author': 'Jack Johnson', 'timestamp': 1181623340, 'length': 21023}, 'French pop music': {'author': 'Mack Johnson', 'timestamp': 1172208041, 'length': 5569}, 'Edogawa, Tokyo': {'author': 'jack johnson', 'timestamp': 1222607041, 'length': 4526}, 'The spastic song': {'author': 'Jack Johnson', 'timestamp': 1609333200, 'length': 21023}}
        article_list = ['List of Canadian musicians', 'French pop music', 'Edogawa, Tokyo', 'The spastic song']

        self.assertEqual(articles_from_year(2008, article_list, dummy_title_info), ['Edogawa, Tokyo'])
        self.assertEqual(articles_from_year(2009, article_list, dummy_title_info), [])
        self.assertEqual(articles_from_year(2008, article_list, {}), [])
        self.assertEqual(articles_from_year(2008, [], dummy_title_info), [])
        self.assertEqual(articles_from_year(2008, [], {}), [])
        self.assertEqual(articles_from_year(2020, article_list, dummy_title_info), ['The spastic song'])
        self.assertEqual(articles_from_year(3000, article_list, dummy_title_info), [])

    #####################
    # INTEGRATION TESTS #
    #####################

    @patch('builtins.input')
    def test_example_integration_test(self, input_mock):
        keyword = 'soccer'
        advanced_option = 5
        advanced_response = 2009

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: ['Spain national beach soccer team', 'Steven Cohen (soccer)']\n"

        self.assertEqual(output, expected)
    
    @patch('builtins.input')
    def test_article_length_integration_test(self, input_mock):
        keyword = 'soccer'
        advanced_option = 1
        advanced_response = 25000

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: ['Spain national beach soccer team', 'Will Johnson (soccer)', 'Steven Cohen (soccer)']\n"

        self.assertEqual(output, expected)
    
    @patch('builtins.input')
    def test_key_by_author_integration_test(self, input_mock):
        keyword = 'soccer'
        advanced_option = 2

        output = get_print(input_mock, [keyword, advanced_option])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + "\n\nHere are your articles: {'jack johnson': ['Spain national beach soccer team'], 'Burna Boy': ['Will Johnson (soccer)'], 'Mack Johnson': ['Steven Cohen (soccer)']}\n"

        self.assertEqual(output, expected)
    
    @patch('builtins.input')
    def test_filter_to_author_integration_test(self, input_mock):
        keyword = 'dog'
        advanced_option = 3
        advanced_response = 'Mr Jake'

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: ['Dalmatian (dog)', 'Sun dog']\n"

        self.assertEqual(output, expected)
    
    @patch('builtins.input')
    def test_filter_out_keyword_integration_test(self, input_mock):
        keyword = 'soccer'
        advanced_option = 4
        advanced_response = 'dog'

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: ['Spain national beach soccer team', 'Will Johnson (soccer)', 'Steven Cohen (soccer)']\n"

        self.assertEqual(output, expected)
    
    @patch('builtins.input')
    def test_filter_out_keyword_integration_test(self, input_mock):
        keyword = 'soccer'
        advanced_option = 5
        advanced_response = 2008

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: ['Will Johnson (soccer)']\n"

        self.assertEqual(output, expected)


# Write tests above this line. Do not remove.
if __name__ == "__main__":
    main()