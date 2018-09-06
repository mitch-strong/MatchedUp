SELECT B.Profile_ID as 'Match', COUNT(*) as 'Strength' FROM (SELECT Profile_ID, Topic_ID from `Matchup`.`Interests` 
WHERE Profile_ID = '1' )A
JOIN
(SELECT Profile_ID, Topic_ID from `Matchup`.`Interests` 
WHERE Profile_ID <> '1') B
ON A.Topic_ID = B.Topic_ID
GROUP BY B.Profile_ID
ORDER BY COUNT(*) DESC;