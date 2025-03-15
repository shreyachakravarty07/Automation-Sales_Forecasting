# import os

# file_list = os.listdir("./models")
# # print("Files in directory:", file_list)
# if file_list == []:
#     dump(prophet_model, 'prophet_model_0.joblib')
# file_list.sort()
# print(file_list[-1])

# latest = file_list[-1].remove('prophet_model_', '.joblib')
# new = int(latest) + 1
# # dump(prophet_model, f'prophet_model_{new}.joblib')

from data_prep import train_size
print(train_size)