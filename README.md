# MSC_Alain_Frey

•	Scanner: accepts a video file and a subtitle file containing DJI telemetry. Inside the script properties such as frames to skip location of the database etc. can be configured.

•	Location Module: calculates the location of an object based on the input coordinates and the location expressed in pixels in the image.

•	Performance Test: Meassures the duration of each inference performed and plots the results such as mean and standard deviation.

•	Visualisation: Visualizes the outputs of the Location Module.

•	Duplicate Remover: Removes items from the databased based on proximity and similarity using a SIFT feature extractor.

•	Cluster Analysis: Used to analyze the precision of multi-detections of objects by clustering the detections into x clusters.

•	Sensitivity Analysis: Performs the sensitivity analysis on bearing, focal length and altitude for the location module and plots the results.

•	Cluster error: Calculates the centroid of the detections in the cluster and calculates and prints the mean and standard deviation of the detections with respect to the centroid.

•	Webserver: Displays the contents of the Database on a local website.

•	Index: Provides the template for the website used in the webserver.
