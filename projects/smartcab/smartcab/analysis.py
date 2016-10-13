import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def analyze_all(agent_name, data_file):
    analyze("{}_parametrized".format(agent_name), "data/{}_parametrized_total_results.csv".format(data_file), [0, 6, 7, 8])
    #analyze("{}_decay".format(agent_name), "data/{}_decaying_learning_parametrized_total_results.csv".format(data_file), [0, 6, 7])
    #analyze("{}_slow_decay".format(agent_name), "data/{}_slow_decaying_learning_parametrized_total_results.csv".format(data_file), [0, 6, 7])

    analyze_groups("{}_parametrized".format(agent_name), "data/{}_parametrized_total_results.csv".format(data_file))

def analyze_groups(agent_name, data_file):
    print agent_name
    print "-------------"

    # Read agent runs data
    agent_data = pd.read_csv(data_file)

    grouped = agent_data.groupby(['alpha', 'gamma', 'epsilon'])

    f = {'n_dest_reached':['mean','std'], 'last_dest_fail':['mean','std'], 'last_penalty':['mean','std'], 'len_qvals':['mean','std']}

    aggregated_result = grouped.agg(f).reset_index()
    
    sorted_results = aggregated_result.sort([('last_penalty', 'mean'), ('last_penalty', 'std')], ascending=[1, 0]).head(n=10)

    print sorted_results
    print "-------------"
    sorted_q = aggregated_result.sort([('n_dest_reached', 'mean'), ('n_dest_reached', 'std')], ascending=[0, 1]).head(n=10)

    print sorted_q

    print "====================================="

def analyze(agent_name, data_file, drop_columns):
    # Read agent runs data
    agent_data = pd.read_csv(data_file)
    
    # Remove parameter columns
    metrics_only = agent_data.drop(agent_data.columns[drop_columns], axis=1)

    print "Agent global Metrics"
    print metrics_only.describe()

    # Rewards will be plotted somewhere wlse
    metrics_only.drop("reward_sum", axis=1, inplace=True)

    sns.boxplot(data=metrics_only)
    plt.savefig("charts/{}_global_results_boxplot.png".format(agent_name))
    plt.close()

    filtered = agent_data.sort(['last_penalty', 'last_dest_fail', 'n_dest_reached'], ascending=[1, 1, 0]).head(n=10)
    
    print "-------------"
    print "Best 10"
    print filtered.describe()
    print "------------"
    print filtered

    to_plot = filtered.drop(agent_data.columns[drop_columns], axis=1)
    to_plot.drop("reward_sum", axis=1, inplace=True)
    sns.boxplot(data=to_plot)
    plt.savefig("charts/{}_filtered_results_boxplot.png".format(agent_name))
    plt.close()


    print "====================================="
        
if __name__ == '__main__':
     # Read agent runs data
    agent_data = pd.read_csv("data/LearningAgent_results.csv")
    drop_columns = [0, 1]

    # Remove parameter columns
    metrics_only = agent_data.drop(agent_data.columns[drop_columns], axis=1)

    print "Agent global Metrics"
    print metrics_only.describe()

    sns.boxplot(data=metrics_only)
    plt.savefig("charts/final_agent_boxplot.png")
    plt.close()

    #pd.set_option('display.max_columns', None)
    #pd.set_option('display.width', 1000)
    #analyze_all("only_input_without_waypoint","OnlyInputWithoutWaypointStateAgent")
    #analyze_all("input_with_waypoint","InputWithWaypointStateAgent")
    #analyze_all("input_with_waypoint_and_deadline","InputWithWaypointAndDeadlineStateAgent")
    #analyze_all("input_with_waypoint_without_right","WithoutRightStateAgent")
    #analyze_all("input_with_waypoint_without_right_and_reduced_left","LearningAgent")
    