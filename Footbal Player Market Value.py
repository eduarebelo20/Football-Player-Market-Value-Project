import pandas as pd
import numpy as np
import scipy.stats as st

offense = pd.read_csv("\\Users\\eduar\\Football-Player-Market-Value-Project\\offense.csv")
defense = pd.read_csv("\\Users\\eduar\\Football-Player-Market-Value-Project\\defensive.csv")
goalkeepers = pd.read_csv("\\Users\\eduar\\Football-Player-Market-Value-Project\\goalkeepers.csv")
followers = pd.read_csv("\\Users\\eduar\\Football-Player-Market-Value-Project\\Number of followers 2021.02.22.csv")

# Convert Data Types That Need Conversion For Offense Dataset

offense.columns = ['Player', 'Season - Club played for', 'Competition name',
       'Value currency (million)', 'Market value',
       'Current club (20/21 season)', 'Player nationality', 'Player age',
       'Position', 'games_appearances', 'mins_played', 'goals', 'goal_assist',
       'Average of Attempts per 90 mins weighted by mins_played per _Season - Club - Competition',
       'total_scoring_att',
       'Average of Attempts on target weighted by mins_played per _Season - Club - Competition (%)',
       'Average of Conversion rate weighted by total_scoring_att per _Season - Club - Competition (%)',
       'Big chances missed',
       'Average of Minute per goal weighted by goals per _Season - Club - Competition',
       'Average of Minute per assist weighted by goals per _Season - Club - Competition',
       'Average of Minute per goal or assist weighted by goals per _Season - Club - Competition',
       'Dribbles per 90 minutes weighted by mins_played per _Season - Club - Competition',
       'Offsides per 90 mins weighted by mins_played per _Season - Club - Competition',
       'Was fouled per 90 mins weighted by mins_played per _Season - Club - Competition',
       'att_pen_goal', 'Penalties missed',
       'Average of Penalty conversion rate weighted by mins_played per _Season - Club - Competition (%)']

x = []
for age in list(offense['Player age']):
    x.append(float(str(age).replace(',','.')))
offense['Player age'] = x

a = 0
b = []
for num in list(offense['Average of Attempts on target weighted by mins_played per _Season - Club - Competition (%)']):
    a = str(num).replace(',','.')
    b.append(float(a.replace('%','')))
offense['Average of Attempts on target weighted by mins_played per _Season - Club - Competition (%)'] = b

a = 0
b = []
for num in list(offense['Average of Conversion rate weighted by total_scoring_att per _Season - Club - Competition (%)']):
    a = str(num).replace(',','.')
    b.append(float(a.replace('%','')))
offense['Average of Conversion rate weighted by total_scoring_att per _Season - Club - Competition (%)'] = b

a = 0
b = []
for num in list(offense['Average of Penalty conversion rate weighted by mins_played per _Season - Club - Competition (%)']):
    a = str(num).replace(',','.')
    b.append(float(a.replace('%','')))
offense['Average of Penalty conversion rate weighted by mins_played per _Season - Club - Competition (%)'] = b

#Selecting Only The Offensive Players

offensive_players = offense[(offense['Position'] == 'FW') | (offense['Position'] == 'LW') | (offense['Position'] == 'RW') | (offense['Position'] == 'AM') | (offense['Position'] == 'CM') & (offense['Competition name'] != 'UEFA Champions League') & (offense['Competition name'] != 'UEFA Europa League') & (offense['Competition name'] != 'German Bundesliga Playoff')]
offensive_players = offensive_players.groupby(['Player'], as_index = False).agg('mean')
offensive_players = offensive_players.drop(['Average of Penalty conversion rate weighted by mins_played per _Season - Club - Competition (%)', 'Penalties missed', 'att_pen_goal'], axis = 1)
offensive_players = offensive_players.fillna(0)

#Correlations for The Offensive Players Data Frame

offensive_players_corr = offensive_players.corr(method = 'spearman')

#Create a Data Frame To Serve as Index

