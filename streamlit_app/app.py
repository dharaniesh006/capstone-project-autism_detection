import sklearn_evaluation
import os

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

import warnings
warnings.filterwarnings("ignore")

# Classification
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier


from sklearn.model_selection import train_test_split
from sklearn.model_selection import  cross_val_score, ShuffleSplit, cross_validate
from sklearn.exceptions import DataConversionWarning
from sklearn.feature_selection import mutual_info_classif
from sklearn.preprocessing import LabelEncoder

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier

# Metrics :
from sklearn.metrics import mean_squared_log_error,mean_squared_error, r2_score,mean_absolute_error
from sklearn.metrics import accuracy_score

# Classification
from sklearn.metrics import recall_score, f1_score, fbeta_score, r2_score, roc_auc_score, roc_curve, auc, cohen_kappa_score   
data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'dataset2.csv')
data=pd.read_csv(data_path)
st.title("AUTISM SPECTRUM DISORDER PREDICTION FOR TODDLERS")
st.set_option('deprecation.showPyplotGlobalUse', False)

data = data.rename(columns={"Age_Mons":"Age Months",
                        "Family_mem_with_ASD":"Family Member with ASD",
                        "Class/ASD Traits ": "ASD Traits"})
#removing irrelevant columns
data_=data.shape
data.drop(['Case_No', 'Who completed the test'], axis = 1, inplace = True)
yes_autism= data[data['ASD Traits']=='Yes']
no_autism= data[data['ASD Traits']=='No']

from sklearn.metrics import classification_report, confusion_matrix
from sklearn.metrics import recall_score, precision_score

from scipy import stats

def metrics(model_name, y_train, y_test, y_hat_train, y_hat_test):
    '''Print out the evaluation metrics for a given model's predictions'''
    st.header(f'Model: {model_name}')
    st.write('-' * 60)

    # Calculate confusion matrix
    cm_test = confusion_matrix(y_test, y_hat_test)
    cm_train = confusion_matrix(y_train, y_hat_train)

    # Calculate recall and precision
    recall_test = recall_score(y_test, y_hat_test)
    recall_train = recall_score(y_train, y_hat_train)
    precision_test = precision_score(y_test, y_hat_test)
    precision_train = precision_score(y_train, y_hat_train)

    st.write(f'Test accuracy: {round(accuracy_score(y_test, y_hat_test), 2)}')
    st.write(f'Test recall: {round(recall_test, 2)}')
    st.write(f'Test precision: {round(precision_test, 2)}')
    st.write(f'Train accuracy: {round(accuracy_score(y_train, y_hat_train), 2)}')
    st.write(f'Train recall: {round(recall_train, 2)}')
    st.write(f'Train precision: {round(precision_train, 2)}')
    st.write('-' * 60)

    # Display confusion matrix for Test Data
    st.write('Confusion Matrix for Test Data:')
    st.table(pd.DataFrame(cm_test, columns=["Predicted 0", "Predicted 1"], index=["Actual 0", "Actual 1"]))
    # Display confusion matrix as a plot
    plt.figure(figsize=(2, 1))
    sns.heatmap(cm_test, annot=True, fmt="d", cmap="Blues")
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    st.pyplot()

    # Display confusion matrix for Train Data
    st.write('Confusion Matrix for Train Data:')
    st.table(pd.DataFrame(cm_train, columns=["Predicted 0", "Predicted 1"], index=["Actual 0", "Actual 1"]))
    # Display confusion matrix for the training data as a plot
    plt.figure(figsize=(2, 1))
    sns.heatmap(cm_train, annot=True, fmt="d", cmap="Blues")
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    st.pyplot()
    # Plot recall
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 4))

    ax1.bar(['Test Recall', 'Train Recall'], [recall_test, recall_train], color=['blue', 'blue'])
    ax1.set_ylabel('Recall')
    ax1.set_title('Recall')
    ax1.set_ylim(0, 1.2)

    ax2.bar(['Test Precision', 'Train Precision'], [precision_test, precision_train], color=['green', 'green'])
    ax2.set_ylabel('Precision')
    ax2.set_title('Precision')
    ax2.set_ylim(0, 1.2)

    st.pyplot(fig)

    report = classification_report(y_test,y_hat_test, output_dict=True)
    # Convert the classification report to a Pandas DataFrame
    report_df = pd.DataFrame(report).transpose()
    st.write('\nTest report:\n')
    st.write(report_df)

    st.write('~' * 60)

    trainreport = classification_report(y_train,y_hat_train, output_dict=True)
    # Convert the classification report to a Pandas DataFrame
    trainreport_df = pd.DataFrame(trainreport).transpose()
    st.write('\nTest report:\n')
    st.write(trainreport_df)

    st.write('~' * 60)
    st.write('\n\n')


