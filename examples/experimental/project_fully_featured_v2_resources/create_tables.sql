create or replace TABLE DEMO_DB_STAGING.CORE.COMMENTS (
	ID FLOAT,
	PARENT FLOAT,
	TIME FLOAT,
	TYPE VARCHAR(16777216),
	USER_ID VARCHAR(16777216),
	TEXT VARCHAR(16777216),
	KIDS VARCHAR(16777216),
	SCORE FLOAT,
	TITLE VARCHAR(16777216),
	DESCENDANTS FLOAT,
	URL VARCHAR(16777216)
);


create or replace TABLE DEMO_DB_STAGING.CORE.STORIES (
	ID FLOAT,
	PARENT FLOAT,
	TIME FLOAT,
	TYPE VARCHAR(16777216),
	USER_ID VARCHAR(16777216),
	TEXT VARCHAR(16777216),
	KIDS VARCHAR(16777216),
	SCORE FLOAT,
	TITLE VARCHAR(16777216),
	DESCENDANTS FLOAT,
	URL VARCHAR(16777216)
);

create or replace TABLE DEMO_DB_STAGING.CORE.COMMENT_STORIES (
	STORY_ID FLOAT,
	COMMENTER_ID VARCHAR(16777216)
);