df1 = pd.DataFrame()
for name in offensive_players.columns:
    if name != 'Player':
        x = sorted(offensive_players[name], key = float)
        df1[name] = x
        
#Create Array With the Indexes of Each Players Stats

x = []
y = []
for i in range(162):
    x.append(y)
    y = []
    for col in offensive_players.columns:
        if col != 'Player':
            y.append(list(df1[col]).index(offensive_players[col][i]))
x.append(y)

x.pop(0) #Don't do this step more then once
a = []
b = []
for lst in x:
    b = []
    for i in range(17):
        b.append((lst[i] - lst[0]) * offensive_players_corr['Market value'][i])
    
    b.pop(0)   
    if 0 > sum(b):
        a.append('Over')
    else:
        a.append('Under')

#Create Data Frame with The Offensive Players Names and If They are Over or Under Valued

final_df_offensive = pd.DataFrame()

social_media = []
for player in list(offensive_players['Player']):
    if player in list(followers['Name']):
        social_media.append('Influent')
    else:
        social_media.append('Non-Influent')
        
justified_overvalue = []
for i in range(len(a)):
    if (a[i] == 'Over') & (social_media[i] == 'Influent'):
        justified_overvalue.append('Justified')
    elif (a[i] == 'Over') & (social_media[i] == 'Non-Influent'):
        justified_overvalue.append('Unjustified')
    else:
        justified_overvalue.append('-')
        
final_df_offensive['Player'] = offensive_players['Player']
final_df_offensive['Under or Over Valued According to In-Game Stats'] = a
final_df_offensive['Social Media'] = social_media
final_df_offensive['Over Value Justification'] = justified_overvalue

#Convert Data Types That Need Conversion For Defense Dataset

defense.columns = ['Player', 'Season - Club played for', 'Competition name',
       'Value currency (millions)', 'Market value', 'Current club',
       'Player nationality', 'Age', 'Position', 'games_appearances',
       'mins_played',
       'Tackle success rate weighted by total_tackle per _Season - Club - Competition (%)',
       'TACKLES (succesful) per 90 mins weighted by mins_played per _Season - Club - Competition',
       'Média de CLEARANCES per 90 mins',
       'INTERCEPTIONS per 90 mins weighted by mins_played per _Season - Club - Competition',
       'BLOCKS per 90 mins weighted by mins_played per _Season - Club - Competition',
       'BALL RECOVERY per 90 mins weighted by mins_played per _Season - Club - Competition',
       'FOULS per 90 mins weighted by mins_played per _Season - Club - Competition',
       'won_tackle', 'Blocked shots/passes/crosses', 'total_clearance',
       'interception', 'ball_recovery', 'own_goals', 'error_lead_to_goal',
       'penalty_conceded']


z = []
for age in list(defense['Age']):
    z.append(float(str(age).replace(',','.')))
defense['Age'] = z

a = 0
b = []
for num in list(defense['Tackle success rate weighted by total_tackle per _Season - Club - Competition (%)']):
    a = str(num).replace(',','.')
    b.append(float(a.replace('%','')))
defense['Tackle success rate weighted by total_tackle per _Season - Club - Competition (%)'] = b

#Selecting Only The Defensive Players

defensive_players = defense[(defense['Position'] == 'CB') | (defense['Position'] == 'LB') | (defense['Position'] == 'RB') | (defense['Position'] == 'DM') & (defense['Competition name'] != 'UEFA Champions League') & (defense['Competition name'] != 'UEFA Europa League') & (defense['Competition name'] != 'German Bundesliga Playoff')]
defensive_players = defensive_players.groupby(['Player'], as_index = False).agg('mean')
defensive_players = defensive_players.fillna(0)

#Create a Data Frame To Serve as Index

df1 = pd.DataFrame()
for name in defensive_players.columns:
    if name != 'Player':
        x = sorted(defensive_players[name], key = float)
        df1[name] = x
        
