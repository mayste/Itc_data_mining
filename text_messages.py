import command_args

SQL_READY = "Connection with MYSQL ready"

SQL_DB_CREATION = "Database was created successfully"

SQL_TABLE_CREATION = "Tables were created successfully"

SQL_FAIL = "Fail to connect to MYSQL"

SQL_FAIL_TABLE = "Fail to create table on MYSQL"

COMPANY_INSERT_FAIL = "Insertion of one company on Company table failed"

COMPETITOR_INSERT_FAIL = "Insertion of one competitor one Company_Competitors table failed"

JOB_INSERT_FAIL = "Insertion of one job on Job table failed"

ERROR_NUM_PAGES = """f'There is a problem to get the number of available pages of jobs post' """

ERROR_NEXT = "Not succeed to click on next"

ERROR_OPTIONAL_DATA = "There is no optional data for this company on this job"

BROWSER_CONNECTION = 'Browser connect to URL'

SEARCH_JOB = f'Search for job title: {command_args.args.job_title}'

SEARCH_LOCATION = f"Search for job location: {command_args.args.job_location}"

NO_POP_UP = 'No popup to close'

POP_UP_CLOSE = 'Succeed to close popup'

CONNECT_NEW_URL = f'Browser connect to new URL with : {command_args.args.job_title}, {command_args.args.job_location}'

AVAILABLE_PAGES = f'Succeed to catch number of available pages'

COMPETITOR_PAGE = "Search for competitor's company page"

NEW_COMPANY_URL = "Browser connect to new URL of a company"