def models(name,model,X_train,y_train,X_test,y_test):
    model.fit(X_train, y_train)
    y_hat_test = model.predict(X_test).astype(int)
    y_hat_train = model.predict(X_train).astype(int)
    st.write(name, 'Accuracy Score is : ', accuracy_score(y_test, y_hat_test))
    metrics(name, y_train, y_test, y_hat_train, y_hat_test)

def display_correlation_heatmap(data):
    plt.style.use('dark_background')
    corr = data.corr()
    plt.figure(figsize=(9, 9))
    sns.heatmap(data=corr, annot=True, square=True, cbar=True)
    st.pyplot()  # Display the plot in the Streamlit app
def display_bar(data):
    plt.style.use('dark_background')
    barplot=data.iloc[:,0:10].sum().sort_values().plot(kind="bar")
    barplot.bar_label(barplot.containers[0])
    st.pyplot()
def display_donut(data):
    plt.style.use('dark_background')
    data["ASD Traits"].value_counts().plot(kind="pie", autopct="%1.1f%%", wedgeprops=dict(width=.3, edgecolor='w'))
    st.pyplot()
def display_sex(data):
    plt.style.use('dark_background')
    sns.countplot(x = 'Qchat-10-Score', hue = 'Sex', data = data)
    st.pyplot()
def display_count(data):
    plt.style.use('dark_background')
    plt.figure(figsize=(20,6))
    sns.countplot(x='Ethnicity',data=yes_autism,order= yes_autism['Ethnicity'].value_counts().index[:11],hue='Sex',palette='Paired')
    plt.title('Ethnicity Distribution of Positive ASD among Toddlers')
    plt.xlabel('Ethnicity')
    plt.tight_layout()
    st.pyplot()
def display_barcount(data):
    plt.style.use('dark_background')
    #Lets visualize the distribution of autism in family within different ethnicity
    f, ax = plt.subplots(figsize=(12, 8))
    sns.countplot(x='Family Member with ASD',data=yes_autism,hue='Ethnicity',palette='rainbow',ax=ax)
    ax.set_title('Positive ASD Toddler relatives with Autism distribution for different ethnicities')
    ax.set_xlabel('Toddler Relatives with ASD')
    plt.tight_layout()
    st.pyplot()
def display_dist(data):
    le = LabelEncoder()
    columns = ['Ethnicity', 'Family Member with ASD', 'ASD Traits', 'Sex', 'Jaundice']
    for col in columns:
        data[col] = le.fit_transform(data[col])
    plt.style.use('dark_background')
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    axes = axes.ravel()
    for i, col in enumerate(data.iloc[:, 11:13]):
        sns.distplot(x=data[col], ax=axes[i])
        axes[i].set_title(col)
    plt.tight_layout()
    plt.show()
    st.pyplot()

def display_ethnicity(data):
    plt.style.use('dark_background')
    plt.figure(figsize = (16,8))
    sns.countplot(x = 'Ethnicity', data=yes_autism)
    st.pyplot()

def display_plot(data):
    df_plot = data.groupby(['Sex', 'Ethnicity']).size().reset_index().pivot(columns='Sex', index='Ethnicity', values=0)
    df_plot.index.name = 'Ethnicity'  # Set the index name to 'Ethnicity'
    df_plot.plot(kind='bar', stacked=True)
    st.pyplot()
    
