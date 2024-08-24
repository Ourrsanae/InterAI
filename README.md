# InterAI Data Visualization & Interpretation Platform

This project provides a web platform for visualizing and interpreting data using advanced machine learning models. The platform allows users to upload CSV or Excel files, generate various plots, and receive automated insights about the data.

## Features

- **Data Visualization**: Generate bar charts, 3D scatter plots, and line charts from uploaded datasets.
- **Data Interpretation**: Automated data insights and pattern recognition using the Gemini AI model.
- **User-Friendly Interface**: Responsive design with support for file uploads and data selection for visualizations.


## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/interai-platform.git
    cd interai-platform
    ```

2. Set up a virtual environment and activate it:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up your API key for the Gemini AI model:

    The project uses the Google Generative AI API (Gemini). You need to configure your own API key.

    - Replace the placeholder in `upload.py` with your own API key:

    ```python
    genai.configure(api_key="YOUR_API_KEY_HERE")
    ```

    **Important**: The API currently supports queries in English. Ensure your input data and prompts are in English to get accurate results.

5. Run the application:

    ```bash
    flask run
    ```

    The app will be available at `http://127.0.0.1:5000`.

## Usage

1. Visit the homepage and navigate to the "Get Start" section.
2. Upload your `.csv` or `.xlsx` file.
3. Choose the type of visualization and customize the axes based on your data.
4. View the generated plot and the AI-driven data interpretation.

## Technologies Used

- **Backend**: Flask, Google Generative AI (Gemini)
- **Frontend**: HTML, CSS, Bootstrap, JavaScript, Plotly
- **Data Processing**: pandas
- **Visualization**: Plotly Express


## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

## Notes

- This project is intended for development and testing purposes. For production deployment, use a WSGI server.

---

![image](https://github.com/user-attachments/assets/528242f6-123c-4628-b2a8-2ef1cd9004cb)
![image](https://github.com/user-attachments/assets/006b81aa-cee7-41a5-b3ef-3d64b83d4d29)
![image](https://github.com/user-attachments/assets/4041f0b7-7fee-46a4-82a4-00ce2028a058)
![image](https://github.com/user-attachments/assets/643efab2-2c55-4e12-81b7-797fdb82e1b2)
![image](https://github.com/user-attachments/assets/5ddf562e-45bd-48bd-8901-23c95f772e2d)
![image](https://github.com/user-attachments/assets/c82c5dd1-0a92-4dfb-a248-ea369b651882)
![image](https://github.com/user-attachments/assets/54351171-4d45-4876-94b6-5786a43d7707)

