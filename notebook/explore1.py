import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, "..", "data", "raw", "testfile.csv")
    return pd.read_csv(path)

#import pandas as pd
df = load_data()
print(df.head())


print(df.shape)
print(df.columns.tolist())
##What you now know about this dataset
#50,000 rows, 16 columns — a decent-sized dataset, good for analysis
#Columns fall into a few natural groups:


print(df.info())
#df.info() gives you, for every column: its data type (int64, float64, object which usually means text) and how many non-null (non-missing) values it has out of 50,000.

print(df['Year_of_Study'].unique())
print(df['Major_Category'].unique())
print(df['Burnout_Risk_Level'].unique())

#df['Year_of_Study'] → this selects just one column from your dataframe. Think of df as a whole spreadsheet, and df['ColumnName'] as picking just one column out of it (this is called a Series in pandas — a single column of data).
#.unique() → this is a method (a built-in action) that looks at every value in that column and returns each distinct value only once, removing duplicates. So instead of seeing "Senior" repeated 8,000 times, you see it just once.

print(df.describe())
#What this does: .describe() is a pandas method that, for every numeric column, computes: count, mean (average), std (how spread out the values are), min, max, and the 25th/50th/75th percentiles (quartiles) — all in one call

#notice the same thing that happened with df.head() earlier: pandas is truncating columns again (that ... in the middle), so you're only seeing Student_ID and Skill_Retention_Score, not the 7 columns hiding between them. We need to fix that before we can actually spot anything "off."

pd.set_option('display.max_columns', None)
print(df.describe())

#pd.set_option(...) → changes a pandas display setting (doesn't affect your actual data, just how it's shown)
#'display.max_columns' → the specific setting for how many columns to show before truncating
#None → means "no limit, show all of them"

##Next step — and why
#We now trust the data. Time to move from "inspecting" to "asking questions." Before writing any code, I want you to write down 3-4 questions you're curious about, based on the columns you've seen — e.g., something about GenAI hours vs GPA, or burnout vs AI dependency.

#A well-formed analytical question names exact columns and what comparison/relationship you're checking. Let's map yours to your actual columns:

#Weekly GenAI hours vs Traditional study hours → Weekly_GenAI_Hours vs Traditional_Study_Hours — good as-is, this is a relationship/correlation question
#Does GenAI reduce or increase stress? → maps to Weekly_GenAI_Hours vs Anxiety_Level_During_Exams — good question
#Skill retention gained or lost → this one needs a small fix: Skill_Retention_Score is a single score (not a before/after pair), so it's not "gained vs lost" — it's more like "what affects skill retention?" e.g., does Weekly_GenAI_Hours relate to Skill_Retention_Score? Worth deciding what you're really asking here.
#AI dependency high or low → Perceived_AI_Dependency — this is really "what's the distribution of AI dependency across students?" (a distribution question, not a comparison)
#AI dependency pre-sem vs post-sem → heads up, there's no pre/post split for Perceived_AI_Dependency in your columns — only Pre_Semester_GPA and Post_Semester_GPA have before/after versions. So this question, as stated, may not be answerable with this dataset. Did you perhaps mean GPA pre vs post (which we already glimpsed), rather than dependency?


correlation = df['Weekly_GenAI_Hours'].corr(df['Traditional_Study_Hours'])
print(correlation)

#Breaking this down:

#df['Weekly_GenAI_Hours'] → selects that one column (a Series, like before)
#.corr(df['Traditional_Study_Hours']) → this method needs two columns to compare, so you call .corr() on the first column and pass the second column into it as an argument
#This returns a single number — the correlation coefficient between those two specific columns

#What .corr() actually computes (the concept, before code)
#Correlation gives you a number between -1 and +1 for any two numeric columns:

#+1 → perfect positive relationship (as one goes up, the other always goes up too)
#-1 → perfect negative relationship (as one goes up, the other always goes down)
#0 → no relationship at all (completely unrelated)
#Values in between (like 0.3 or -0.6) tell you the strength and direction of the relationship, not perfect, but present






plt.scatter(df['Weekly_GenAI_Hours'], df['Traditional_Study_Hours'], alpha = 0.3)
plt.xlabel('Weekly_GenAI_Hours')
plt.ylabel('Traditional_Study_Hours')
plt.title('GenAI Hours Vs Traditional Study Hours')
plt.show()

#Explaining each line:

#import matplotlib.pyplot as plt → matplotlib is Python's core plotting library; pyplot is the specific module that gives you simple plotting functions; as plt is just a widely-used shorthand alias so you don't have to type matplotlib.pyplot every time
#plt.scatter(x_values, y_values, alpha=0.3) → draws the actual scatter plot

#First argument = what goes on the x-axis (Weekly_GenAI_Hours)
#Second argument = what goes on the y-axis (Traditional_Study_Hours)
#alpha=0.3 → controls transparency of each dot (0 = invisible, 1 = fully solid). With 50,000 points, dots will overlap heavily and just look like a solid blob — lowering alpha lets you see density (darker area = more overlapping points = more common combination)