with st.sidebar:
    add_sidebar=st.radio('pages:',('Home','Visualization of data','Information gain','ML algorithms','Overfitting','Forward Feature selection','Significant algorithm','Conclusion','Prediction for input from user'))
if add_sidebar=='Home':
    st.header('Autism Dataset')
    st.table(data.head(10))
    st.header('Autism Data description')
    df=data.describe()
    st.table(df)
    st.header('Details')
    st.subheader("Checking null values")
    temp=data.isnull().sum()
    st.table(temp)
    st.subheader('Shape of data')
    temp=data.shape
    st.write('Before processing',data_)
    st.write('After preprocessing',temp)
    st.subheader('Toddler')
    ans=st.radio('Autism Toddler:',['Yes','No'])
    if ans=='Yes':
      st.write(yes_autism)
      st.write("Percentage of Toddlers with autism", round(len(yes_autism)/len(data) * 100,2))
    elif ans=='No':
      st.write(no_autism)
      st.write("Percentage of Toddlers with autism",round(len(no_autism)/len(data) * 100,2))

    st.subheader('Outlier Detection')
    def detect_outliers(column_data, threshold):
        z_scores = np.abs(stats.zscore(column_data))
        outliers = np.where(z_scores > threshold)[0]
        return outliers


    threshold = 3
    #st.slider("Select the Z-Score Threshold", min_value=1, max_value=10, value=3)

    columns_to_analyze = ['Age Months', 'Qchat-10-Score']

    for column in columns_to_analyze:
        column_data = data[column]
        outliers = detect_outliers(column_data, threshold)

            # Display the results
        st.write(f"Outliers in column '{column}':", outliers)
        plt.figure(figsize=(8, 6))
        sns.boxplot(y=column_data)            
        plt.title(f'Box Plot for {column}')
        st.pyplot(plt)




elif add_sidebar=='Visualization of data':
    st.header("Correlation Heatmap")
    display_correlation_heatmap(data)
    st.header("Which feature among a1-a10 contributes most to ASD traits?")
    display_bar(data)
    st.header("ASD TRAITS-YES OR NO")
    display_donut(data)
    st.header("Q-chat score based on sex")
    display_sex(data)
    st.header("Ethnicity Distribution of Positive ASD among Toddlers")
    display_count(data)
    st.header("Positive ASD Toddler relatives with Autism distribution for different ethnicities")
    display_barcount(data)
    st.header("Data Distribution on Age and Qchat 10 Score")
    display_dist(data)
    st.header("Ethnicity and Autism")
    display_ethnicity(data)
    st.header("Sex and Ethnicity")
    display_plot(data)
    
