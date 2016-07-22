import operator


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
    group_sentiment = {
        0: '',
        1: '',
        2: ''
    }
    for i in range(0, len(array)):
        count_dict[array[i][0]] += 1
        if array[i][0] == 0:
            zeros_sentiment_prop[music_dict[music_list[i].strip()]['sentiment']] += 1
        elif array[i][0] == 1:
            ones_sentiment_prop[music_dict[music_list[i].strip()]['sentiment']] += 1
        else:
            twos_sentiment_prop[music_dict[music_list[i].strip()]['sentiment']] += 1

    # print 'Total labels:'
    # print "Label 0: ", count_dict[0], " Label 1: ", count_dict[1], "Label 2: ", count_dict[2]
    # print "Label 0 Proportions:"
    # print "pos: ", zeros_sentiment_prop['pos']/count_dict[0], "neg: ", zeros_sentiment_prop['neg']/count_dict[0], "neutral: ", zeros_sentiment_prop['neutral']/count_dict[0]
    # print "####################################################################"
    # print "Label 1 Proportions:"
    # print "pos: ", ones_sentiment_prop['pos']/count_dict[1], "neg: ", ones_sentiment_prop['neg']/count_dict[1], "neutral: ", ones_sentiment_prop['neutral']/count_dict[1]
    # print "####################################################################"
    # print "Label 2 Proportions:"
    # print "pos: ", twos_sentiment_prop['pos']/count_dict[2], "neg: ", twos_sentiment_prop['neg']/count_dict[2], "neutral: ", twos_sentiment_prop['neutral']/count_dict[2]
    # print

    group_sentiment[0] = max(zeros_sentiment_prop.iteritems(), key=operator.itemgetter(1))[0]
    group_sentiment[1] = max(ones_sentiment_prop.iteritems(), key=operator.itemgetter(1))[0]
    group_sentiment[2] = max(twos_sentiment_prop.iteritems(), key=operator.itemgetter(1))[0]

    return group_sentiment


