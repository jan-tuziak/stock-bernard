import pandas as pd

data1 = {"pds":[None,None,None], "x":[2,4,6]}
df1 = pd.DataFrame.from_dict(data1)

data2 = {"a":[0,1,2], "b":[7,8,9]}
df2 = pd.DataFrame.from_dict(data2)

df1.at[0, "pds"] = df2
df1.at[1, "pds"] = df2
df1.at[2, "pds"] = df2

print(df1)