SELECT X.Name, Y.Topic FROM (
SELECT C.Name, D.Topic_ID FROM (
SELECT B.Event_ID  as 'Event' , B.Topic_ID FROM (
SELECT Topic_ID from `Matchup`.`Interests` 
WHERE Profile_ID = '1' )A
JOIN
(SELECT Event_ID, Topic_ID from `Matchup`.`Event_Topics` ) B
ON A.Topic_ID = B.Topic_ID
) D 
JOIN 
(SELECT * FROM `Matchup`.`Event` ) C
ON D.Event = C.Event_ID) X
JOIN 
(SELECT * FROM `Matchup`.`Topics` ) Y
ON X.Topic_ID = Y.Topic_ID
ORDER BY X.NAME;

