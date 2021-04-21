import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("C:\\DEV\\IA\\TP3_machinelearning\\dataset_SOON_Electric_Engine_Simulator\\2021-03-26\\gray_75_balanced.csv", header=None, names=["sound", "acc1", "acc2"])

print("\n== Dataframe description ==")
print(df.describe())  # general description of the dataframe
print("\n", df.head())  # print the first 5 lines
print("\n", df.tail(3))  # print the last 3 lines

# plot accel. data
df[['acc1','acc2']].plot()
plt.show()

# plot sound data
df['sound'].plot()

plt.show()

# merge mulple dataset
print("\n== Dataframe concatenation ==")

df2 = pd.read_csv("C:\\DEV\\IA\\TP3_machinelearning\\dataset_SOON_Electric_Engine_Simulator\\2021-03-26\\gray_75_balanced.csv", header=None, names=["sound", "acc1", "acc2"])
print("\nDataframe description")
print("\n", df2.describe())  # general description of the dataframe
print("\n", df.head())  # print the first 5 lines

result = pd.concat([df, df], axis=1) # concatenate 2 df (colum-wise)
print("\nConcatenation results")
print("\n", result.describe())
print("\n", result.head())


# convert dataframe to nparray 
print("\n== Conversion to numpy ==")
X_train = df.to_numpy()
print("Shape: ", X_train.shape)
print(X_train[0])
print(X_train[1])