elif add_sidebar=="Information gain":
      

    #from sklearn.preprocessing import LabelEncoder
    #from sklearn.model_selection import train_test_split
    #from sklearn.feature_selection import mutual_info_classif

    # Create a Streamlit radio button to select the calculation method
    option = st.radio("Information gain", ["inbuilt", "manual"])


    # Label encode categorical columns
    le = LabelEncoder()
    columns = ['Ethnicity', 'ASD Traits', 'Sex', 'Jaundice']
    for col in columns:
        data[col] = le.fit_transform(data[col])

    # Drop columns that are not needed
    columns_to_drop = ["Family Member with ASD"]
    data.drop(columns=columns_to_drop, inplace=True)

    # Define X and y
    X = data.drop(columns=['ASD Traits', 'Qchat-10-Score'])
    y = data['ASD Traits']

    # Select test size using a Streamlit selectbox
    #test = st.selectbox("Test size:", (10, 20, 30, 40), index=None)

    # Replace the index=None with an initial index value, e.g., 0
    test = st.selectbox("Test size:", (10, 20, 30, 40), index=0)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test, random_state=42)

    # Calculate and display information gain based on the selected option
    if option == 'manual':
        test = test / 100
        pt_cols = X_train.columns.values.tolist()

        # Define functions for entropy and information gain
        def entropy(y):
            unique_values, counts = np.unique(y, return_counts=True)
            probabilities = counts / len(y)
            return -np.sum(probabilities * np.log2(probabilities))

        def information_gain(X, y, feature):
            total_entropy = entropy(y)
            unique_values, counts = np.unique(X[feature], return_counts=True)
            weighted_entropy = np.sum([(counts[i] / len(X)) * entropy(y[X[feature] == unique_values[i]]) for i in range(len(unique_values))])
            return total_entropy - weighted_entropy

        # Calculate information gain for each feature
        information_gains = {}
        for feature in X_train.columns:
            information_gains[feature] = information_gain(X_train, y_train, feature)

        # Sort features by information gain in descending order
        sorted_information_gains = sorted(information_gains.items(), key=lambda x: x[1], reverse=True)

        # Display the information gains in a DataFrame
        infogain = pd.DataFrame(sorted_information_gains)
        infogain.columns = ['Feature', 'Information Gain']
        infogain.reset_index(drop=True, inplace=True)
        st.write(infogain)

        # Plot the information gains
        feature_names, gains = zip(*sorted_information_gains)
        st.header("Information gain for features")
        plt.figure(figsize=(8, 6))
        plt.plot(feature_names, gains, marker='o', linestyle='-')
        plt.xticks(rotation=90)
        plt.xlabel('Features')
        plt.ylabel('Information Gain')
        plt.title('Information Gain for Features')
        plt.tight_layout()
        plt.show()
        st.pyplot(plt)

    elif option == 'inbuilt':
        # Calculate information gain using scikit-learn's mutual_info_classif
        mutual_info = mutual_info_classif(X, y)
        mutual_info = pd.Series(mutual_info)
        mutual_info.index = X_train.columns

        index_name = 'Feature'
        mutual_info.index.name = index_name

        series_name = 'Information Gain'
        mutual_info.name = series_name

        st.write(mutual_info.sort_values(ascending=False))
        st.subheader('Information gain for features')
        cols = mutual_info.sort_values(ascending=False).plot.bar(figsize=(20, 8))
        st.pyplot()
    

elif add_sidebar=='ML algorithms':
    tab1, tab2, tab3 ,tab4,tab5= st.tabs(["Logistic Regression", "KNN", "Decision Tree","Gaussian NB","Random Forest"])
    le = LabelEncoder()
    columns = ['Ethnicity', 'ASD Traits', 'Sex', 'Jaundice']
    for col in columns:
        data[col] = le.fit_transform(data[col])
    columns_to_drop = ["Family Member with ASD"]
    data.drop(columns=columns_to_drop, inplace=True)
    X = data.drop(columns=['ASD Traits','Qchat-10-Score'])
    y = data['ASD Traits']
    #st.table(X.info())
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    model = []
    model.append(('LR', LogisticRegression()))
    model.append(('KNN', KNeighborsClassifier()))
    model.append(('CART', DecisionTreeClassifier()))
    model.append(('NB', GaussianNB()))
    model.append(('RF', RandomForestClassifier()))
    with tab1:
      name,modl=model[0]
      models(name,modl,X_train,y_train,X_test,y_test)
    with tab2:
      name,modl=model[1]
      models(name,modl,X_train,y_train,X_test,y_test)
    with tab3:
      name,modl=model[2]
      models(name,modl,X_train,y_train,X_test,y_test)
    with tab4:
      name,modl=model[3]
      models(name,modl,X_train,y_train,X_test,y_test)
    with tab5:
      name,modl=model[4]
      models(name,modl,X_train,y_train,X_test,y_test)

