import pandas as pd
from io import StringIO
import pydotplus
from sklearn import tree
import base64


class DecisionTree:
    __df = None
    __classifier_column_name = None
    __class_names = None

    def __init__(self, datafile):
        self.__df = pd.read_csv(datafile)

    def show_classes(self):
        return self.__df.columns.values.tolist()

    def set_classifier_column(self, classifier):
        self.__classifier_column_name = classifier
        self.__class_names = \
            self.__get_unique_values(
                self.__df[self.__classifier_column_name].values)

        self.__df[self.__classifier_column_name] = \
            self.__df[self.__classifier_column_name].apply(
                self.__convert_class_names)

        self.__df = pd.get_dummies(self.__df)

    @staticmethod
    def __get_unique_values(all_values):
        return list(dict.fromkeys(all_values))

    def __convert_class_names(self, name):
        return self.__class_names.index(name)

    def __plot_decision_tree_testing(self, clf, feature_name):
        dot_data = StringIO()
        tree.export_graphviz(clf,
                             out_file=dot_data,
                             feature_names=feature_name,
                             class_names=self.__class_names,
                             filled=True,
                             rounded=True,
                             special_characters=True)
        graph = pydotplus.graph_from_dot_data(dot_data.getvalue())

        image = base64.encodebytes(graph.create_png()).decode('ascii')

        with open('picture.txt', 'w') as file:
            file.write(image)

        return graph.write_png('picture.png')

    def __plot_decision_tree(self, clf, feature_names):
        dot_data = StringIO()
        tree.export_graphviz(clf,
                             out_file=dot_data,
                             feature_names=feature_names,
                             class_names=self.__class_names,
                             filled=True,
                             rounded=True,
                             special_characters=True)
        graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
        image = base64.encodebytes(graph.create_png()).decode('ascii')
        return image

    def create_decision_tree(self, criterion='entropy', splitter='best'):
        x_axis = self.__df.loc[:, self.__df.columns != self.__classifier_column_name]
        y_axis = self.__df[self.__classifier_column_name]
        clf = tree.DecisionTreeClassifier(criterion=criterion,
                                          splitter=splitter)
        clf = clf.fit(x_axis, y_axis)
        return self.__plot_decision_tree(clf, x_axis.columns)


"""
Example:
opa = DecisionTree('tennis.csv')
opa.set_classifier_column('play')
opa.create_decision_tree()
"""
