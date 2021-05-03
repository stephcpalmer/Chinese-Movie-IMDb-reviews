#clean IMDb files
import re


Chinese_titles_id_regex = re.compile(r'(tt\d{7}).+\tCN\t',re.X) #captures id if the title is from China
Id_regex = re.compile(r'(tt\d{7})')

#tconst	titleType	primaryTitle	originalTitle	isAdult	startYear	endYear	runtimeMinutes	genres  ###Header from Title_basics.txt
Basics_info_regex = re.compile(r'tt\d{7}\tmovie\t([^\t]+)\t([^\t]+)\t\d\t([^\t]+)\t[^\t]+\t[^\t]+\t([^\t]+)\n')

#tconst	averageRating	numVotes
Ratings_info_regex = re.compile(r'tt\d{7}\t(\d\.\d)\t(\d+)\n')

Chinese_titles_dict = {}

with open('Title_akas.txt','r',encoding='utf8') as data_file:
    while True:
        line = data_file.readline() #reading line by line as loading in the whole file under with open.. too expensive on memory
        if line == '':
            break 
        Check_is_chinese = Chinese_titles_id_regex.search(line)
        if Check_is_chinese is not None:
            for i in range(1,5):
                if Check_is_chinese:
                    Chinese_id = Check_is_chinese.group(1)
                    Chinese_titles_dict[Chinese_id] = None  #kept as dictionary bc don't want multiples

print("Done parsing for Chinese movies")

Chinese_movies = Chinese_titles_dict.keys()
Chinese_movies_dict = {}

with open('Title_basics.txt','r',encoding='utf8') as data_file:
    while True:
        line = data_file.readline()
        if line == '':
            break
        Id = Id_regex.search(line)
        if Id is not None:
            if Id.group(1) is not None:
                Id = Id.group(1)
                if Id in Chinese_movies:    
                    Basic_info = Basics_info_regex.search(line)
                    if Basic_info:
                        Genres = re.sub(',','&',Basic_info.group(4))
                        Basic_info = [Basic_info.group(1),Basic_info.group(2),Basic_info.group(3),Genres]
                        Chinese_movies_dict[Id]= Basic_info

print("Done writing Chinese movie info")

Chinese_movies = Chinese_movies_dict.keys()

with open('Title_ratings.txt','r',encoding='utf8') as data_file:
    while True:
        line = data_file.readline()
        if line == '':
            break
        Id = Id_regex.search(line)
        if Id is not None:
            if Id.group(1) is not None:
                Id = Id.group(1)
                if Id in Chinese_movies:
                    Ratings_info = Ratings_info_regex.search(line)
                    if Ratings_info:
                        Chinese_movies_dict[Id].append(Ratings_info.group(1))
                        Chinese_movies_dict[Id].append(Ratings_info.group(2))
                        
print("Done rating Chinese movies")

Temp_dict = Chinese_movies_dict.copy()

for key,value in Chinese_movies_dict.items():
    if len(value)<=4:
        Temp_dict.pop(key)

Chinese_movies_dict = Temp_dict

Chinese_movies_dict_str = str(Chinese_movies_dict)
Pretty_dict_str = Chinese_movies_dict_str.replace("{",'').replace("}",'').replace('"','').replace("'",'').replace(': [',',').replace('], ','\n').replace('\\N','N/A').replace('\\','').replace(']','')

with open('Chinese_movies.txt','w',encoding = 'utf8') as wf:
    wf.write("tconst\tprimaryTitle\toriginalTitle\tstartYear\tgenres\taverageRating\tnumVotes\n")
    wf.write(Pretty_dict_str)
print("Done!")
