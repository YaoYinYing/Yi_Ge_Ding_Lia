import json
import random
import re

idiom_file = "./chinese-xinhua-master/data/idiom.json"
replace_char_dict_extract = {"āáǎà": 'a', "ōóǒò": 'o', "ēéěèê": 'e', "īíǐì": 'i', "ūúǔù": 'u', "ǖǘǚǜ": 'v'}
replace_char_dict_bootstrap = {'a': "āáǎà", 'o': "ōóǒò", 'e': "ēéěèê", 'i': "īíǐì", 'u': "ūúǔù", 'v': "ǖǘǚǜ"}


def idiom_lib_init(idiom_file):
    with open(idiom_file, 'r', encoding="utf8") as ir:
        return [x for x in json.loads(ir.read()) if len(x['word'])==4]


idiom_lib = idiom_lib_init(idiom_file)


def search_idiom(input_idiom, idiom_lib):
    for item in idiom_lib:
        if input_idiom == item['word']:
            return item
    exit()


def extract_pinyin(target_idiom_dic):
    idiom_pinyin = target_idiom_dic['pinyin']
    for item in replace_char_dict_extract:
        idiom_pinyin = re.sub(r'[' + item + ']', replace_char_dict_extract[item], idiom_pinyin)
    return idiom_pinyin.replace("yie","ye")


def search_next_idiom(former_pinyin, idiom_lib):
    last_word_pinyin = former_pinyin.split(" ")[-1]
    search_pinyin_list = []
    for item in replace_char_dict_bootstrap:
        if item in last_word_pinyin:
            for x in replace_char_dict_bootstrap[item]:
                search_pinyin_list.append(last_word_pinyin.replace(item, x))
    # print(search_pinyin_list)
    next_idiom_list = []
    for item in search_pinyin_list:
        next_idiom_list += [x['word'] for x in idiom_lib if (re.match(r'^' + item + ' ', x['pinyin']) != None) and len(x['word'])==4]
    return next_idiom_list


def same_word_linkage(input_idiom, next_idiom_list):
    return [x for x in next_idiom_list if re.match(r'^' + input_idiom[-1], x)]


def yi_ge_ding_lia(next_idiom_list, same_word_list, idiom_dic):


    if re.match(r'^yi ', extract_pinyin(search_idiom(next_idiom_list[0], idiom_dic))) != None:
        return "一个顶俩"
    else:
        end_with_yi_list = [x for x in next_idiom_list if
                            re.search(r' yi\Z', extract_pinyin(search_idiom(x, idiom_dic))) != None]
        if end_with_yi_list.__len__()!=0:
            #print(end_with_yi_list)
            return random.choice(end_with_yi_list)
        elif same_word_list.__len__() != 0:
            return random.choice(same_word_list)
        elif next_idiom_list.__len__() != 0:
            return random.choice(next_idiom_list)
        else:
            return 0


idiom_input_sample = random.choice(idiom_lib)['word']
# idiom_input_sample = "坚壁清野"
idiom_trace = []
count=1
while True:
    print("%s: %s" % (count,idiom_input_sample))
    idiom_trace.append(idiom_input_sample)
    search_test = search_idiom(idiom_input_sample, idiom_lib)
    print(search_test)
    extract_pinyin_test = extract_pinyin(search_test)
    print("extract_pinyin_test = %s" % extract_pinyin_test)
    pinyin_list_test = search_next_idiom(extract_pinyin_test, idiom_lib)
    print("pinyin_list_test = %s" % pinyin_list_test)

    same_word_list_test = same_word_linkage(idiom_input_sample, pinyin_list_test)
    print("same_word_list_test = %s" % same_word_list_test)
    ygdl_test = yi_ge_ding_lia(pinyin_list_test, same_word_list_test, idiom_lib)

    if ygdl_test != "一个顶俩":
        idiom_input_sample = ygdl_test
        count +=1
    else:
        count += 1

        print("%s: 一个顶俩" % count)
        idiom_trace.append("一个顶俩")
        if count > 4:
            with open("./record.log", 'a') as record:
                record.write('->'.join(idiom_trace))
                record.write("\n==============================================================\n\n")
        print("==============================================================\n\n\n\n")
        print('->'.join(idiom_trace))
        idiom_input_sample = random.choice(idiom_lib)['word']
        idiom_trace = []
        count = 1
    pass
