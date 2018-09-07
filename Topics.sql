SELECT A.Person, B.Topic AS 'Topic' FROM (

SELECT B.Profile_ID as 'Person', B.Topic_ID as 'Topic' FROM (SELECT Profile_ID, Topic_ID from `Matchup`.`Interests` 
WHERE Profile_ID = '1' )A
JOIN
(SELECT Profile_ID, Topic_ID from `Matchup`.`Interests` 
WHERE Profile_ID <> '1') B
ON A.Topic_ID = B.Topic_ID
ORDER BY B.Profile_ID DESC) A 
JOIN 
`Matchup`.`Topics` B 
ON A.Topic = B.Topic_ID
ORDER BY A.Person;