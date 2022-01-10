from MovieRecommender.views import *


def read_movie_data():
    df = p.read_csv('E:/PythonProjects/data/movies_metadata.csv')
    column_names = ['id', 'title', 'overview', 'budget', 'original_language', 'popularity', 'poster_path',
                    'release_date', 'video'
        , 'vote_average', 'vote_count']

    data = df[column_names]

    genres_id = df['genres'].fillna('[]').apply(literal_eval).apply(
        lambda x: [i['id'] for i in x] if isinstance(x, list) else [])

    companies_id = df['production_companies'].fillna('[]').apply(literal_eval).apply(
        lambda x: [i['id'] for i in x] if isinstance(x, list) else [])

    for x in range(40000, len(data)):
        print(x)
        for x in range(0, len(data)):
            movie = Movie.objects.filter(movie_id=data.iloc[x]['id'])
            for y in range(0, len(genres_id[x])):
                grn = Genre.objects.get(genre_id=genres_id[x][y])
                for z in range(0, len(movie)):
                    movie[z].genres.add(grn)

            for y in range(0, len(companies_id[x])):
                crn = Company.objects.get(company_id=companies_id[x][y])
                for z in range(0, len(movie)):
                    movie[z].production_companies.add(crn)
        print(movie)


def get_unique_values(list1):
    unique_list = []
    for x in list1:
        if x not in unique_list:
            unique_list.append(x)

    return unique_list


def fill_genres_companies_data():
    df = p.read_csv('E:/PythonProjects/data/movies_metadata.csv')

    companies_names = df['production_companies'].fillna('[]').apply(literal_eval).apply(
        lambda x: [i['name'] for i in x] if isinstance(x, list) else [])
    companies_id = df['production_companies'].fillna('[]').apply(literal_eval).apply(
        lambda x: [i['id'] for i in x] if isinstance(x, list) else [])

    names = []
    i = 0
    j = 0
    for x in range(0, len(companies_names)):
        for y in range(0, len(companies_names[x])):
            names.append(companies_names[x][y])

    names = get_unique_values(names)

    ids = []
    i = 0
    j = 0
    for x in range(0, len(companies_id)):
        for y in range(0, len(companies_id[x])):
            ids.append(companies_id[x][y])

    ids = get_unique_values(ids)

    print(names)
    print(ids)

    for x in range(0, len(names)):
        Company.objects.create(company_id=ids[x], name=names[x])

    genres = df['production_companies']