#Correlations for The Defensive Players Data Frame

defensive_players_corr = defensive_players.corr(method = 'spearman')

#Create Array With the Indexes of Each Players Stats

x = []
y = []
for i in range(49):
    x.append(y)
    y = []
    for col in defensive_players.columns:
        if col != 'Player':
            y.append(list(df1[col]).index(defensive_players[col][i]))
x.append(y)

x.pop(0) #Don't do this step more than once
a = []
b = []
for lst in x:
    b = []
    for i in range(17):
        b.append((lst[i] - lst[0]) * defensive_players_corr['Market value'][i])
    
    b.pop(0)   
    if 0 > sum(b):
        a.append('Over')
    else:
        a.append('Under')
        
#Create Data Frame with The Defensive Players Names and If They are Over or Under Valued

final_df_defensive = pd.DataFrame()

social_media = []
for player in list(defensive_players['Player']):
    if player in list(followers['Name']):
        social_media.append('Influent')
    else:
        social_media.append('Non-Influent')
        
justified_overvalue = []
for i in range(len(a)):
    if (a[i] == 'Over') & (social_media[i] == 'Influent'):
        justified_overvalue.append('Justified')
    elif (a[i] == 'Over') & (social_media[i] == 'Non-Influent'):
        justified_overvalue.append('Unjustified')
    else:
        justified_overvalue.append('-')
        
final_df_defensive['Player'] = defensive_players['Player']
final_df_defensive['Under or Over Valued According to In-Game Stats'] = a
final_df_defensive['Social Media'] = social_media
final_df_defensive['Over Value Justification'] = justified_overvalue

#Convert Data Types That Need Conversion For GoalKeeper Dataset

z = []
for age in list(goalkeepers['Player age']):
    z.append(float(str(age).replace(',','.')))
goalkeepers['Player age'] = z

z = []
for age in list(goalkeepers['Saves per 90 mins weighted by mins_played per _Season - Club - Competition']):
    z.append(float(str(age).replace(',','.')))
goalkeepers['Saves per 90 mins weighted by mins_played per _Season - Club - Competition'] = z

a = 0
b = []
for num in list(goalkeepers['Average of Save % (overall) weighted by Total attempts faced per _Season - Club - Competition']):
    a = str(num).replace(',','.')
    b.append(float(a.replace('%','')))
goalkeepers['Average of Save % (overall) weighted by Total attempts faced per _Season - Club - Competition'] = b

a = 0
b = []
for num in list(goalkeepers['Average of Save % (attempts outside the box) weighted by Total attempts faced (obox) per _Season - Club - Competition']):
    a = str(num).replace(',','.')
    b.append(float(a.replace('%','')))
goalkeepers['Average of Save % (attempts outside the box) weighted by Total attempts faced (obox) per _Season - Club - Competition'] = b

a = 0
b = []
for num in list(goalkeepers['Average of Save % (attempts in the box) weighted by Total attempts faced (ibox) per _Season - Club - Competition']):
    a = str(num).replace(',','.')
    b.append(float(a.replace('%','')))
goalkeepers['Average of Save % (attempts in the box) weighted by Total attempts faced (ibox) per _Season - Club - Competition'] = b

a = 0
b = []
for num in list(goalkeepers['Penalty save % weighted by penalty_faced per _Season - Club - Competition']):
    a = str(num).replace(',','.')
    b.append(float(a.replace('%','')))
goalkeepers['Penalty save % weighted by penalty_faced per _Season - Club - Competition'] = b

#Create a Data Frame To Serve as Index

goalkeepers_df = goalkeepers[(goalkeepers['Competition name'] != 'UEFA Champions League') & (goalkeepers['Competition name'] != 'UEFA Europa League') & (goalkeepers['Competition name'] != 'German Bundesliga Playoff')]
goalkeepers_df = goalkeepers_df.groupby(['Player'], as_index = False).agg('mean')