elif add_sidebar=='Overfitting':
    st.subheader('CHECKING OVERFITTING')
    st.write('Interpretation: Compare the training accuracy with the mean cross-validation score: If the training accuracy is significantly higher than the mean cross-validation score, it suggests overfitting. If the training accuracy is close to the mean cross-validation score, it indicates that the model is likely not overfitting.')
    tab1, tab2, tab3 ,tab4,tab5,tab6= st.tabs(["Logistic Regression", "KNN", "Decision Tree","Gaussian NB","Random Forest","Learning curve"])
    le = LabelEncoder()
    columns = ['Ethnicity', 'ASD Traits', 'Sex', 'Jaundice']
    columns_to_drop = ["Family Member with ASD"]
    data.drop(columns=columns_to_drop, inplace=True)
    for col in columns:
        data[col] = le.fit_transform(data[col])
    X = data.drop(columns=['ASD Traits','Qchat-10-Score'])
    y = data['ASD Traits']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    from sklearn.model_selection import cross_val_score

    with tab1:
      LR=LogisticRegression()
      LR.fit(X_train,y_train)
      y_train_pred = LR.predict(X_train)
      training_accuracy = accuracy_score(y_train, y_train_pred)
      st.write(f"Training Accuracy: {training_accuracy}")

      scores = cross_val_score(LR, X, y, cv=5)  # 5-fold cross-validation
      st.write(f"\nCross-Validation Scores: {scores}")
      avg_score=scores.mean()
      std_score=scores.std()

      st.write(f"\nAverage Cross-Validation Score: {avg_score}")
      st.write(f"\nStandard Deviation of Cross-Validation Scores: {std_score}")

    with tab2:
      Knn=KNeighborsClassifier()
      Knn.fit(X_train,y_train)
      y_train_pred = Knn.predict(X_train)
      training_accuracy = accuracy_score(y_train, y_train_pred)
      st.write(f"Training Accuracy: {training_accuracy}")

      scores = cross_val_score(Knn, X, y, cv=5)  # 5-fold cross-validation
      st.write(f"\nCross-Validation Scores: {scores}")
      avg_score=scores.mean()
      std_score=scores.std()

      st.write(f"\nAverage Cross-Validation Score: {avg_score}")
      st.write(f"\nStandard Deviation of Cross-Validation Scores: {std_score}")

    with tab3:
      DC=DecisionTreeClassifier()
      DC.fit(X_train,y_train)
      # Assuming RF is your classifier and X, y are your data and labels
      y_train_pred = DC.predict(X_train)
      training_accuracy = accuracy_score(y_train, y_train_pred)
      st.write(f"Training Accuracy: {training_accuracy}")

      scores = cross_val_score(DC, X, y, cv=5)  # 5-fold cross-validation
      st.write(f"\nCross-Validation Scores: {scores}")
      avg_score=scores.mean()
      std_score=scores.std()

      st.write(f"\nAverage Cross-Validation Score: {avg_score}")
      st.write(f"\nStandard Deviation of Cross-Validation Scores: {std_score}")

    with tab4:
      G=GaussianNB()
      G.fit(X_train,y_train)
      # Assuming RF is your classifier and X, y are your data and labels
      y_train_pred = G.predict(X_train)
      training_accuracy = accuracy_score(y_train, y_train_pred)
      st.write(f"Training Accuracy: {training_accuracy}")

      scores = cross_val_score(G, X, y, cv=5)  # 5-fold cross-validation
      st.write(f"\nCross-Validation Scores: {scores}")
      avg_score=scores.mean()
      std_score=scores.std()

      st.write(f"\nAverage Cross-Validation Score: {avg_score}")
      st.write(f"\nStandard Deviation of Cross-Validation Scores: {std_score}")
    with tab5:
      RF=RandomForestClassifier()
      RF.fit(X_train,y_train)
      # Assuming RF is your classifier and X, y are your data and labels
      y_train_pred = RF.predict(X_train)
      training_accuracy = accuracy_score(y_train, y_train_pred)
      st.write(f"Training Accuracy: {training_accuracy}")

      scores = cross_val_score(RF, X, y, cv=5)  # 5-fold cross-validation
      st.write(f"\nCross-Validation Scores: {scores}")
      avg_score=scores.mean()
      std_score=scores.std()

      st.write(f"\nAverage Cross-Validation Score: {avg_score}")
      st.write(f"\nStandard Deviation of Cross-Validation Scores: {std_score}")

    from sklearn.model_selection import learning_curve
    from sklearn_evaluation import plot

    with tab6:
        plt.style.use('dark_background')
        train_sizes = np.linspace(0.1, 1.0, 5)
        # Create a figure with a grid of subplots
        fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(15, 10))
        models = [LR, Knn, DC, G, RF]
        model_names = ['Linear Regression', 'K-Nearest Neighbors', 'Decision Tree', 'GaussianNB', 'Random Forest']

        for i, model in enumerate(models):
            row = i // 3
            col = i % 3

            train_sizes, train_scores, test_scores = learning_curve(model, X=X_train, y=y_train, train_sizes=train_sizes)
            plot.learning_curve(train_scores, test_scores, train_sizes, ax=axes[row, col])
            axes[row, col].set_title(f'Learning Curve for {model_names[i]}')

      # Add labels and titles
        for ax in axes.flatten():
            ax.set_xlabel('Training Set Size')
            ax.set_ylabel('Score')
            ax.grid(True)

        fig.delaxes(axes[1, 2])
        plt.subplots_adjust(hspace=0.7)
        plt.show()
        st.pyplot()

      
    #   rf_probas = RF.fit(X_train, y_train).predict_proba(X_test)
    #   lr_probas = LR.fit(X_train, y_train).predict_proba(X_test)
    #   dc_probas = DC.fit(X_train, y_train).predict_proba(X_test)
    #   nb_probas = G.fit(X_train, y_train).predict_proba(X_test)
    #   knn_probas = Knn.fit(X_train, y_train).predict_proba(X_test)

    #   probabilities = [rf_probas, lr_probas, nb_probas,dc_probas,knn_probas]

    #   clf_names = [
    #       "Random Forest",
    #       "Logistic Regression",
    #       "Gaussian Naive Bayes",
    #       "Decision Tree",
    #       "KNN"
    #   ]

    #   probabilities = [rf_probas, lr_probas, nb_probas,dc_probas,knn_probas]
    #   plot.calibration_curve(y_test, probabilities, clf_names=clf_names)
    #st.pyplot()
      

