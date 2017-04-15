import csv
from inspect import getsourcefile
from os.path import abspath, dirname, join
from matplotlib import pyplot as plt
from sklearn.metrics import accuracy_score, precision_recall_curve, average_precision_score, f1_score, precision_score, recall_score
from sklearn.metrics import classification_report
import numpy as np

class_list = ['pos', 'neg', 'neu']


def get_dataset(filepath):
    """
    Gets labelled dataset for sentiment analysis evaluation
    returns a dictionary (text,scores,label) with /t delimiters
    """
    # full_filepath = join(dirname(abspath(getsourcefile(lambda: 0))),
    # filepath)
    fpath = "c:\\Users\\ZackTong\\Desktop\\TwitterFYP\\outData\\" + filepath
    with open(fpath, encoding='utf8') as dataset:
        dialect = csv.Sniffer().sniff(dataset.read(1024), delimiters="\t")
        dataset.seek(0)
        tweet_data = list(list(rec) for rec in csv.reader(dataset, dialect))
    return tweet_data


def evaluate(binarise_result, y_test, y_score, file_name):
    """
    computes the accuracy, precision and recall. 
    plots the precision and recall curve.
    :
        param binarise_result:
            list of binarised result after prediction from classifier
    :
        type binarise_result:
            list[list[int]]
    :
        param y_test:
            list of binarised labels from the test set
    :
        type y_test:
            list[list[int]]
    :
        param y_score:
            distance of each sample from the decision boundary for each class
    :
        type y_score:
            list
    :
        param file_name:
            directory name for saving all figures from the plots
    :
        type file_name:
            str
    :
        return:
    :
        rtype:
    """
    num_class = y_test.shape[1]

    # Compute Precision-Recall and plot curve
    precision = dict()
    recall = dict()
    average_precision = dict()
    for i in range(num_class):
        precision[i], recall[i], _ = precision_recall_curve(
            y_test[:, i], y_score[:, i])
        average_precision[i] = average_precision_score(
            y_test[:, i], y_score[:, i])

    # Compute micro-average ROC curve and ROC area
    precision["micro"], recall["micro"], _ = precision_recall_curve(
        y_test.ravel(), y_score.ravel())
    average_precision["micro"] = average_precision_score(
        y_test, y_score, average="micro")

    # plots
    plot_precision_recall_curve(
        average_precision, precision, recall, file_name)
    # Plot Precision-Recall curve for each class
    plot_precision_recall_curve_all_classes(average_precision, precision, recall, file_name,
                                            num_class)

    generate_eval_metrics(binarise_result, file_name, y_test)


def generate_eval_metrics(result, file_name, y_test):
    accuracy = accuracy_score(np.array(y_test), np.array(result))
    precision = precision_score(y_test, result, average="macro")
    recall = recall_score(y_test, result, average="macro")
    f1_measure = f1_score(y_test, result, average="macro")

    # save results in a txt file
    with open(file_name + "_result.txt", "w") as text_file:
        text_file.write("Accuracy: {0}\n".format(accuracy))
        text_file.write("Precision: {0}\n".format(precision))
        text_file.write("Recall: {0}\n".format(recall))
        text_file.write("F1 measure: {0}\n".format(f1_measure))


def generate_report(result, filename, target):
    """ save classification results in a report"""
    with open(filename + "_result.txt", "w") as text_file:
        print("Writing text file")
        text_file.write(classification_report(
            target, result, target_names=class_list))


def plot_precision_recall_curve_all_classes(average_precision,
                                            precision,
                                            recall,
                                            file_name,
                                            num_class,
                                            show_plot=False):
    plt.clf()
    plt.plot(recall["micro"],
             precision["micro"],
             label='micro-average Precision-recall curve (area = {0:0.2f})'
             ''.format(average_precision["micro"]))
    for i in range(num_class):
        plt.plot(recall[i],
                 precision[i],
                 label='Precision-recall curve of class {0} (area = {1:0.2f})'
                 ''.format(i, average_precision[i]))
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Extension of Precision-Recall curve to multi-class')
    plt.legend(loc="lower right")
    plt.savefig('figure_' + file_name + '_precision_recall_curve_all.png')
    if show_plot:
        plt.show()


def plot_precision_recall_curve(average_precision, precision, recall, file_name, show_plot=False):
    plt.clf()
    plt.plot(recall[0], precision[0], label='Precision-Recall curve')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.ylim([0.0, 1.05])
    plt.xlim([0.0, 1.0])
    plt.title(
        'Precision-Recall example: AUC={0:0.2f}'.format(average_precision[0]))
    plt.legend(loc="lower left")
    plt.savefig('figure_' + file_name + '_precision_recall_curve.png')
    if show_plot:
        plt.show()
