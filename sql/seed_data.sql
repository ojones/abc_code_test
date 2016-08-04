insert into questions values(
    'question-1',
    'What is a conditional?',
    3
);

insert into keywords values(
    'keyword-1',
    'question-1',
    'An if then statement.',
    'if then'
);

insert into keywords values(
    'keyword-2',
    'question-1',
    'A yes no question.',
    'yes no'
);

insert into keywords values(
    'keyword-3',
    'question-1',
    'Code that provides instructions that depend on if then statement.',
    'instructions depend'
);

insert into keywords values(
    'keyword-4',
    'question-1',
    'Action case or statement dependant on a condition.',
    'case depend'
);

insert into criteria values(
    'criteria-1',
    'keywords matched in order'
);

insert into criteria values(
    'criteria-2',
    'keywords matched out of order'
);

insert into criteria values(
    'criteria-3',
    'some keywords matched'
);

insert into criteria values(
    'criteria-4',
    'no keywords matched'
);

insert into testees values(
    'testee-1',
    'Ada',
    'Lovelace',
    '233 Baker ST, London, England 1800',
    'ada@example.com',
    '321-654-0987',
    9,
    4,
    0
);

insert into tests values(
    'test-1',
    'testee-1',
    '2017-07-18 08:23:19'
);

insert into scores values(
    'score-1',
    'test-1',
    'question-1',
    'A conditional is a way to tell between two cases.',
    2,
    'criteria-3'
);