elif add_sidebar=='Forward Feature selection':
    le = LabelEncoder()
    columns = ['Ethnicity', 'Family Member with ASD', 'ASD Traits', 'Sex', 'Jaundice']
    for col in columns:
        data[col] = le.fit_transform(data[col])

    from mlxtend.feature_selection import SequentialFeatureSelector as sfs
    from sklearn.preprocessing import OneHotEncoder
    from sklearn.ensemble import RandomForestClassifier

    columns_to_drop = ["Family Member with ASD"]
    data.drop(columns=columns_to_drop, inplace=True)
    X = data.drop(['ASD Traits','Qchat-10-Score'], axis = 1)
    y = data['ASD Traits']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.40, random_state =42)
    y_train = y_train.ravel()
    y_test = y_test.ravel()
    st.subheader("Forward feature selection")
    st.write('Training dataset shape:', X_train.shape, y_train.shape)
    st.write('Testing dataset shape:', X_test.shape, y_test.shape)

    clf = RandomForestClassifier(n_estimators=100, n_jobs=-1)
    sfs1 = sfs(clf,
              k_features=5,
              forward=True,
              floating=False,
              verbose=2,
              scoring='accuracy',
              cv=5)

    # Perform SFFS
    sfs1 = sfs1.fit(X_train, y_train)
    st.write(sfs1.subsets_)
    st.write(sfs1.k_score_)
    st.write('Best accuracy score: %.2f' % sfs1.k_score_)
    st.write('Best subset (indices):', sfs1.k_feature_idx_)
    st.write('Best subset (corresponding names):', sfs1.k_feature_names_)
    feat_cols = list(sfs1.k_feature_idx_)
    st.write(feat_cols)
    st.write(X_train.iloc[:, feat_cols].head())

    clf = RandomForestClassifier(n_estimators=1000, random_state=42, max_depth=4)
    clf.fit(X_train.iloc[:, feat_cols], y_train)

    y_train_pred = clf.predict(X_train.iloc[:, feat_cols])
    st.write('Training accuracy on selected features: %.3f' % accuracy_score(y_train, y_train_pred))

    y_test_pred = clf.predict(X_test.iloc[:, feat_cols])
    st.write('Testing accuracy on selected features: %.3f' % accuracy_score(y_test, y_test_pred))

