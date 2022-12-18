from init import *
from prepare import *
from elo import *
from merge import *

from sklearn.metrics import accuracy_score, log_loss, confusion_matrix, roc_curve, roc_auc_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier, XGBRegressor
from lightgbm import LGBMRegressor, LGBMClassifier
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures


classifiers = [
    KNeighborsClassifier(3),
    SVC(probability=True),
    DecisionTreeClassifier(),
    RandomForestClassifier(),
    AdaBoostClassifier(),
    GradientBoostingClassifier(),
    GaussianNB(),
    LinearDiscriminantAnalysis(),
    QuadraticDiscriminantAnalysis(),
    LogisticRegression(),
    XGBClassifier(),
    LGBMClassifier(),
]


X, y = matches.loc[:, ['average_rank', 'rank_difference',
                       'point_difference', 'elo_difference', 'is_stake']], matches['is_won']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

log_cols = ["Classifier", "Accuracy"]
log = pd.DataFrame(columns=log_cols)

acc_dict = {}


for clf in classifiers:
    name = clf.__class__.__name__
    clf.fit(X_train, y_train)
    train_predictions = clf.predict(X_test)
    acc = accuracy_score(y_test, train_predictions)
    # figures
    fpr, tpr, _ = roc_curve(y_test, clf.predict_proba(X_test)[:, 1])
    plt.figure(figsize=(15, 5))
    ax = plt.subplot(1, 3, 1)
    ax.plot([0, 1], [0, 1], 'k--')
    ax.plot(fpr, tpr)
    ax.set_title('AUC score is {0:0.2}'.format(
        roc_auc_score(y_test, clf.predict_proba(X_test)[:, 1])))
    ax.set_aspect(1)

    ax = plt.subplot(1, 3, 2)
    cm = confusion_matrix(y_test, clf.predict(X_test))
    ax.imshow(cm, cmap='Blues', clim=(0, cm.max()))

    ax.set_xlabel('Predicted label using ' + name)
    ax.set_title('Performance on the Test set')

    ax = plt.subplot(1, 3, 3)
    cm = confusion_matrix(y_train, clf.predict(X_train))
    ax.imshow(cm, cmap='Blues', clim=(0, cm.max()))
    ax.set_xlabel('Predicted label using ' + name)
    ax.set_title('Performance on the Training set')
    pass
    if name in acc_dict:
        acc_dict[name] += acc
    else:
        acc_dict[name] = acc

for clf in acc_dict:
    acc_dict[clf] = acc_dict[clf] / 10.0
    log_entry = pd.DataFrame([[clf, acc_dict[clf]]], columns=log_cols)
    log = log.append(log_entry)


# import seaborn as sns
# import matplotlib.pyplot as plt
# plt.xlabel('Accuracy')
# plt.title('Classifier Accuracy')

# sns.set_color_codes("muted")
# sns.barplot(x='Accuracy', y='Classifier', data=log, color="b")
