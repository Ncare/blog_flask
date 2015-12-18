


def generate_page(sumItem, perPage, currentPage=1):

    sumPage = int(sumItem/perPage)
    if sumItem%perPage != 0:
        sumPage += 1

    has_prv = False
    has_next = False

    if currentPage < sumPage:
        has_next = True

    if currentPage > 1:
        has_prv = True

    return {
        'sumPage':sumPage,
        'currentPage':currentPage,
        'has_prv':has_prv,
        'has_next':has_next
    }