elif add_sidebar=='Significant algorithm':
    le = LabelEncoder()
    columns = ['Ethnicity', 'Family Member with ASD', 'ASD Traits', 'Sex', 'Jaundice']
    for col in columns:
        data[col] = le.fit_transform(data[col])
    from scipy.stats import ttest_ind,f_oneway

    # Sample data (replace with your actual performance metrics)
    sdata = {
        'LR':[1.00,1.00,1.00],
        'KNN':[0.85,0.87,0.86],
        'DecisionTree':[0.87,0.85,0.86],
        'GaussianNB':[0.91,0.90,0.90],
        'RandomForest':[0.45,1.00,0.62]
    }

    # Create a DataFrame from the sample data
    df=pd.DataFrame(sdata)

    # Perform one-way ANOVA
    f_statistic, p_value = f_oneway(df['LR'], df['KNN'], df['DecisionTree'],df['GaussianNB'],df['RandomForest'])

    # Print ANOVA results
    st.write("One-way ANOVA Results:")
    st.write(f"F-statistic: {f_statistic}")
    st.write(f"P-value: {p_value}")

    if p_value < 0.05:
        st.write("One-way ANOVA indicates significant differences among algorithms (p < 0.05)")
    else:
        st.write("One-way ANOVA does not indicate significant differences among algorithms (p >= 0.05)")
    import scipy.stats as stats
    from itertools import combinations

    # List of algorithm names
    algorithms = ['KNN', 'LR', 'DecisionTree', 'RandomForest', 'GaussianNB']

    # Perform pairwise t-tests
    significant_pairs = []
    for combo in combinations(algorithms, 2):
        alg1, alg2 = combo
        t_stat, p_value = stats.ttest_ind(
            df[alg1],
            df[alg2],
            equal_var=False  # Set to False if variances are unequal
        )
        if p_value < 0.05:
            significant_pairs.append((alg1, alg2))

    if len(significant_pairs) > 0:
        print("Significant pairwise differences:")
        for pair in significant_pairs:
            st.write(f"{pair[0]} and {pair[1]} are significantly different.")
    else:
        st.write("No significant pairwise differences found.")


elif add_sidebar=='Conclusion':
    le = LabelEncoder()
    columns = ['Ethnicity', 'Family Member with ASD', 'ASD Traits', 'Sex', 'Jaundice']
    for col in columns:
        data[col] = le.fit_transform(data[col])

    columns_to_drop = ["Family Member with ASD"]
    data.drop(columns=columns_to_drop, inplace=True)

    X = data.drop(['ASD Traits','Qchat-10-Score'], axis = 1)
    y = data['ASD Traits']
    models=['LogisticRegression','KNeighborsClassifier','DecisionTreeClassifier',
        'GaussianNB','RandomForestClassifier']

    test_Accuracy=[1.0,0.91,0.91,0.94,0.64]

    accuracy_summary = pd.DataFrame([models, test_Accuracy]).T
    accuracy_summary.columns = ['Classifier', 'test_Accuracy']
    st.subheader('Accuracy Summary')
    st.table(accuracy_summary)
    #PICKLE FILE
    from sklearn.model_selection import StratifiedKFold
    from sklearn.metrics import accuracy_score

    LR=LogisticRegression()
    Knn=KNeighborsClassifier()
    DC=DecisionTreeClassifier()
    G=GaussianNB()
    RF=RandomForestClassifier()
    ml_algorithms = {
      'LR': LR,
      'KNN': Knn,
      'CART': DC,
      'NB':G,
      'RF': RF
    }


    kf = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
    best_models = {}
    for algo_name, algo_func in ml_algorithms.items():
      best_model = None
      best_metric = 0

      for fold_num, (train_idx, test_idx) in enumerate(kf.split(X, y), start=1):
        X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

        model = algo_func.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        metric = accuracy_score(y_test, y_pred)

        if metric > best_metric:
          best_metric = metric
          best_model = model
        print()
        print(algo_name,best_metric,end="")
        best_models[algo_name] = best_model
      print()

    model_save_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ml_training', 'models', 'best_models.pkl')
    with open(model_save_path, "wb") as model_file:
      pickle.dump(best_models,model_file)
    file_pathallmodels = model_save_path

    # Open the Pickle file for reading in binary mode
    with open(file_pathallmodels, "rb") as file1:
        loaded_dataallmodels = pickle.load(file1)

    st.write(loaded_dataallmodels)

    kf = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
    best_models = None
    best_accuracy = 0

    for algo_name, algo_func in ml_algorithms.items():
      total_accuracy=0

      for fold_num, (train_idx, test_idx) in enumerate(kf.split(X, y), start=1):
        X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

        model = algo_func.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        total_accuracy += accuracy

      average_accuracy = total_accuracy / kf.get_n_splits()

      if average_accuracy > best_accuracy:
          best_model = model
          best_accuracy = average_accuracy

    model_acc_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ml_training', 'models', 'best_modelaccuracybased.pkl')
    with open(model_acc_path, "wb") as model_file:
      pickle.dump(best_model,model_file)

    file_path = model_acc_path

    # Open the Pickle file for reading in binary mode
    with open(file_path, "rb") as file:
        loaded_data = pickle.load(file)

    st.write(loaded_data)


    st.write("Logistic Regression is a  good model in our autism project")
    st.write("\n")
    st.write("A9 is the most important features, other important features are A1, A3, A7 and A8. Jaundice and the type of gender'sex' are less important features. Genes in this study which appears through the column of family member with ASD is not an important feature")
    st.write("Autism Spectrum Disorder is not hereditary, thus it is independent of family members.")
    st.write("Males are more positive to autism than females")
    st.write("Ages close to 36 months which is three years old show more positive autism.")
    st.write("White European, Asian and middle eastern are the ethnicities that showed an increase in autism cases.")
    
