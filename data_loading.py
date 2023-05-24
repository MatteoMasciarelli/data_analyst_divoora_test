from db_info import H
from ETLPipeline import ETLPipeline

def perform_etl(filename: str, H: str) -> None:
    pipeline: ETLPipeline = ETLPipeline(filename=filename, H = H)

    pipeline.extract()
    pipeline.load()

if __name__ == '__main__':
    filename = ""
    perform_etl(filename=filename, H = H)