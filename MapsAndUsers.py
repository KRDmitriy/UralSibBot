import numpy as np
import pandas as pd
import math

#data = pd.read_json("http://aerothedeveloper.ru/api/office")
#[Address, CompanyID, Coordinates, Country, ID, Name, Phone, Website, WorkHours]

def CreateData(path_to_api):
    '''
    TAKE: a path to api
    RETURN: FrameWork of all banks
    '''
    try:
        data = pd.read_json(path_to_api)
        return data
    
    except:
        pass

def GetAllCoordinatesFromDataFrame(data_frame):
    '''
    TAKE: DataFrame (import pandas) with banks
    RETURN: Array with arrays if coordinates [[lat,lon]...]
    '''
    try:
        current_coordinates = data_frame['Coordinates']
        array_of_coordinates = []
        for bank in current_coordinates:
            my_coordinates = [bank['Lat'],bank['Lon']]
            array_of_coordinates.append(my_coordinates)
        return array_of_coordinates

    except:
        pass

def Rad_to_deg(rad):
    try:
        return rad * 180 / math.pi

    except:
        pass

def Deg_to_rad(deg):
    try:
        return deg * math.pi / 180.0

    except:
        pass

def CalculateDistance(lat1, lon1, lat2, lon2):
    try:
        theta = lon1-lon2
        dist = math.sin(Deg_to_rad(lat1)) * math.sin(Deg_to_rad(lat2))
        dist = dist + math.cos(Deg_to_rad(lat1))*math.cos(Deg_to_rad(lat2))*math.cos(Deg_to_rad(theta))
        dist = math.acos(dist)
        dist = Rad_to_deg(dist)
        return dist * 60 * 1.1515

    except:
        pass

def FindClosestBank(array_of_coordinates, data_frame, my_coordinates):
    '''
    TAKE: array_with_coordinates, data_frame with banks (import pandas),
          user coordinates in array form
    RETURN: Closest bank to user

    THROW ValueError if len of data_frame != len of array_of_coordinates
    '''
    try:
        if(len(data_frame) == len(array_of_coordinates)):
            min_dist = -1
            my_index = -1
            for i in range(len(data_frame)):
                if(min_dist==-1):
                    min_dist = CalculateDistance(my_coordinates[0],
                        my_coordinates[1],
                        array_of_coordinates[i][0],
                        array_of_coordinates[i][1])
                    my_index = i
                else:
                    if(min_dist>CalculateDistance(my_coordinates[0],
                        my_coordinates[1],
                        array_of_coordinates[i][0],
                        array_of_coordinates[i][1])):
                        min_dist = CalculateDistance(my_coordinates[0],
                            my_coordinates[1],
                            array_of_coordinates[i][0],
                            array_of_coordinates[i][1])
                        my_index = i
            return array_of_coordinates[my_index],data_frame.iloc[my_index]
        else:
            raise ValueError("Some banks do not have an information about coordinates!")
    
    except:
        pass

def RunPrograme(user_coordinates, path):
    '''
    TAKE:  user coordinates as an array ( [lat,lon] ), path to API with all banks
    Return: array of coordinates fo closest bank in format [lat,lon]

    WARNING: return [0] if FindClosestBank throw ValueError!
    '''
    try:
        data = CreateData(path)
        coordinates = GetAllCoordinatesFromDataFrame(data)
        try:
            result,bank = FindClosestBank(coordinates, data, user_coordinates)
        except ValueError:
            return [0]
        return result, bank[0], bank[1]
    
    except:
        pass

def FindThreeBanks(array_of_coordinates, data_frame, my_coordinates):
    try:
        first=-1
        second=-1
        third=-1
        if(len(data_frame)==len(array_of_coordinates)):
            min_dist = -1
            my_index = -1
            for i in range(len(data_frame)):
                if(min_dist==-1):
                    min_dist = CalculateDistance(my_coordinates[0],
                        my_coordinates[1],
                        array_of_coordinates[i][0],
                        array_of_coordinates[i][1])
                    my_index = i
                else:
                    if(min_dist>CalculateDistance(my_coordinates[0],
                        my_coordinates[1],
                        array_of_coordinates[i][0],
                        array_of_coordinates[i][1])):
                        min_dist = CalculateDistance(my_coordinates[0],
                            my_coordinates[1],
                            array_of_coordinates[i][0],
                            array_of_coordinates[i][1])
                        my_index = i
            first = my_index
            my_index=-1
            min_dist=-1
            ALL_COORDINATES = []
            ALL_COORDINATES.append(array_of_coordinates[first])
            for i in range(len(data_frame)):
                if(i==first):
                    continue
                if(min_dist==-1):
                    min_dist = CalculateDistance(my_coordinates[0],
                        my_coordinates[1],
                        array_of_coordinates[i][0],
                        array_of_coordinates[i][1])
                    my_index = i
                else:
                    if(min_dist>CalculateDistance(my_coordinates[0],
                        my_coordinates[1],
                        array_of_coordinates[i][0],
                        array_of_coordinates[i][1])):
                        min_dist = CalculateDistance(my_coordinates[0],
                            my_coordinates[1],
                            array_of_coordinates[i][0],
                            array_of_coordinates[i][1])
                        my_index = i
            second = my_index
            my_index=-1
            min_dist=-1
            ALL_COORDINATES.append(array_of_coordinates[second])
            for i in range(len(data_frame)):
                if(i==first or i==second):
                    continue
                if(min_dist==-1):
                    min_dist = CalculateDistance(my_coordinates[0],
                        my_coordinates[1],
                        array_of_coordinates[i][0],
                        array_of_coordinates[i][1])
                    my_index = i
                else:
                    if(min_dist>CalculateDistance(my_coordinates[0],
                        my_coordinates[1],
                        array_of_coordinates[i][0],
                        array_of_coordinates[i][1])):
                        min_dist = CalculateDistance(my_coordinates[0],
                            my_coordinates[1],
                            array_of_coordinates[i][0],
                            array_of_coordinates[i][1])
                        my_index = i
            third = my_index
            ALL_COORDINATES.append(array_of_coordinates[third])
            ALL_BANKS = []
            ALL_BANKS.append(data_frame.iloc[first])
            ALL_BANKS.append(data_frame.iloc[second])
            ALL_BANKS.append(data_frame.iloc[third])
            return ALL_COORDINATES, ALL_BANKS
        else:
            raise ValueError("Some banks do not have an information about coordinates!")

    except:
        pass

def RunProgramWithThreeBanks(user_coordinates, path):
    try:
        data=CreateData(path)
        coordinates = GetAllCoordinatesFromDataFrame(data)
        try:
            COOR, BANKS = FindThreeBanks(coordinates, data, user_coordinates)
        except ValueError:
            return [0]
        return COOR, [BANKS[0][0],BANKS[1][0],BANKS[2][0]], [BANKS[0][1],BANKS[1][1],BANKS[2][1]]

    except:
        pass

    #[ [lat, lon] [lat, lon] [lat,lon]   ]
    # [  name1, name2,name3]
    #[id1, id2,id3]