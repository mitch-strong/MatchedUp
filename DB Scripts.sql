CREATE SCHEMA `Matchup` ;

CREATE TABLE `Matchup`.`Profile` (
  `Profile_ID` int(10) NOT NULL AUTO_INCREMENT,
  `Name` VARCHAR(45) NULL,
  `Gender` VARCHAR(45) NULL,
  `DOB` DATETIME NULL,
  `From_City` VARCHAR(45) NULL,
  `New_City` VARCHAR(45) NULL,
  `School` VARCHAR(45) NULL,
  `Language` VARCHAR(45) NULL,
  `Major` VARCHAR(45) NULL,
  `Local` INT NULL,
  `Email` VARCHAR(45) NOT NULL,
  `Password` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`Profile_ID`),
  UNIQUE `Email` (`Email`),
  UNIQUE INDEX `Profile_ID_UNIQUE` (`Profile_ID` ASC));

CREATE TABLE `Matchup`.`Topics` (
  `Topic_ID` int(10) NOT NULL AUTO_INCREMENT,
  `Topic` VARCHAR(45) NULL,
  PRIMARY KEY (`Topic_ID`),
  UNIQUE INDEX `Topic_ID_UNIQUE` (`Topic_ID` ASC));

CREATE TABLE `Matchup`.`Interests` (
  `Profile_ID` int(10) NOT NULL,
  `Topic_ID` int(10) NOT NULL,
  INDEX `Interests_Profile_ID_idx` (`Profile_ID` ASC),
  INDEX `Interests_Topic_ID_idx` (`Topic_ID` ASC),
  CONSTRAINT `Interests_Profile_ID`
    FOREIGN KEY (`Profile_ID`)
    REFERENCES `Matchup`.`Profile` (`Profile_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Interests_Topic_ID`
    FOREIGN KEY (`Topic_ID`)
    REFERENCES `Matchup`.`Topics` (`Topic_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

CREATE TABLE `Matchup`.`Matched` (
  `Match_ID` VARCHAR(45) NOT NULL,
  `Accepted` INT NULL,
  `Person1` VARCHAR(45) NULL,
  `Person2` VARCHAR(45) NULL,
  `Strength` INT NULL,
  PRIMARY KEY (`Match_ID`),
  UNIQUE INDEX `Match_ID_UNIQUE` (`Match_ID` ASC) ,
  INDEX `Match_Person1_idx` (`Person1` ASC) ,
  INDEX `Match_Person2_idx` (`Person2` ASC) ,
  CONSTRAINT `Match_Person1`
    FOREIGN KEY (`Person1`)
    REFERENCES `Matchup`.`Profile` (`Profile_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Match_Person2`
    FOREIGN KEY (`Person2`)
    REFERENCES `Matchup`.`Profile` (`Profile_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

CREATE TABLE `Matchup`.`Matched_On` (
  `Matched_ID` VARCHAR(45) NOT NULL,
  `Topic_ID` VARCHAR(45) NOT NULL,
  INDEX `Matched_On_MatchID_idx` (`Matched_ID` ASC) ,
  INDEX `Matched_On_TopicID_idx` (`Topic_ID` ASC) ,
  CONSTRAINT `Matched_On_MatchID`
    FOREIGN KEY (`Matched_ID`)
    REFERENCES `Matchup`.`Matched` (`Match_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Matched_On_TopicID`
    FOREIGN KEY (`Topic_ID`)
    REFERENCES `Matchup`.`Topics` (`Topic_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

CREATE TABLE `Matchup`.`Event` (
  `Event_ID` VARCHAR(45) NOT NULL,
  `Name` VARCHAR(45) NULL,
  `Location` VARCHAR(45) NULL,
  `Time` DATETIME NULL,
  PRIMARY KEY (`Event_ID`),
  UNIQUE INDEX `Event_ID_UNIQUE` (`Event_ID` ASC) );


CREATE TABLE `Matchup`.`Event_Topics` (
  `Event_ID` VARCHAR(45) NOT NULL,
  `Topic_ID` VARCHAR(45) NOT NULL,
  INDEX `EventTopic_Event_idx` (`Event_ID` ASC) ,
  INDEX `EventTopic_Topic_idx` (`Topic_ID` ASC) ,
  CONSTRAINT `EventTopic_Event`
    FOREIGN KEY (`Event_ID`)
    REFERENCES `Matchup`.`Event` (`Event_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `EventTopic_Topic`
    FOREIGN KEY (`Topic_ID`)
    REFERENCES `Matchup`.`Topics` (`Topic_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

CREATE TABLE `Matchup`.`Attend` (
  `Event_ID` VARCHAR(45) NOT NULL,
  `Profile_ID` VARCHAR(45) NOT NULL,
  INDEX `Attend_Event_idx` (`Event_ID` ASC) ,
  INDEX `Attend_Profile_idx` (`Profile_ID` ASC) ,
  CONSTRAINT `Attend_Event`
    FOREIGN KEY (`Event_ID`)
    REFERENCES `Matchup`.`Event` (`Event_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Attend_Profile`
    FOREIGN KEY (`Profile_ID`)
    REFERENCES `Matchup`.`Profile` (`Profile_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

CREATE TABLE `Matchup`.`Forum` (
  `Forum_ID` VARCHAR(45) NOT NULL,
  `Name` VARCHAR(45) NULL,
  ` Created_On` DATETIME NULL,
  `Created_By` VARCHAR(45) NULL,
  PRIMARY KEY (`Forum_ID`),
  UNIQUE INDEX `Forum_ID_UNIQUE` (`Forum_ID` ASC) ,
  INDEX `Forum_CreatedBy_idx` (`Created_By` ASC) ,
  CONSTRAINT `Forum_CreatedBy`
    FOREIGN KEY (`Created_By`)
    REFERENCES `Matchup`.`Profile` (`Profile_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

CREATE TABLE `Matchup`.`Post` (
  `Post_ID` VARCHAR(45) NOT NULL,
  `Forum_ID` VARCHAR(45) NULL,
  `Profile_ID` VARCHAR(45) NULL,
  `Text` VARCHAR(255) NULL,
  PRIMARY KEY (`Post_ID`),
  UNIQUE INDEX `Post_ID_UNIQUE` (`Post_ID` ASC) ,
  INDEX `Post_Forum_idx` (`Forum_ID` ASC) ,
  INDEX `Post_Profile_idx` (`Profile_ID` ASC) ,
  CONSTRAINT `Post_Forum`
    FOREIGN KEY (`Forum_ID`)
    REFERENCES `Matchup`.`Forum` (`Forum_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Post_Profile`
    FOREIGN KEY (`Profile_ID`)
    REFERENCES `Matchup`.`Profile` (`Profile_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);
