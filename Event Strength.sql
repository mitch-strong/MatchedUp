SELECT D.Name, C.Strength FROM (

SELECT B.Event_ID as 'Event', COUNT(*) as 'Strength' FROM (
SELECT Topic_ID from `Matchup`.`Interests` 
WHERE Profile_ID = '1' )A
JOIN
(SELECT Event_ID, Topic_ID from `Matchup`.`Event_Topics` 
) B
ON A.Topic_ID = B.Topic_ID
GROUP BY B.Event_ID
ORDER BY COUNT(*) DESC) C
JOIN
(SELECT * FROM `Matchup`.`Event`) D
ON C.Event = D.Event_ID;