from data_loading import perform_etl
from report_construction import perform_both
from db_info import H

def main():
    # Perform etl process
    perform_etl("database.xlsx", H)

    # Perform queries and extract data
    #perform_both()

if __name__ == '__main__':
    main()