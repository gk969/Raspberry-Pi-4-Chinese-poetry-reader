import os
import codecs

POETRY_DELI='----------------------------------'

POETRY_FILES = ('school.txt', 'tang300.txt', 'song300.txt')
poetry_list=[]

def read_poetry_dir():
    for file in POETRY_FILES:
        with codecs.open(os.path.join('poetry', file), "r", 'utf-8') as infile:
            poetries=infile.read()
            for poetry in poetries.split(POETRY_DELI):
                poetry_list.append(poetry)
                
def gtts_speak(str):
    os.system('printf "\\033c"')
    print(str)
    str=str.replace('\n', '。')
    cmd='gtts-cli -l zh-tw "%s" | mpg123 - > /dev/null 2>&1' % str
    os.popen(cmd).readlines()
    
read_cnt=0
READ_CNT_MAX=3

def read_poetry():
    if len(poetry_list)==0:
        read_poetry_dir()
    
    i=0;
    try:
        with open('idx.txt', 'rt') as index_file:
            i=int(index_file.read())
    except Exception as e:
        str=e
        
    gtts_speak(poetry_list[i])
    
    global read_cnt
    read_cnt+=1
    if read_cnt>=READ_CNT_MAX:
        read_cnt=0
        i+=1
        with open('idx.txt', 'wt') as index_file:
            print("%d" % i, file=index_file)

    