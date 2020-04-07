# Data Extractor for agents
In this repository, **Cyrus**  team have added C++ and Python scripts to **Agent2d-base** to extract data from agents in some specific situations.

## DataExtractor.cpp/.h
In this class we have **update** function that is run every time chain action decide an action, and extract **features** and write them into files for each agent.
the file names determine agent unum and opponents team name and if parallel games run at time, it separate them by port of agents.

### Option
**DataExtractor** class  have a struct option that user can select easily which feature wants to write in the file for which team.
 
 ```c++
 DataExtractor::Option::Option() {
    side = BOTH;
    unum = BOTH;
    type = BOTH;
    body = BOTH;
    face = BOTH;
    tackling = BOTH;
    kicking = BOTH;
    card = BOTH;
    pos = BOTH;
    relativePos = BOTH;
    polarPos = BOTH;
    vel = BOTH;
    polarVel = BOTH;
    counts = BOTH;
    isKicker = BOTH;
    openAnglePass = TM;
    nearestOppDist = TM;
    polarGoalCenter = TM; // a polar vector from player to goal center
    openAngleGoal = TM;
    in_offside = TM;

    dribleAngle = Kicker;
    nDribleAngle = 12;

    worldMode = NONE_FULLSTATE;
    playerSortMode = X;

    use_convertor = true;
}
 ```
 #### dribleAngle  & nDribleAngle
 from player pos separate nDribleAngle zone and find nearest opponent in these zones, for example in angle range [30,60] dribleAngle=10, it means that in this range nearest opponent distance is 10.
  
 #### worldMode
 this feature determine from which world extract data, **world** or **fullstate_world**, in base you can change player.conf to separate these two.(in this project, player.conf have been changed for this purpose.)

#### playerSortMode
in this feature we determine the order of players to write it in file, which can be by their x of positions, or unums, or angles from kickable player. these are lambdas that used to sort the players.

#### use_convertor
this feature determine that all data should be normalize or not.

## Python Scripts
in the script directory is python script tools

### 2dDataAnalysis
this class change the data base on inputs.
#### initialization
```python3
def __init__(self, file_in, file_out, sort_type=None, randomize=0, img_mode=False)
        ```

 - **file_in**: is input file of data.
 - **file_out**: is output file that result save in it.
 - **sort_type**: sort the order of players.
 - **randomize**: in every state(cycle) randomly select n pair of player in each team and swap their order.
 - **img_mode**: determine that save result files as png file. in this mode, **file_out** should be directory.
 - **normalize**: this input determine that data would be normalized or not.

### 2DOffense.py
this file make DNN by **Keras** and start learning.

### data_extractor_merger.py
this script base on input directory and an output file, merge all input directory files and merge them in output file.

### feature_importance.py
this script read an input csv file and determine feature importance for classifier outputs, and write in csv file file for each output.(the algorithm is Random Forest Classifier.)
