import math

def make_pagination_range( page_range,qty_pages,current_page):
    _middle_page = math.ceil(qty_pages/2)
    _stop_point = len(page_range) - _middle_page
    _total_pages = len(page_range)
    pagination = None
    start_range = 0
    stop_range = 0
    #aki é pra caso a pagina atual esteja antes do primeiro meio do range ex:[1, 2, [3], 4, 5]
    if current_page <= _middle_page:
        pagination = page_range[0:qty_pages]
    #e aki é pra caso esteja no ultimo meio de range
    elif current_page > _stop_point:
        
        pagination = page_range[-qty_pages:]
    
    #aki eu faço os calculos para mostrar o range das paginas
    if current_page > _middle_page and current_page <= _stop_point:
        '''
        aki começa a mexer o range, start_rage sempre sendo 1 a mais 
        que o range anterior

        ex:
             1   2   3  4
            [2, [3], 4, 5] -> currente_page = 3; md = 2; resultado => 3-2=1;

             2   3   4  5
            [3, [4], 5, 6] -> currente_page = 4; md = 2; resultado => 4-2=2;
            
             3   4   5  6
            [4, [5], 6, 7] -> currente_page = 5; md = 2; resultado => 5-2=3;
            
             4   5   6  7
            [5, [6], 7, 8] -> currente_page = 6; md = 2; resultado => 6-2=4;

        '''
        start_range = current_page - _middle_page


        '''
        aki eu simplesmente somo a tamanho do range solicitado ao num inicial
        do range atual
        ex:
             1  2  3  4
            [2, 3, 4, 5] => start_range = 1;qty_page = 4; stop_range = 1 + 4

             1  2  3  4  5
            [2, 3, 4, 5, 6] => start_range = 1;qty_page = 5; stop_range = 1 + 5

        '''
        stop_range = start_range + qty_pages

        pagination = page_range[start_range:stop_range]

    return {
        'pagination': pagination,
        'page_range': page_range,
        'qty_pages': qty_pages,
        'current_page': current_page,
        'total_pages': _total_pages,
        'start_range': start_range,
        'stop_range': stop_range,
        'first_page_out_of_range': current_page > _middle_page,
        'last_page_out_of_range': stop_range < _total_pages,    
    }



if __name__ == '__main__':
    # for i in range(1, 21):
    #     a: dict = make_pagination_range(list(range(1, 21)),4, int(i)) #type: ignore
    #     for num in a['pagination']:
    #         if num == i:
    #             print(f'[{num}]', end=' ')
    #         else:
    #             print(num, end=' ')
    #     print()
    #         # print(num)

    a = make_pagination_range(list(range(1, 21)),4, 0)['pagination']
    print(a)