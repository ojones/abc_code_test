create table questions(
    id varchar(30),
    question varchar(255),
    points smallint
);

create table keywords(
    id varchar(30),
    question_id varchar(30),
    answer varchar(255),
    ordered_keywords varchar(255)
);

create table criteria(
    id varchar(30),
    explanation varchar(255)
);

create table testees(
    id varchar(30),
    first_name varchar(30),
    last_name varchar(30),
    address_name varchar(30),
    email_name varchar(30),
    phone_name varchar(30),
    age smallint,
    grade_level smallint,
    sex smallint
);

create table tests(
    id varchar(30),
    testee_id varchar(30),
    datetime varchar(30)
);

create table scores(
    id varchar(30),
    test_id varchar(30),
    question_id varchar(30),
    answered varchar(255),
    score smallint,
    criteria_id varchar(30)
);

create table fake_scores(
    id varchar(30),
    test_id varchar(30),
    question_id varchar(30),
    answered varchar(255),
    score smallint,
    criteria_id varchar(30)
);