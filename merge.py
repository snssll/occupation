import pandas as pd
import os

df = pd.read_csv('tasks.csv')
df['index'] = range(len(df))

file_list = os.listdir('./output/')
file_list = [int(file.split('.')[0]) for file in file_list if file.endswith('.txt')]
file_list.sort()

def fetch_indicator(ai_output):
    label = ''
    confidence = ''
    div = [x for x in ai_output.split("\n") if x != ""]
    if len(div) > 2:
        if 'E0' in div[-2]:
            label = 'E0'
        elif 'E1' in div[-2]:
            label = 'E1'
        elif 'E2' in div[-2]:
            label = 'E2'
        elif 'E3' in div[-2]:
            label = 'E3'
        
        if 'high' in div[-1] or 'High' in div[-1]:
            confidence = 'high'
        elif 'moderate' in div[-1] or 'Moderate' in div[-1]:
            confidence = 'moderate'
        elif 'low' in div[-1] or 'Low' in div[-1]:
            confidence = 'low'

    return label, confidence

for index in file_list:
    ai_output = open(f'./output/{index}.txt', 'r').read()
    label, confidence = fetch_indicator(ai_output)
    df.loc[df['index'] == index, 'label'] = label
    df.loc[df['index'] == index, 'confidence'] = confidence

df.to_csv('results.csv', index=False)