#plt.xlabel(...) / plt.ylabel(...) → labels for each axis — always label your axes, a chart without labels is meaningless to anyone else (and to you, a week later)
#plt.title(...) → title for the whole chart
#plt.show() → actually renders/displays the chart window — without this line, matplotlib builds the chart internally but never shows it to you
#A scatter plot puts one variable on the x-axis, another on the y-axis, and draws one dot per row (per student, in your case). This lets you see the actual shape of a relationship — clusters, trends, outliers — instead of just one summary number like correlation. It's the standard chart for "how do two numeric variables relate to each other."


#"There is a weak negative correlation (-0.157) between weekly GenAI usage and traditional study hours, suggesting a slight tendency for heavier GenAI users to study less traditionally — but the relationship is not strong, and most students fall into a broad middle range regardless of GenAI usage."


correlation = df['Weekly_GenAI_Hours'].corr(df['Anxiety_Level_During_Exams'])
print(correlation)
#0.26907967009961153

plt.scatter(df['Weekly_GenAI_Hours'], df['Anxiety_Level_During_Exams'], alpha = 0.4)
plt.xlabel('Weekly_GenAI_Hours')
plt.ylabel('Anxiety_Level_During_Exams')
plt.title("Stress level with AI during exam")
plt.show()


x = df['Weekly_GenAI_Hours']
y = df['Anxiety_Level_During_Exams']

plt.scatter(x, y, alpha=0.4)

# calculate trend line
z = np.polyfit(x, y, 1)
p = np.poly1d(z)
plt.plot(x, p(x), color='red', linewidth=2)

plt.xlabel('Weekly GenAI Hours')
plt.ylabel('Anxiety Level During Exams')
plt.title('Stress Level with AI Usage')
plt.show()

#Explaining the new parts:

#import numpy as np → numpy is the math library pandas is built on; we need it here for the trend line calculation
#np.polyfit(x, y, 1) → this literally means "fit a polynomial of degree 1 (a straight line) to this x,y data" — it calculates the slope and intercept of the best-fit line through your cloud of points. This returns two numbers: slope and intercept.
#np.poly1d(z) → takes those two numbers and turns them into a usable function p, where p(x) gives you the line's y-value for any x
#plt.plot(x, p(x), color='red', linewidth=2) → draws that straight line in red, on top of your scatter plot, so you can see the trend clearly without guessing


#"There is a weak-to-moderate positive correlation (+0.269) between weekly GenAI usage and exam anxiety levels, with the trend line confirming a mild upward slope — suggesting students who rely more heavily on GenAI tools tend to experience somewhat higher anxiety during exams, though the effect is not strong."


#Q.The question, spelled out: Is there a relationship between how dependent a student feels on AI (Perceived_AI_Dependency) and how well they actually retain skills (Skill_Retention_Score)? If dependency is high, does retention tend to be lower (over-reliance hurting learning) or is there no clear link?

correlation = df['Skill_Retention_Score'].corr(df['Perceived_AI_Dependency'])
print(correlation)
#-0.08432431881589089

plt.figure()   # ← starts a fresh, empty chart
x = df['Skill_Retention_Score']
y = df['Perceived_AI_Dependency']

plt.scatter(x, y, alpha=0.4)

# calculate trend line
z = np.polyfit(x, y, 1)
p = np.poly1d(z)
plt.plot(x, p(x), color='red', linewidth=2)

plt.xlabel('Skill_Retention_Score')
plt.ylabel('Perceived_AI_Dependency')
plt.title('Skill retention Vs AI dependency')
plt.show()

#"There is only a very weak negative correlation (-0.084) between perceived AI dependency and skill retention score, with a nearly flat trend line — suggesting that how dependent a student feels on AI tools has little measurable relationship with how well they retain skills, at least in this dataset."


plt.figure()   # fresh canvas

plt.hist(df['Perceived_AI_Dependency'], bins=10, edgecolor='black')
plt.xlabel('Perceived AI Dependency')
plt.ylabel('Number of Students')
plt.title('Distribution of Perceived AI Dependency')
plt.show()

#plt.hist(data, bins=10, edgecolor='black') → this is matplotlib's histogram function

#First argument = the column you want to see the distribution of
#bins=10 → since your dependency scale is 1-10, using 10 bins means each bin roughly corresponds to one rating value (1, 2, 3...10) — this makes the chart easy to read cleanly
#edgecolor='black' → just draws a thin black outline around each bar so adjacent bars are visually distinct instead of blending into one solid blob


#"The distribution of perceived AI dependency is right-skewed, with most students reporting low-to-moderate dependency (peaking around 3-4 on a 1-10 scale) and very few students reporting high dependency (8-10). This suggests that, despite widespread GenAI usage, most students don't perceive themselves as heavily reliant on these tools."

