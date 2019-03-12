import numpy as np
import os, math
import matplotlib.pyplot as plt
from pydelicious import get_popular, get_userposts, get_urlposts

critics={
    'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5, 
                  'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5, 
                  'The Night Listener': 3.0},
    'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 
                     'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0, 
                     'You, Me and Dupree': 3.5}, 
    'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
                         'Superman Returns': 3.5, 'The Night Listener': 4.0},
    'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
                     'The Night Listener': 4.5, 'Superman Returns': 4.0, 
                     'You, Me and Dupree': 2.5},
    'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 
                     'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
                     'You, Me and Dupree': 2.0}, 
    'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                      'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
    'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}
}

def draw_movie_plot(pref, movie1, movie2):
    name_score = {}
    for name, movies in pref.items():
        statistic = [-1, -1]
        for movie_name, scope in movies.items():
            if movie1 in movie_name:
                statistic[0] = scope
            if movie2 in movie_name:
                statistic[1] = scope
                
        if -1 not in statistic:
            name_score[name] = statistic
    
    scores = []
    for name, score in name_score.items():
        scores.append(score)
    
    scores = np.array(scores)
    max_lim = np.max(scores)+1
    plt.xlim((0, max_lim))
    plt.ylim((0, max_lim))
    plt.scatter(scores[:,0], scores[:,1])
    plt.show()

def draw_people_plot(pref, person1, person2):
    critic1 = pref[person1]
    critic2 = pref[person2]
    common_obs = [[critic1[item],critic2[item]] for item in critic1.keys() if item in critic2.keys()]
    scores = np.array(common_obs)
    max_lim = np.max(scores)+1
    plt.xlim((0, max_lim))
    plt.ylim((0, max_lim))
    plt.scatter(scores[:,0], scores[:,1])
    plt.show()
    
def Euclidean_distance(pref, person1, person2):
    critic1 = pref[person1]
    critic2 = pref[person2]
    common_obs = [[critic1[item],critic2[item]] for item in critic1.keys() if item in critic2.keys()]
    if len(common_obs) == 0:
        return 0
    dis = sum([(it[0]-it[1])**2 for it in common_obs])
    # print(1/(1+math.sqrt(dis)))
    return 1/(1+math.sqrt(dis))
    
def Pearson_distance(pref, person1, person2):
    critic1 = pref[person1]
    critic2 = pref[person2]
    
    sim = {}
    for movie_name in critic1:
        if movie_name in critic2:
            sim[movie_name] = 1
    
    if len(sim) == 0:
        return 0
    # calculate sum of the pref
    critic1_sum = sum([critic1[item] for item in sim])
    critic2_sum = sum([critic2[item] for item in sim])
    # calculate square sum of the pref
    critic1_sum2 = sum([critic1[item]**2 for item in sim])
    critic2_sum2 = sum([critic2[item]**2 for item in sim])
    # calculate cross product
    critic12_sum = sum([critic1[item]*critic2[item] for item in sim])
    
    # pearson correlation score
    n = len(sim)
    num = critic12_sum - (critic1_sum*critic2_sum)/n
    den = math.sqrt((critic1_sum2-(critic1_sum**2)/n)*(critic2_sum2-(critic2_sum**2)/n))
    if den == 0:
        return 1
    
    # print(num/den)
    return num/den
    
def top_matches(pref, person, n = 5, sim_function = Pearson_distance):
    sims = list()
    for person_name in pref:
        if person_name != person:
            sims.append((sim_function(pref, person, person_name), person_name))
    # print(sims)
    sims = sorted(sims, key=lambda x: x[0], reverse=True)
    return sims[:n]
    
def get_recommandations(pref, person, sim_function = Pearson_distance):
    new_movies = {}
    for person_name, movies in pref.items():
        if person_name == person:
            continue
        else:
            sim = sim_function(pref, person, person_name)
            if sim <= 0:
                continue
            for movie_name in movies:
                if movie_name not in new_movies:
                    new_movies[movie_name] = [sim, sim*movies[movie_name]]
                else:
                    new_movies[movie_name][0] += sim
                    new_movies[movie_name][1] += sim*movies[movie_name]

    old_movies = pref[person].keys()
    recommands = [(movie_name, critic[1]/(critic[0]+0.00001)) for movie_name, critic in new_movies.items() if movie_name not in old_movies ]
    recommands = sorted(recommands, key=lambda x: x[1], reverse=True)
    return recommands

def transform_items(pref):
    result = {}
    for person in pref:
        for movie in pref[person]:
            result.setdefault(movie, {})
            result[movie][person] = pref[person][movie]
    return result

def calculate_similar_items(pref, n=10):
    result = {}

    item_pref = transform_items(pref)
    c=0
    for item in item_pref:
        c+=1
        if c%100==0:
            print("%d / %d" % (c, len(item_pref)))
        result[item] = top_matches(item_pref, item, n=n, sim_function=Euclidean_distance)
    return result

def get_recommand_item(pref, itemMatches, item):
    old_item = pref[item]
    result = {}

    for item, score in old_item.items():
        for score_elem in itemMatches[item]:
            item2 = score_elem[1]
            alpha = score_elem[0]
            if item2 in old_item:
                continue
            # item2 indicate the item will be recommand
            result.setdefault(item2, [0, 0])
            result[item2][0] += score*alpha
            result[item2][1] += alpha

    recommands = [(item, it[0]/it[1]) for item, it in result.items()]
    recommands = sorted(recommands, key=lambda x: x[1], reverse=True)
    return recommands

def load_movielens(path):
    movies_id = {}
    movies_id_path = os.path.join(path, 'movies.csv')
    with open(movies_id_path, 'r') as fp:
        for line in fp.readlines():
            line = line.strip()
            if 'movieId' in line:
                continue
            elems = line.split(',')
            movies_id[elems[0]] = elems[1]
    critic = {}
    movies_rate_path = os.path.join(path, 'ratings.csv')
    with open(movies_rate_path, 'r') as fp:
        for line in fp.readlines():
            line = line.strip()
            if 'movieId' in line:
                continue
            elems = line.split(',')
            critic.setdefault(elems[0], {})
            critic[elems[0]][movies_id[elems[1]]] = float(elems[2])
    return critic

if __name__=='__main__':
#     movie1 = 'Snakes'; movie2 = 'Dupree'
#     draw_plot('Dupree', 'Snakes')
    # print(Euclidean_distance(critics, 'Gene Seymour', 'Lisa Rose'))
#     draw_people_plot('Lisa Rose', 'Toby')
#     draw_people_plot('Jack Matthews', 'Lisa Rose')
#     Pearson_distance('Jack Matthews', 'Lisa Rose')
#     tops = top_matches('Toby', 3)
#     print(get_recommandations('Toby'))
#     trans_pref = transform_items(critics)
#     tops = top_matches(trans_pref, person='Superman Returns')
#     print(tops)
    # get_popular(tag='programming')
    # score = calculate_similar_items(critics)
    # recomd = get_recommand_item(critics, score, 'Toby')
    # print(recomd)

    file_path = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.join(file_path, 'ml-latest-small')
    movie_lens = load_movielens(data_path)
    transf_movie_lens = transform_items(movie_lens)
    sim_items = calculate_similar_items(transf_movie_lens, n=50)
    res = get_recommand_item(movie_lens, sim_items, '87')[:30]
    print(res)