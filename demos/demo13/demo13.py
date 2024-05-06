import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import metrics

def predict_prop(model, X_test):
    return model.predict_proba(X_test)[:,1]

def predict_with_threshold(model, X_test, threshold=0.5):
    y_pred = predict_prop(model, X_test)
    return (y_pred > threshold).astype(int)

def confusion_matrix(y_test, y_pred):
    # Compare real and modeled outcomes with confusion matrix
    fig, ax = plt.subplots()
    cnf_matrix = metrics.confusion_matrix(y_test, y_pred)
    labels = np.array([
        ['\n\nTrue Negatives\n(Non-Evictions We Predicted)', '\n\nFalse Positives\n(Non-Evictions We Missed)'],
        ['\n\nFalse Negatives\n(Evictions We Missed)', '\n\nTrue Positives\n(Evictions We Predicted)']])
    # labels = np.char.add('\n', labels)
    annot = np.char.add(cnf_matrix.astype(str), labels)
    sns.heatmap(pd.DataFrame(cnf_matrix), annot=annot, cmap="YlGnBu" ,fmt='', cbar=False, yticklabels=['Not Evicted (0)','Evicted (1)'], xticklabels=['Not Evicted (0)','Evicted (1)'])
    ax.xaxis.set_label_position("top")
    plt.tight_layout()
    plt.title('Confusion matrix', y=1.1)
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.show()

def precision_recall_table(y_test, y_pred):
    target_names = ['not evicted', 'evicted']
    report = metrics.classification_report(y_test, y_pred, target_names=target_names, output_dict=True)
    return pd.DataFrame(report).transpose()

def roc_plot(model, y_test, X_test, ):
    y_pred_proba = predict_prop(model, X_test)
    fpr, tpr, _ = metrics.roc_curve(y_test,  y_pred_proba)
    auc = metrics.roc_auc_score(y_test, y_pred_proba)
    plt.plot(fpr,tpr,label="ROC, AUC="+str(auc.round(2)))
    plt.legend(loc=4)
    plt.xlabel("False Positive Rate (1 - Specificity)")
    plt.ylabel("True Positive Rate (Sensitivity)")
    plt.show()