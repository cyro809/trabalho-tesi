def get_proportion(array, music_dict, music_list):
    count_dict = {
        0: 0,
        1: 0,
        2: 0
    }
    zeros_sentiment_prop = {
        'pos': .0,
        'neg': .0,
        'neutral': .0
    }
    ones_sentiment_prop = {
        'pos': .0,
        'neg': .0,
        'neutral': .0
    }
    twos_sentiment_prop = {
        'pos': .0,
        'neg': .0,
        'neutral': .0
    }
    for i in range(0,len(array)):
        count_dict[array[i]] += 1
        if array[i] == 0:
            print "Label 0: ", music_list[i].strip()
            zeros_sentiment_prop[music_dict[music_list[i].strip()]['sentiment']] += 1
        elif array[i] == 1:
            print "Label 1: ", music_list[i].strip()
            ones_sentiment_prop[music_dict[music_list[i].strip()]['sentiment']] += 1
        else:
            print "Label 2: ", music_list[i].strip()
            twos_sentiment_prop[music_dict[music_list[i].strip()]['sentiment']] += 1

    print 'Total labels:'
    print "Label 0: ", count_dict[0], " Label 1: ", count_dict[1], "Label 2: ", count_dict[2]
    print "Label 0 Proportions:"
    print "pos: ", zeros_sentiment_prop['pos']/count_dict[0], "neg: ", zeros_sentiment_prop['neg']/count_dict[0], "neutral: ", zeros_sentiment_prop['neutral']/count_dict[0]
    print "####################################################################"
    print "Label 1 Proportions:"
    print "pos: ", ones_sentiment_prop['pos']/count_dict[1], "neg: ", ones_sentiment_prop['neg']/count_dict[1], "neutral: ", ones_sentiment_prop['neutral']/count_dict[1]
    print "####################################################################"
    print "Label 2 Proportions:"
    print "pos: ", twos_sentiment_prop['pos']/count_dict[2], "neg: ", twos_sentiment_prop['neg']/count_dict[2], "neutral: ", twos_sentiment_prop['neutral']/count_dict[2]


