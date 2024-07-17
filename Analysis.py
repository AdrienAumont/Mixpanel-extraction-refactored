from Client_Statistics_obj import ClientStatistics as client_stats
from Client_obj import Client
from Wellbeing_questionaire import Questionnaire


def calc_stats(list_of_clients: list[Client]):
    cs = client_stats(list_of_clients)
    pa_dict = {}
    analyse_pa1(pa_dict, cs)
    for i in range(1, len(list_of_clients[0].quests)):
        if cs.count_matches(lambda client: client.has_pa_i(i)) != 0:
            analyse_non_specific_pa(i, cs, pa_dict)
    return pa_dict


def analyse_pa1(pa_dict, cs):
    pa_dict['PA1 # with symptoms'] = cs.count_matches(lambda client: client.has_key_symptom_at_i('medical_score', 0))
    pa_dict['PA1 % with symptoms'] = (
        "{:.2f}".format(cs.ratio_of_matches(lambda client: client.has_key_symptom_at_i('medical_score', 0), len(cs.list_of_clients))))
    pa_dict['PA1 # no symptoms'] = len(cs.list_of_clients) - pa_dict['PA1 # with symptoms']
    pa_dict['PA1 % no symptoms'] = "{:.2f}".format(pa_dict['PA1 # no symptoms'] / len(cs.list_of_clients))
    pa_dict['PA1 UI mean symptoms'] = "{:.2f}".format(cs.mean_of_vals(
        lambda client: client.get_num_key_at_i('medical_score', 0)))
    pa_dict['PA1 UI stdv symptoms'] = "{:.2f}".format(cs.pstdv_of_vals(
        lambda client: client.get_num_key_at_i('medical_score', 0)))
    pa_dict['PA1 % stress incontinence'] = "{:.2f}".format(cs.ratio_of_matches(
        lambda client: client.has_stress(), len(cs.list_of_clients)))
    pa_dict['PA1 % urge incontinence'] = "{:.2f}".format(cs.ratio_of_matches(
        lambda client: client.has_urge(), len(cs.list_of_clients)))
    pa_dict['PA1 % mixed incontinence'] = "{:.2f}".format(cs.ratio_of_matches(
        lambda client: client.has_mixed(), len(cs.list_of_clients)))
    pa_dict['PA1 % prolapse'] = "{:.2f}".format(cs.ratio_of_matches(
        lambda client: client.has_key_symptom_at_i('medical_prolapse_4', 0), len(cs.list_of_clients)))
    pa_dict['PA1 % stage 1'] = "{:.2f}".format(cs.ratio_of_matches(
        lambda client: client.quests[0].properties['medical_prolapse_4'] == 1, len(cs.list_of_clients)))
    pa_dict['PA1 % stage 2'] = "{:.2f}".format(cs.ratio_of_matches(
        lambda client: client.quests[0].properties['medical_prolapse_4'] == 2, len(cs.list_of_clients)))
    pa_dict['PA1 % stage 3'] = "{:.2f}".format(cs.ratio_of_matches(
        lambda client: client.quests[0].properties['medical_prolapse_4'] == 3, len(cs.list_of_clients)))
    pa_dict['PA1 % stage 4'] = "{:.2f}".format(cs.ratio_of_matches(
        lambda client: client.quests[0].properties['medical_prolapse_4'] == 4, len(cs.list_of_clients)))
    pa_dict['PA1 % incontinence pads'] = "{:.2f}".format(cs.ratio_of_matches(
        lambda client: client.has_key_symptom_at_i('medical_life_1', 0), len(cs.list_of_clients)))
    pa_dict['PA1 % avoid or delay drinking'] = "{:.2f}".format(cs.ratio_of_matches(
        lambda client: client.has_key_symptom_at_i('medical_life_2', 0), len(cs.list_of_clients)))
    pa_dict['PA1 % birth'] = "{:.2f}".format(cs.ratio_of_matches(
        lambda client: client.has_key_symptom_at_i('medical_birth', 0), len(cs.list_of_clients)))
    pa_dict['PA1 % no birth'] = "{:.2f}".format(cs.ratio_of_matches(
        lambda client: client.has_not_key_symptom_at_i('medical_birth', 0), len(cs.list_of_clients)))
    pa_dict['PA1 % premenopausal'] = "{:.2f}".format(cs.ratio_of_matches(
        lambda client: client.quests[0].properties['menstrual_status'] == 'pre_menopausal', len(cs.list_of_clients)))
    pa_dict['PA1 % postmenopausal'] = "{:.2f}".format(cs.ratio_of_matches(
        lambda client: client.quests[0].properties['menstrual_status'] == 'post_menopausal', len(cs.list_of_clients)))
    pa_dict['PA1 mean subjective'] = "{:.2f}".format(cs.mean_of_vals(
        lambda client: client.get_num_key_at_i('subjective', 0)))
    pa_dict['PA1 stdv subjective'] = "{:.2f}".format(cs.pstdv_of_vals(
        lambda client: client.get_num_key_at_i('subjective', 0)))
    pa_dict['PA1 % subjective excellent'] = "{:.2f}".format(cs.ratio_of_matches(
        lambda client: client.quests[0].properties['subjective'] == 0, len(cs.list_of_clients)))
    pa_dict['PA1 % subjective good'] = "{:.2f}".format(cs.ratio_of_matches(
        lambda client: client.quests[0].properties['subjective'] == 1, len(cs.list_of_clients)))
    pa_dict['PA1 % subjective average'] = "{:.2f}".format(cs.ratio_of_matches(
        lambda client: client.quests[0].properties['subjective'] == 2, len(cs.list_of_clients)))
    pa_dict['PA1 % subjective poor'] = "{:.2f}".format(cs.ratio_of_matches(
        lambda client: client.quests[0].properties['subjective'] == 3, len(cs.list_of_clients)))
    pa_dict['PA1 % subjective very poor'] = "{:.2f}".format(cs.ratio_of_matches(
        lambda client: client.quests[0].properties['subjective'] == 4, len(cs.list_of_clients)))
    pa_dict['PA1 mean sexual wellbeing'] = "{:.2f}".format(cs.mean_of_vals(
        lambda client: client.get_num_key_at_i('sex_result', 0)))
    pa_dict['PA1 stdv sexual wellbeing'] = "{:.2f}".format(cs.pstdv_of_vals(
        lambda client: client.get_num_key_at_i('sex_result', 0)))