df1 = pd.DataFrame()
for name in goalkeepers_df.columns:
    if name != 'Player':
        x = sorted(goalkeepers_df[name], key = float)
        df1[name] = x
        
#Correlations for The Goalkeepers Data Frame

goalkeepers_corr = goalkeepers_df.corr(method = 'spearman')

#Create Array With the Indexes of Each Players Stats

x = []
y = []
for i in range(9):
    x.append(y)
    y = []
    for col in goalkeepers_df.columns:
        if col != 'Player':
            y.append(list(df1[col]).index(goalkeepers_df[col][i]))
x.append(y)

x.pop(0) #Don't do this step more than one time
a = []
b = []
for lst in x:
    b = []
    for i in range(14):
        b.append((lst[i] - lst[0]) * defensive_players_corr['Market value'][i])
    
    b.pop(0)   
    if 0 > sum(b):
        a.append('Over')
    else:
        a.append('Under')
        
#Create Data Frame with The Offensive Players Names and If They are Over or Under Valued

final_df_goalkeepers = pd.DataFrame()

social_media = []
for player in list(goalkeepers_df['Player']):
    if player in list(followers['Name']):
        social_media.append('Influent')
    else:
        social_media.append('Non-Influent')
        
justified_overvalue = []
for i in range(len(a)):
    if (a[i] == 'Over') & (social_media[i] == 'Influent'):
        justified_overvalue.append('Justified')
    elif (a[i] == 'Over') & (social_media[i] == 'Non-Influent'):
        justified_overvalue.append('Unjustified')
    else:
        justified_overvalue.append('-')
        
final_df_goalkeepers['Player'] = goalkeepers_df['Player']
final_df_goalkeepers['Under or Over Valued According to In-Game Stats'] = a
final_df_goalkeepers['Social Media'] = social_media
final_df_goalkeepers['Over Value Justification'] = justified_overvalue

#Statistical Testing

#Goodness of Fit:

#Assume that the Sports Director claimed that the top offensive players in the top 11 leagues of Europe + English second
#division with a market value from 40M to 60M should have ate least this many goals and assists combined by position CM = 8,
#AM = 10, FW = 15, LW = 15, FW = 20.

off = offense[(offense['Market value'] > 40.0) & (offense['Market value'] < 60.0) & (offense['Competition name'] != 'UEFA Champions League') & (offense['Competition name'] != 'UEFA Europa League') & (offense['Competition name'] != 'German Bundesliga Playoff')]
columns_wanted = ['goals', 'goal_assist']
off = off.groupby(['Position'], as_index = False)[columns_wanted].agg('mean')
off = off[(off['Position'] == 'AM') | (off['Position'] == 'LW') | (off['Position'] == 'RW') | (off['Position'] == 'FW') | (off['Position'] == 'CM')]

goals = list(off['goals'])
assists = list(off['goal_assist'])
observed = np.array([goals[0] + assists[0], goals[1] + assists[1], goals[2] + assists[2], goals[3] + assists[3], goals[4] + assists[4]])
expected = np.array([10, 8, 20, 15, 15])

#Perform the Test ChiSquare for a 95% Confidence Level

st.chisquare(observed, expected)
print("We can't refute the expected results. But we can say that the Sports Director claim isn't very accurate.")

#Confidence Intervals

# The sports director believes that the club needs to by reinforced in the defense, midfield and attack, buying players
#that need to fulfill some requirements And he wants me to check what is the price that the club should pay for a player in
#order for the club to be almost sure that he will fulfill those requirements

#He wants to know how high he can expect the AVERAGE (THE CONFIDENCE INTERVAL LOSES MEANING IF IT IS NOT THE AVERAGE)
#market value to be for a player from a more attacking nature that can play any of the front 3 positions (LW, RW, FW),
#that can score on average more than 10 goals per season in the league

