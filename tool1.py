import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import os
from sklearn.metrics.pairwise import cosine_similarity

def read_file(file_path):
    with open(file_path,'r', encoding='latin-1') as jb:
        content=jb.read()
    return content

def read_all_resume(folder_path):
  file_content={}
  for filename in os.listdir(folder_path):
    file_path=os.path.join(folder_path,filename)
    file_content[filename]=read_file(file_path)
  return file_content

def filter_cv_keyword(cv_ks):
    #removing some unnecessary characters from words
    cv_ks=[keyword.translate(str.maketrans('','',',():;')) for keyword in cv_ks]
    #removing words which are useless for critical keyword comparision
    useless_substring=['www.','/','\\','.com','---']
    cv_ks=[keyword for keyword in cv_ks if not any(substring in keyword for substring in useless_substring)]
    #removing empty keywords
    useless_keywords=['the','a','','on','it','and','using','by','an','for','to','from','of','in','this']
    cv_ks=[keyword for keyword in cv_ks if keyword not in useless_keywords]
    return cv_ks

def find_similarity(jb_content,cv_content,critical_keyword):
    vectorizer=TfidfVectorizer(stop_words='english')
    tfidf_matrix=vectorizer.fit_transform([cv_content,jb_content])
    similarity_matrix=cosine_similarity(tfidf_matrix[0],tfidf_matrix[1])
    #critical keyword
    critical_k=[keyword.strip().lower() for keyword in critical_keyword.split(',')]
    #cv content
    cv_k=filter_cv_keyword([keyword.strip().lower() for keyword in cv_content.split(' ')])
    n_of_keyword_match=sum(1 for key in critical_k if key in cv_k)
    keyword_score=n_of_keyword_match/len(critical_k)
    score=int((similarity_matrix[0][0]+keyword_score*2)/3*10)
    return score

def rate_all(resume_group_path,jb_content_path,critical_keyword_path,rating_saving_path):
    resume_group=read_all_resume(resume_group_path)
    jb_content=read_file(jb_content_path)
    critical_keyword=read_file(critical_keyword_path)
    name_list=[]
    score_list=[]
    rating={}
    for key in resume_group:
        score=find_similarity(jb_content,resume_group[key],critical_keyword)
        name_list.append(key[:-4].replace("_"," ").strip())
        score_list.append(score)
    rating['name']=name_list
    rating['rating']=score_list
    rating_df=pd.DataFrame(rating)
    if not os.path.exists(rating_saving_path):
        os.makedirs(rating_saving_path)
    rating_df.to_csv(os.path.join(rating_saving_path,'rating.csv'),index=False)
    rating_dict={}
    for i in range(0,len(name_list)):
        rating_dict[name_list[i]]=score_list[i]
    print(rating_df)
    return rating_dict
        
if __name__=='__main__':
    print('Example:\n')
    print('Enter resumes folder path: resume/resume_list')
    print('Enter job description file path: resume/job_description.txt')
    print('Enter critical keyword file path: resume/critical_keyword.txt')
    print('Enter the file path to save rating: resume')
    print('\nNow Enter your corresponding path\n')
    #resume_group_path=input('Enter resume folder path: ')
    #jb_content_path=input('Enter job description file path: ')
    #critical_keyword_path=('Enter critical keyword file path: ')
    #rating_saving_path=('Enter the file path to save rating:')
    resume_group_path='resume/resume_list'
    jb_content_path='resume/job_description.txt'
    critical_keyword_path='resume/critical_keyword.txt'
    rating_saving_path='rating'
    rate_all(resume_group_path,jb_content_path,critical_keyword_path,rating_saving_path)