elif add_sidebar=='Prediction for input from user':
   
    st.title("ASD Traits Prediction")

    # Add input elements for the user
    #st.sidebar.header("Input Features")

    # Provide input fields for the user to enter data
    age_months = st.slider("Age in Months", min_value=0, max_value=36, value=18)
    qchat_score = st.slider("Qchat-10 Score", min_value=0, max_value=10, value=6)
    sex = st.selectbox("Sex", ["Male", "Female"])
    ethnicity = st.selectbox("Ethnicity", ["middle eastern", "White European","Native Indian","Hispanic","asian","black","Latino","Pacifica","mixed","others"])
    #jaundice = st.checkbox("Jaundice")
    #family_member_asd = st.checkbox("Family Member with ASD")

    # Convert categorical features to numerical
    sex = 1 if sex == "Male" else 0
    #jaundice = 1 if jaundice == "True" else 0
    #family_member_asd = 1 if family_member_asd == "True" else 0
    ethnicity_mapping = {
        "middle eastern": 0,
        "White European": 1,
        "Native Indian": 2,
        "Hispanic": 3,
        "asian": 4,
        "black": 5,
        "Latino": 6,
        "Pacifica": 7,
        "mixed": 8,
        "others": 9
    }
    ethnicity_encoded = ethnicity_mapping[ethnicity]
    
    # Create a dictionary with the user input
    user_input = {
        'Age Months': age_months,
        'Qchat-10-Score': qchat_score,
        'Sex': sex,
        'Ethnicity': ethnicity_encoded,
    }

    le = LabelEncoder()
    columns = ['Ethnicity', 'Family Member with ASD', 'ASD Traits', 'Sex', 'Jaundice']
    for col in columns:
        data[col] = le.fit_transform(data[col])

    X = data.drop(columns=['ASD Traits'])
    y = data['ASD Traits']
    

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    columns_to_remove = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10','Jaundice','Family Member with ASD']
    X_train = X_train.drop(columns=columns_to_remove)


    LR=LogisticRegression()
    LR.fit(X_train,y_train)
    # Create a DataFrame from the user input
    user_df = pd.DataFrame([user_input])

    # Make predictions using the trained model
    prediction = LR.predict(user_df)

    # Display the prediction
    st.subheader("ASD Traits Prediction:")
    if prediction[0] == 1:
        st.write("High Risk of ASD Traits")
    else:
        st.write("Low Risk of ASD Traits")