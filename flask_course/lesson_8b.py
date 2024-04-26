companies = [
  {
    'id': 4,
    # другие элементы словаря
  },
  {
    'id': 2,
    # другие элементы словаря
  },
  {
    'id': 8,
    # другие элементы словаря
  },
]


def companies_page(id):
    res = list(filter(lambda x: x.get('id') == id, companies))
    if res:
        return res[0]
    return 'Oops', 404


print(companies_page(8))
