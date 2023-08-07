import pandas as pd
import numpy as np 
from google.colab import files
from IPython.display import clear_output

def file_upload(message):
    clear_output()
    print(message)
    user_file = files.upload()
    clear_output()
    return '/content/Input/{0}'.format(next(iter(user_file)))

def pipes():
    user_file = file_upload("Upload Civil 3D Pipe Data CSV File")
    df = pd.read_csv(user_file)
    df['UsInvert'],df['DsInvert']=np.where(df['UsInvert']<df['DsInvert'],
        (df['DsInvert'],df['UsInvert']),(df['UsInvert'],df['DsInvert']))
    df.to_csv('/content/Output/LinkPipeOutput.csv', encoding='utf-8', index=False)
    clear_output()

def basins():
    user_file = file_upload("Upload Civil Catchment Data CSV File")
    df = pd.read_csv(user_file)
    df['CN'] = (df['C'] + 1)/0.020
    df.to_csv('/content/Output/BasinDataOutput.csv', encoding='utf-8', index=False)

def simulations():
    user_file = file_upload("Upload Atlas 14 Rainfall Data CSV File")
    atlas_df = pd.read_csv(user_file, sep=',', usecols=[0,1,2,3,4,5],
                            header=0, skiprows=13, nrows=10)
    atlas_df.drop(atlas_df.head(4).index, inplace=True)

    list = []

    for index in range(atlas_df.shape[0]):
        if index > 0:
            columnSeriesObj = atlas_df.iloc[:, index]
            list1 = columnSeriesObj.tolist()
            list.extend(list1)

    rain_df = pd.DataFrame({'RainfallAmount':list})
    rain_df['RainfallAmount'] += (rain_df['RainfallAmount'] * 0.10)

    sim_df = pd.read_csv ('Output/Simulation_Files/Collection-Simulation.csv')
    sim_df['RainfallAmount'] = rain_df['RainfallAmount']
    sim_df.to_csv('/content/Output/Simulation_Files/Collection-Simulation.csv', 
                    encoding='utf-8', index=False)

def boundary():
    # df = pd.read_csv ('/content/Input/Node - Time Series.csv')
    user_file = file_upload("Upload fill model time series data")
    df = pd.read_csv(user_file)
    boundary_stage_point = df.reindex(df.columns.tolist() + ['Year', 'Month', 'Day'], axis=1)
    boundary_stage_point = boundary_stage_point.rename(columns={'Sim': 'Set', 
                                                                'Node Name': 'Parent', 
                                                                'Relative Time [hrs]': 'Hour', 
                                                                'Stage [ft]': 'Stage'})
    boundary_stage_point = boundary_stage_point[['Set', 'Parent', 'Year', 'Month', 'Day', 'Hour', 'Stage']]

    nodes = df['Node Name'].unique()
    simulations = df['Sim'].unique()

    boundary_stage_set = pd.DataFrame(simulations, columns =['Name']) 
    boundary_stage_set['Comment'] = np.nan
   
    combined_list = []
    for sim in simulations:
        for node in nodes:
            row = [sim, node, '']
            combined_list.append(row)
    boundary_stage = pd.DataFrame(combined_list, columns =['Parent', 'Name', 'Comment']) 

    boundary_stage_point.to_csv('/content/Output/Boundary_Files/Collection-BoundaryStage_Point.csv',
                    encoding='utf-8', index=False)
    boundary_stage_set.to_csv('/content/Output/Boundary_Files/Collection-BoundaryStageSet.csv',
                    encoding='utf-8', index=False)
    boundary_stage.to_csv('/content/Output/Boundary_Files/Collection-BoundaryStage.csv',
                    encoding='utf-8', index=False)
