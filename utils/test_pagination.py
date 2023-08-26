from unittest import TestCase
from utils.pagination_func import make_pagination_range

class PaginationTest(TestCase):
    def test_make_pagination_range_returns_a_pagination_range(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1
        )['pagination'] 

        self.assertEqual([1, 2, 3, 4], pagination)
    
    def test_first_range_is_static_if_current_page_is_less_than_middle_page(self):
        
        #current_page = 1; expected_range = [1, 2, 3, 4]
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1
        )['pagination']

        self.assertEqual([1, 2, 3, 4], pagination)


        #current_page = 2; expected_range = [1, 2, 3, 4]
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=2,
        )['pagination'] 

        self.assertEqual([1, 2, 3, 4], pagination)


        #current_page = 3; expected_range = [2, 3, 4, 5]
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=3,
        )['pagination'] 

        self.assertEqual([2, 3, 4, 5], pagination)


        #current_page = 4; expected_range = [3, 4, 5, 6]
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=4,
        )['pagination'] 

        self.assertEqual([3, 4, 5, 6], pagination)

    def test_make_sure_middle_ranges_are_correct(self):
        
        #current_page = 10; expected_range = [9, 10, 11, 12]
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=10,
        )['pagination'] 

        self.assertEqual([9, 10, 11, 12], pagination)


        #current_page = 12; expected_range = [11, 12, 13, 14]
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=12,
        )['pagination'] 

        self.assertEqual([11, 12, 13, 14], pagination)

    def test_pagination_range_stay_static_if_its_in_the_final_range(self):
        #current_page = 18; expected_range = [17, 18, 19, 20]
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=18,
        )['pagination'] 

        self.assertEqual([17, 18, 19, 20], pagination)

        #current_page = 19; expected_range = [17, 18, 19, 20]
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=19,
        )['pagination'] 

        self.assertEqual([17, 18, 19, 20], pagination)

        #current_page = 20; expected_range = [17, 18, 19, 20]
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=22,
        )['pagination'] 

        self.assertEqual([17, 18, 19, 20], pagination)