off = offense[(offense['Competition name'] != 'UEFA Champions League') & (offense['Competition name'] != 'UEFA Europa League') & (offense['Competition name'] != 'German Bundesliga Playoff') & (offense['Position'] == 'LW') | (offense['Position'] == 'RW') | (offense['Position'] == 'FW') ]
columns_wanted = ['goals', 'Market value']
off = off.groupby(['Player'], as_index = False)[columns_wanted].agg('mean')
off = off[off['goals'] > 9.9]

sample = off['Market value'].sample(15)
n = len(sample)
mean = np.mean(sample)
sem = st.sem(sample)
z = st.t.ppf(0.95, n-1)
h = sem*z
CI = (mean-h, mean+h)
print(CI)

#Unfortunately we can only buy players that are valued between 20M and 40M for a player for those position

off = offense[(offense['Competition name'] != 'UEFA Champions League') & (offense['Competition name'] != 'UEFA Europa League') & (offense['Competition name'] != 'German Bundesliga Playoff') & (offense['Position'] == 'LW') | (offense['Position'] == 'RW') | (offense['Position'] == 'FW')]
columns_wanted = ['goals', 'Market value']
off = off.groupby(['Player'], as_index = False)[columns_wanted].agg('mean')
off = off[(off['Market value'] < 40.1) & (off['Market value'] > 19.9)]

sample = off['goals'].sample(15)
n = len(sample)
mean = np.mean(sample)
sem = st.sem(sample)
z = st.t.ppf(0.95, n-1)
h = sem*z
CI = (mean-h, mean+h)
print(CI)

#He wants to know how high he can expect the AVERAGE (THE CONFIDENCE INTERVAL LOSES MEANING IF IT IS NOT THE AVERAGE)
#market value to be for a player from a more attacking nature that can play any of the more attacking midfield positions
#(CM, AM), that can score 2 goals or more and provide 4 assists or more per season in the league

off = offense[(offense['Competition name'] != 'UEFA Champions League') & (offense['Competition name'] != 'UEFA Europa League') & (offense['Competition name'] != 'German Bundesliga Playoff') & (offense['Position'] == 'CM') | (offense['Position'] == 'AM')]
columns_wanted = ['goals', 'Market value', 'goal_assist']
off = off.groupby(['Player'], as_index = False)[columns_wanted].agg('mean')
off = off[(off['goals'] > 1.9) & (off['goal_assist'] > 3.9)]

sample = off['Market value'].sample(15)
n = len(sample)
mean = np.mean(sample)
sem = st.sem(sample)
z = st.t.ppf(0.95, n-1)
h = sem*z
CI = (mean-h, mean+h)
print(CI)

#He wants to know how high he can expect the AVERAGE (THE CONFIDENCE INTERVAL LOSES MEANING IF IT IS NOT THE AVERAGE)
#market value to be for a player from a more defensive nature that can play any of the more defending positions in the mid
#and in the defense (DM, CB, LB, RB), with 1.5 or more interceptions per 90 mins per mins playerd, 6.5 or more ball
#recoveries per 90 mins per mins played and 1.5 sucessful tackles per 90 mins per mins played because he want a very
#pressing and agressive defense that wins the ball a lot during the game

columns_wanted = ['INTERCEPTIONS per 90 mins weighted by mins_played per _Season - Club - Competition', 'BALL RECOVERY per 90 mins weighted by mins_played per _Season - Club - Competition', 'TACKLES (succesful) per 90 mins weighted by mins_played per _Season - Club - Competition']
defe = defensive_players[(defensive_players['INTERCEPTIONS per 90 mins weighted by mins_played per _Season - Club - Competition'] > 1.4) & (defensive_players['BALL RECOVERY per 90 mins weighted by mins_played per _Season - Club - Competition'] > 6.4) & (defensive_players['TACKLES (succesful) per 90 mins weighted by mins_played per _Season - Club - Competition'] > 1.4)]


sample = off['Market value'].sample(15)
n = len(sample)
mean = np.mean(sample)
sem = st.sem(sample)
z = st.t.ppf(0.95, n-1)
h = sem*z
CI = (mean-h, mean+h)
print(CI)