import mysql.connector
import datetime

db = mysql.connector.connect(host='HOST', user='USER', passwd='PASSWORD', db='DB')
cursor = db.cursor()

def InsertGame():
    MatchType = input("MatchType: ")
    PlayerA = input("Player A: ")
    ScoreA = input("Player A Score: ")
    PlayerB = input("Player B: ")
    ScoreB = input("Player B Score: ")

    DT = datetime.datetime.now().strftime('%Y-%m-%d')

    val = [str(DT), str(MatchType), str(PlayerA), str(ScoreA), str(ScoreB), str(PlayerB)]
    values = "('{}', '{}', '{}', '{}', '{}', '{}')".format(val[0], val[1], val[2], val[3], val[4], val[5])
    query = "INSERT INTO GameLog (Date, MatchType, PlayerA, PlayerAScore, PlayerBScore, PlayerB) VALUES " + str(values)
    cursor.execute(query)
    db.commit()
    print('ok')

    if ScoreA > ScoreB:
        return [PlayerA, PlayerB]
    elif ScoreB > ScoreA:
        return [PlayerB, PlayerA]
    else:
        return [PlayerA, PlayerB]

def GetOldRating(player):
    query = "SELECT ELORating FROM rankings WHERE Player = '" + player +"'"
    cursor.execute(query)
    result = cursor.fetchall()
    return result[0][0]

def MatchType():
    query = "SELECT MatchType FROM gamelog WHERE ID = (SELECT max(ID) FROM gamelog)"
    cursor.execute(query)
    result = cursor.fetchall()
    type = result[0][0]
    if type == 'Tournament':
        return 60
    elif type == 'Season':
        return 40
    elif type == 'Friendly':
        return 20

def GoalDifference():
    query = "SELECT PlayerAScore, PlayerBScore FROM gamelog WHERE ID = (SELECT max(ID) FROM gamelog)"
    cursor.execute(query)
    result = cursor.fetchall()
    ScoreA = int(result[0][0])
    ScoreB = int(result[0][1])
    GD = ScoreA - ScoreB
    if GD == 0 or GD == 1:
        return 1
    elif GD == 2:
        return 1.5
    else:
        return (11+GD)/8

def WinExpectancy():
    query = "SELECT PlayerA, PlayerB FROM gamelog WHERE ID = (SELECT max(ID) FROM gamelog)"
    cursor.execute(query)
    result = cursor.fetchall()
    PlayerA = result[0][0]
    PlayerB = result[0][1]
    query = "SELECT ELORating FROM rankings WHERE Player = '" + PlayerA +"'"
    cursor.execute(query)
    result1 = cursor.fetchall()
    CurrentRating = float(result1[0][0])
    query = "SELECT ELORating FROM rankings WHERE Player = '" + PlayerB + "'"
    cursor.execute(query)
    result2 = cursor.fetchall()
    OpponentRating = float(result2[0][0])
    dr = CurrentRating - OpponentRating
    We = 1 / ( (10**(-(dr/400))) + 1)
    return We

def Result():
    query = "SELECT PlayerAScore, PlayerBScore FROM gamelog WHERE ID = (SELECT max(ID) FROM gamelog)"
    cursor.execute(query)
    result = cursor.fetchall()
    ScoreA = int(result[0][0])
    ScoreB = int(result[0][1])
    difference = ScoreA - ScoreB
    if difference == 0:
        return 0.5
    elif difference > 0:
        return 1
    elif difference < 0:
        return 0

def GenerateRating():
    Players = InsertGame()
    PlayerA = Players[0]
    PlayerB = Players[1]
    R_oldA = GetOldRating(PlayerA)
    R_oldB = GetOldRating(PlayerB)
    K = MatchType()
    G = GoalDifference()
    W = Result()
    We = WinExpectancy()
    P = abs(K*G*(W-We))
    RWINNER = R_oldA + P
    RLOSER = R_oldB - P

    query1 = "UPDATE Rankings SET ELORating = " + str(RWINNER) + " WHERE Player = " + "'" + str(PlayerA) + "'"
    cursor.execute(query1)
    db.commit()

    query2 = "UPDATE Rankings SET ELORating = " + str(RLOSER) + " WHERE Player = " + "'" + str(PlayerB) + "'"
    cursor.execute(query2)
    db.commit()
    return True

GenerateRating()
query = ("SELECT * FROM Rankings")
cursor.execute(query)
result = cursor.fetchall()
for i in result:
    print(i)
