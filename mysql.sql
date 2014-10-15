CREATE TABLE `test`.`media_set` (
  `media_sets_id` INT NOT NULL,
  `name` VARCHAR(100) NULL,
  `description` VARCHAR(300) NULL,
  PRIMARY KEY (`media_sets_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;

CREATE TABLE `media` (
  `media_id` int(11) NOT NULL,
  `url` varchar(300) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`media_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `test`.`media_media_set` (
  `media_id` INT NOT NULL,
  `media_set_id` INT NOT NULL,
  PRIMARY KEY (`media_id`, `media_set_id`),
  INDEX `media_sets_id_idx` (`media_set_id` ASC),
  CONSTRAINT `media_id`
    FOREIGN KEY (`media_id`)
    REFERENCES `test`.`media` (`media_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `media_sets_id`
    FOREIGN KEY (`media_set_id`)
    REFERENCES `test`.`media_set` (`media_sets_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);