def analyse_non_specific_pa(i, cs, pa_dict):
    pa_dict[f'pa{i + 1} # respondents'] = cs.count_matches(lambda client: client.has_pa_i(i))
    if pa_dict[f'pa{i + 1} # respondents'] == 0:
        return
    pa_dict[f'pa{i + 1} # with UI symptoms at PA1'] = cs.count_matches(
        lambda client: client.has_key_symptom_at_i('medical_score', 0) and client.has_pa_i(i))
    pa_dict[f'pa{i + 1} % with UI symptoms at PA1'] = "{:.2f}".format(cs.ratio_of_matches(
        lambda client: client.has_pa_i(i) and client.has_key_symptom_at_i('medical_score', 0),
        pa_dict[f'pa{i + 1} # respondents']))
    pa_dict[f'pa{i + 1} # no UI symptoms at PA1'] = cs.count_matches(
        lambda client: client.has_not_key_symptom_at_i('medical_score', 0) and client.has_pa_i(i))
    pa_dict[f'pa{i + 1} % no UI symptoms at PA1'] = "{:.2f}".format(cs.ratio_of_matches(
        lambda client: client.has_pa_i(i) and client.has_not_key_symptom_at_i('medical_score', 0),
        pa_dict[f'pa{i + 1} # respondents']))
    pa_dict[f'pa{i + 1} mean time since PA1 UI'] = "{:.2f}".format(cs.mean_of_vals(
        lambda client: client.quests[i].properties.get('days_since_PA1', None)
        if client.has_key_symptom_at_i('medical_score', i) else None))
    pa_dict[f'pa{i + 1} stdv time since PA1 UI'] = "{:.2f}".format(cs.pstdv_of_vals(
        lambda client: client.delta_time_i(i) if client.has_key_symptom_at_i('medical_score', i) else None))
    pa_dict[f'pa{i + 1} % improved symptoms'] = "{:.2f}".format(cs.ratio_of_matches(
        lambda client: client.got_better_at_i('medical_score', i), pa_dict[f'pa{i + 1} # respondents']))
    pa_dict[f'pa{i + 1} % improved symptoms not cured'] = "{:.2f}".format(
        (cs.count_matches(lambda client: client.got_better_at_i('medical_score', i)) -
         cs.count_matches(lambda client: client.got_cured_at_i('medical_score', i))) /
        pa_dict[f'pa{i + 1} # respondents']
    )
    pa_dict[f'pa{i + 1} % cured'] = "{:.2f}".format(cs.ratio_of_matches(
        lambda client: client.got_cured_at_i('medical_score', i), pa_dict[f'pa{i + 1} # respondents']))
    pa_dict[f'pa{i + 1} % same symptoms'] = "{:.2f}".format(cs.ratio_of_matches(
        lambda client: client.got_no_change_at_i('medical_score', i), pa_dict[f'pa{i + 1} # respondents']))
    pa_dict[f'pa{i + 1} % worse symptoms'] = "{:.2f}".format(cs.ratio_of_matches(
        lambda client: client.got_worse_at_i('medical_score', i), pa_dict[f'pa{i + 1} # respondents']))
    pa_dict[f'pa{i + 1} developed symptoms'] = cs.count_matches(
        lambda client: client.has_dev_symptom('medical_score', i))
    pa_dict[f'pa{i + 1} Mean symptoms at PA1'] = "{:.2f}".format(cs.mean_of_vals(
        lambda client: client.get_num_key_at_i('medical_score', i)))
    pa_dict[f'pa{i + 1} Stdev symptoms at PA1'] = "{:.2f}".format(cs.pstdv_of_vals(
        lambda client: client.get_num_key_at_i('medical_score', i)))
    pa_dict[f'pa{i + 1} Mean symptom delta'] = "{:.2f}".format(cs.mean_of_vals(
        lambda client: client.delta_pa_i('medical_score', i)))
    pa_dict[f'pa{i + 1} Stdv symptom delta '] = "{:.2f}".format(cs.pstdv_of_vals(
        lambda client: client.delta_pa_i('medical_score', i)))
    pa_dict[f'pa{i + 1} UI % better subjective'] = "{:.2f}".format(cs.ratio_of_matches(
        lambda client: client.has_key_symptom_at_i('medical_score', 0) and client.got_better_at_i('subjective', i),
        pa_dict[f'pa{i + 1} # with UI symptoms at PA1']))
    pa_dict[f'pa{i + 1} UI % same subjective'] = "{:.2f}".format(cs.ratio_of_matches(
        lambda client: client.has_key_symptom_at_i('medical_score', 0) and client.got_no_change_at_i('subjective', i),
        pa_dict[f'pa{i + 1} # with UI symptoms at PA1']))
    pa_dict[f'pa{i + 1} UI % worse subjective'] = "{:.2f}".format(cs.ratio_of_matches(
        lambda client: client.has_key_symptom_at_i('medical_score', 0) and client.got_worse_at_i('subjective', i),
        pa_dict[f'pa{i + 1} # with UI symptoms at PA1']))
    pa_dict[f'pa{i + 1} Mean subjective at PA1'] = "{:.2f}".format(cs.mean_of_vals(
        lambda client: client.get_num_key_at_i('subjective', 0)))
    pa_dict[f'pa{i + 1} Stdv subjective at PA1 '] = "{:.2f}".format(cs.pstdv_of_vals(
        lambda client: client.get_num_key_at_i('subjective', 0)))
    pa_dict[f'pa{i + 1} Mean subjective delta '] = "{:.2f}".format(cs.mean_of_vals(
        lambda client: client.get_num_key_at_i('subjective', i)))
    pa_dict[f'pa{i + 1} Stdv subjective delta'] = "{:.2f}".format(cs.pstdv_of_vals(
        lambda client: client.get_num_key_at_i('subjective', i)))
    pa_dict[f'pa{i + 1} UI % better sexual wellbeing'] = "{:.2f}".format(cs.ratio_of_matches(
        lambda client: client.has_key_symptom_at_i('medical_score', 0) and client.got_better_at_i('sex_result', i),
        pa_dict[f'pa{i + 1} # with UI symptoms at PA1']))
    pa_dict[f'pa{i + 1} UI % same sexual wellbeing'] = "{:.2f}".format(cs.ratio_of_matches(
        lambda client: client.has_key_symptom_at_i('medical_score', 0) and client.got_no_change_at_i('sex_result', i),
        pa_dict[f'pa{i + 1} # with UI symptoms at PA1']))
    pa_dict[f'pa{i + 1} UI % worse sexual wellbeing'] = "{:.2f}".format(cs.ratio_of_matches(
        lambda client: client.has_key_symptom_at_i('medical_score', 0) and client.got_worse_at_i('sex_result', i),
        pa_dict[f'pa{i + 1} # with UI symptoms at PA1']))
    pa_dict[f'pa{i + 1} # with prolapse at PA1'] = cs.count_matches(
        lambda client: client.has_key_symptom_at_i('medical_prolapse_4', 0) and client.has_pa_i(i))
    pa_dict[f'pa{i + 1} mean time since PA1 P'] = "{:.2f}".format(cs.mean_of_vals(
        lambda client: client.delta_time_i(i) if client.has_key_symptom_at_i('medical_prolapse_4', 0) else None))
    pa_dict[f'pa{i + 1} stdv time since PA1 P'] = "{:.2f}".format(cs.pstdv_of_vals(
        lambda client: client.delta_time_i(i) if client.has_key_symptom_at_i('medical_prolapse_4', 0) else None))
    pa_dict[f'pa{i + 1} % better prolapse symptoms'] = "{:.2f}".format(cs.ratio_of_matches(
        lambda client: client.has_key_symptom_at_i('medical_prolapse_4', 0) and
        client.got_better_at_i('medical_prolapse_symptoms', i) and client.has_pa_i(i),
        pa_dict[f'pa{i + 1} # with prolapse at PA1']))
    pa_dict[f'pa{i + 1} % same prolapse symptoms'] = "{:.2f}".format(cs.ratio_of_matches(
        lambda client: client.has_key_symptom_at_i('medical_prolapse_4', 0) and
        client.got_no_change_at_i('medical_prolapse_symptoms', i) and client.has_pa_i(i),
        pa_dict[f'pa{i + 1} # with prolapse at PA1']))
    pa_dict[f'pa{i + 1} % worse prolapse symptoms'] = "{:.2f}".format(cs.ratio_of_matches(
        lambda client: client.has_key_symptom_at_i('medical_prolapse_4', 0) and
        client.got_worse_at_i('medical_prolapse_symptoms', i) and client.has_pa_i(i),
        pa_dict[f'pa{i + 1} # with prolapse at PA1']))
    pa_dict[f'pa{i + 1} # with no prolapse no UI at PA1'] = cs.count_matches(
        lambda client: client.has_not_key_symptom_at_i('medical_score', 0) and client.has_not_key_symptom_at_i(
            'medical_prolapse_4', i))
    pa_dict[f'pa{i + 1} mean time since PA1 NA'] = "{:.2f}".format(cs.mean_of_vals(
        lambda client: client.delta_time_i(i)
        if client.has_not_key_symptom_at_i('medical_score', 0) and client.has_not_key_symptom_at_i('medical_prolapse_4', i)
        else None
    ))
    pa_dict[f'pa{i + 1} stdv time since PA1 NA'] = "{:.2f}".format(cs.pstdv_of_vals(
        lambda client: client.delta_time_i(i)
        if client.has_not_key_symptom_at_i('medical_score', 0) and client.has_not_key_symptom_at_i('medical_prolapse_4', i)
        else None
    ))
    pa_dict[f'pa{i + 1} NA % better subjective'] = "{:.2f}".format(cs.ratio_of_matches(
        lambda client: client.got_better_at_i('subjective', i) and
        client.has_not_key_symptom_at_i('medical_score', 0) and
        client.has_not_key_symptom_at_i('medical_prolapse_4', i),
        pa_dict[f'pa{i + 1} # with no prolapse no UI at PA1']
    ))
    pa_dict[f'pa{i + 1} NA % same subjective'] = "{:.2f}".format(cs.ratio_of_matches(
        lambda client: client.got_no_change_at_i('subjective', i)
        and client.has_not_key_symptom_at_i('medical_score', 0)
        and client.has_not_key_symptom_at_i('medical_prolapse_4', i),
        pa_dict[f'pa{i + 1} # with no prolapse no UI at PA1']
    ))
    pa_dict[f'pa{i + 1} NA % worse subjective'] = "{:.2f}".format(cs.ratio_of_matches(
        lambda client: client.got_worse_at_i('subjective', i)
        and client.has_not_key_symptom_at_i('medical_score', 0)
        and client.has_not_key_symptom_at_i('medical_prolapse_4', i),
        pa_dict[f'pa{i + 1} # with no prolapse no UI at PA1']
    ))
    pa_dict[f'pa{i + 1} NA % better sexual wellbeing'] = "{:.2f}".format(cs.ratio_of_matches(
        lambda client: client.got_better_at_i('sex_result', i)
        and client.has_not_key_symptom_at_i('medical_score', 0)
        and client.has_not_key_symptom_at_i('medical_prolapse_4', i),
        pa_dict[f'pa{i + 1} # with no prolapse no UI at PA1']
    ))
    pa_dict[f'pa{i + 1} NA % same sexual wellbeing'] = "{:.2f}".format(cs.ratio_of_matches(
        lambda client: client.got_no_change_at_i('sex_result', i)
        and client.has_not_key_symptom_at_i('medical_score', 0)
        and client.has_not_key_symptom_at_i('medical_prolapse_4', i),
        pa_dict[f'pa{i + 1} # with no prolapse no UI at PA1']
    ))
    pa_dict[f'pa{i + 1} NA % worse sexual wellbeing'] = "{:.2f}".format(cs.ratio_of_matches(
        lambda client: client.got_worse_at_i('sex_result', i)
        and client.has_not_key_symptom_at_i('medical_score', 0)
        and client.has_not_key_symptom_at_i('medical_prolapse_4', i),
        pa_dict[f'pa{i + 1} # with no prolapse no UI at PA1']
    ))
