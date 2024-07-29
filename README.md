# NextRead

NextRead is a simple book recommendation system. It works by taking a book title from the user and suggesting 10 other books that are similar to the first one. You can find the live demo [here](https://nextread-book-recommender.streamlit.app/).

## Installation and Setup
To install and set up this project locally, follow these next steps.

1. Clone this repository.
    ```
    git clone https://github.com/ade555/NextRead.git
    ```
2. Navigate to the NextRead folder:
    ```
    cd NextRead
    ```
3. Install the project dependencies with this command:
    ```
    pip install -r requirements.txt
    ```
    **NOTE**: You can optionally create a virtual environment before installing the dependencies.
4. Run the project by typing this command into your terminal:
    ```
    streamlit run recommender.py
    ```

## Scraping Data
This project currently uses a small amount of data from the [Goodreads website](https://www.goodreads.com/). If you want to scrape more data, you can use the following command to run the scraper:
```
python scraper.py
```

## Contribution
This project welcomes new ideas and contributions. To make a contribution, firstly raise an issue about it. Once you have been assigned the issue, you are free to clone the project and make your contributions to it.
You can submit your contribution by making a pull request to the main repo.