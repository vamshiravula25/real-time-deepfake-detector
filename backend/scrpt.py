import kagglehub

# Download the latest version of the dataset
path = kagglehub.dataset_download("therealeye/real-vs-fake-img")

# Print the path where the dataset has been downloaded
print("Path to dataset files:", path)
