# ECG2AF Model Web Application

Welcome to my **ECG2AF Prediction Web App**! This application demonstrates the deployment of ECG2AF, a clinical AI model designed to predict the risk of developing atrial fibrillation (AF) from ECG data. 

To run this app locally, place `app.py`, `ecg_model.py`, and the required folders inside the `app/` directory. Ensure that `Dockerfile` and `requirements.txt` are in the parent directory. 

I developed this project using tools like `vim` and `VS Code`, utilizing GitHub Copilot for some function autocompletion. The app is currently deployed on an `EC2` instance (Linux `t2.medium`), with an attached 32 GB `gp3` volume for additional storage. Additionally, I’ve set the Nginx file upload limit to 500 MB to accommodate larger files.


In this tutorial, you’ll learn how to set up, run, and use the app. Here is an outline of the first page that can submit multiple `.hd5` files to the server. 

![Upload ECG File](fig/uploads2.png)

## Background

AI is widely used in clinical applications to improve risk stratification and intervention. For example, neuroscientists and psychiatrists use AI to understand how the human brain functions and to identify the roots of certain psychopathological disorders. However, this project focuses on cardiovascular disease, specifically aiming to predict AF risk based on ECG data.
I launched this app on AWS, enabling users to upload an ECG file, process it with the ECG2AF model, and view the prediction results.

## Objective

Our objective is to allow users to: Upload an ECG file (.hd5 format), Process the uploaded ECG using a pre-trained ECG2AF model, and Display the prediction results, including four output values.

## How It Works

1. **Upload your ECG file(s)** in `.hd5` format by dragging and dropping it into the upload area.
2. **Process with ECG2AF**: The model will process the file in real-time.
3. **View Predictions**: At the end, the app displays four predictions for each ECG file, including AF risk and demographic estimations. You will also see charts corresponding to each result for better interpretation. 

### Prediction Outputs

- **AF Risk**: Estimated risk for developing atrial fibrillation.
- **Sex Prediction (Male/Female)**: Probability-based estimate of biological sex.
- **Age Prediction**: Estimated age based on ECG data.
- **AF In Read (Yes/No)**: Classification for AF presence in the read.

Each prediction result includes a probability or estimate, displayed in both a table and a chart for easy viewing.

![Example Results](fig/results2.png)

## Try It Out!

The app is live [here](http://34.204.36.84/)! 

All you need to do is:
1. Open the link.
2. Drag and drop your `.hd5` ECG file onto the upload area.
3. Wait a few seconds, and you’ll see the predictions displayed for you!

## Scalability Considerations

The current version supports multiple file submissions, but they are processed sequentially. While we recently moved the app to Nginx to balance requests, further scalability considerations remain. For handling larger data volumes and more users, here’s what we would consider next:

1. **Batch Processing**: Process multiple ECG files simultaneously using a distributed system or Python's built-in ``multiprocessing`` functions like ``Pool``. 
2. **Database and Caching**: Store previously uploaded `.hd5` files on disk for each user separately, allowing them to choose from their past uploads to avoid reprocessing
3. **Cloud Deployment and Load Balancing**:  We’ve deployed this tool on AWS, using Nginx to balance incoming requests effectively. AWS’s Elastic Load Balancer (ELB) could also be incorporated if additional scaling is needed. By default, Auto Scaling groups with ELB will automatically register new EC2 instances, so no manual setup is required for load balancing at scale.  

## Technical Requirements

The app is built with Flask and TensorFlow for ease of deployment and model integration.

- **Python Version**: 3.6+
- **Libraries**: Flask, TensorFlow, and other dependencies in `requirements.txt`.

To run the app locally, you can clone this repository, set up a virtual environment, install dependencies, and run `app.py`. For more detailed steps, check below.

## Local Setup

To run this app locally:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/ecg2af.git
   cd ecg2af
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Flask app**:
   ```bash
   python app.py
   ```

4. **Open the app**: Go to `http://127.0.0.1:5000` in your browser.

## Error Handling

We’ve designed the app to handle errors gracefully. Here’s how it responds:
- **Invalid File Format**: The app will prompt you to upload a valid `.hd5` ECG file if an incorrect format is uploaded.
- **Server Errors**: Any server errors during processing will display a user-friendly error message.

## Resources and References

- **ECG2AF Model**: [GitHub Link](https://github.com/broadinstitute/ml4h/tree/master/model_zoo/ECG2AF)
- **Model Setup**: We used the ML4H Docker container `ghcr.io/broadinstitute/ml4h:tf2.9-latest-cpu` for easy library setup.

Happy predicting, and let us know if you have any questions! My email is `javiddadashkarimi@gmail.com`

## Visualization and Results
The charts in the application that you see after submission, are bar charts created using the `Chart.js` library, an open-source JavaScript package used for creating interactive and visually appealing data visualizations (see [chartjs](https://www.chartjs.org/)). Each chart presents predictions related to the uploaded .hd5 files, including AF risk, sex prediction (male and female), and age prediction values. 

We used ``ChatGPT 40 mini`` in order to create the css file and format the first page.

## Adding Nginx to Flask with Docker

Nginx acts as a reverse proxy for our Flask app in Docker, handling HTTP requests on port `80` and forwarding them to Flask on 5000. So I set up the app on port 5000, but it can be accessible via default port `80` through Nginx. 

### Benefits of Using Nginx
Running Flask alone is fine for testing, but it lacks the scalability, security, and robustness needed for production. Nginx fills those gaps effectively.

- **Security**: Nginx hides the Flask server from direct internet exposure.

- **Load Balancing**: Can manage traffic efficiently and scale easily.

- **Static File Handling**: Serves static files faster, reducing Flask's load.

- **Production-Ready**: Unlike Flask's dev server, Nginx handles multiple users reliably.

Since previously I had deployed our `CAROT Project` on Nginx, it didn't take that much time from me! 

