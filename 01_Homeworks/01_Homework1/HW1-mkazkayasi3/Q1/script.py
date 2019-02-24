"""Allowed packages"""
import http.client
import json
import time
import sys
import csv
# import collections


def get_350_drama(api_key):
    """This module gets 350 drama movies in decreasing popularity order"""

    conn = http.client.HTTPSConnection("api.themoviedb.org")

    j = 0
    movie_ids = []
    id_name = []
    while True:
        j += 1
        now = time.time()

        conn.request("GET", "/3/discover/movie?page="+str(j)+"&include_video=false&sort_by="\
        "popularity.desc&primary_release_date.gte=2004&with_genres=18&api_key="+api_key, "{}")

        res = conn.getresponse()
        data = res.read()

        # read as JSON
        data_load = json.loads(data)

        for i in range(20):
            count = (j-1)*20 + i + 1
            if count > 350:
                break
            # print("{:<5} {}".format(str(count), (data_load["results"][i]["release_date"])))

            # save movie_id and name of movie in variables
            movie_ids.append(data_load["results"][i]["id"])
            the_id = data_load["results"][i]["id"]
            the_name = data_load["results"][i]["title"]
            id_name.append((the_id, the_name))

        time_long = time.time() - now
        if time_long < 10.0/40:
            # print(time_long)
            time.sleep(10.0/40 - time_long)

        if count > 350:
            break


    # send them to CSV file
    with open('movie_ID_name.csv', 'w', newline='') as csvfile:
        csv.writer(csvfile).writerows(id_name)
    csvfile.close()

    # print(data.decode("utf-8"))
    # print(id_name)
    return movie_ids

def get_5_similar(movie_ids, api_key):
    """This module brings 5 similar movies and produces list of list of 6 movies
    (first one and 5 similar)"""
    list_of_sixes = []
    time.sleep(1)
    conn = http.client.HTTPSConnection("api.themoviedb.org")
    for mov_id in movie_ids:

        now = time.time()
        # use similar movie api and put it in
        conn.request("GET", "/3/movie/"+str(mov_id)+"/similar?page=1&language="\
        "en-US&api_key="+api_key, "{}")
        res = conn.getresponse()
        data = res.read()
        data_load = json.loads(data)

        # line_new = '{:<12}  {:>12}  {:>12}'.format(word[0], word[1], word[2])
        # print("{:<8}  {}".format(mov_id, "CAYIR CAYIR"))
        # print(mov_id, "CAYIR CAYIR")
        # get the 5 similar movie from data_load
        if "results" not in data_load:
            print(data_load)
        list_six = [mov_id]
        for k in range(min(5, len(data_load["results"]))):
            list_six.append(data_load["results"][k]["id"])
        list_of_sixes.append(list_six)

        if time.time() - now < 10.0/40:
            # print(time_long)
            time.sleep(10.0/40 - (time.time() - now))

    # remove duplicates
    the_return_list = []
    for six in list_of_sixes:
        if len(six) > 1:
            for j in range(1, len(six)):
                if (six[0], six[j]) not in the_return_list \
                and (six[j], six[0]) not in the_return_list:
                    the_return_list.append((six[0], six[j]))

    # print(the_return_list)
    # send them to CSV file
    with open('movie_ID_sim_movie_ID.csv', 'w', newline='') as csvfile:
        csv.writer(csvfile).writerows(the_return_list)
    csvfile.close()

def main():
    """main function to call others"""
    # get the api_key or use mine
    # if len(sys.argv) > 1:
    #     api_key = sys.argv[1]
    # else:
    #     api_key = "xxx"

    api_key = sys.argv[1]
    # print(api_key)


    movie_ids = get_350_drama(api_key)
    get_5_similar(movie_ids, api_key)
    # print(list_of_sixes)

main()
