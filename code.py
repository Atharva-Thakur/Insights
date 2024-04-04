import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris

# Load the iris dataset
iris = load_iris()

# Visualize the distribution of sepal length
sns.histplot(iris['data'][:, 0])
plt.xlabel('Sepal Length')
plt.ylabel('Count')
plt.title('Distribution of Sepal Length')
plt.show()

# Visualize the relationship between sepal length and sepal width
sns.scatterplot(iris['data'][:, 0], iris['data'][:, 1])
plt.xlabel('Sepal Length')
plt.ylabel('Sepal Width')
plt.title('Relationship between Sepal Length and Sepal Width')
plt.show()

# Visualize the relationship between sepal length, sepal width, and petal length
sns.pairplot(iris['data'], hue=iris['target'])
plt.show()