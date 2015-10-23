SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';

CREATE SCHEMA IF NOT EXISTS `rush_hour` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci ;
USE `rush_hour` ;

-- -----------------------------------------------------
-- Table `rush_hour`.`game_states`
-- -----------------------------------------------------
#drop table `rush_hour`.game_states;
#drop table `rush_hour`.topo_classes;
#drop table rush_hour.comb_classes;

-- distance_to_final_state == 0 => node is a final state

#drop table `rush_hour`.game_states;
CREATE  TABLE IF NOT EXISTS `rush_hour`.`game_states` (
  `game_number` INT NOT NULL ,
  `comb_class_id` TINYINT not NULL ,
  `game_hash_top` BIGINT NULL ,
  `game_hash_bottom` BIGINT NULL,
  `red_car_left_space` TINYINT NOT NULL,
  `connected_component_id` BIGINT NULL ,
  `topo_class_hash` BIT(36) NULL ,
  `distance_to_final_state` TinyInt Unsigned NULL ,
  `best_transition_state` BIGINT NULL ,
  
  
primary key (`game_number`, `comb_class_id`))
ENGINE = InnoDB;


#drop table rush_hour.comb_classes;
CREATE  TABLE IF NOT EXISTS `rush_hour`.`comb_classes` (
  `comb_class_id` BIGINT NOT NULL ,
  `num_cars` TINYINT NULL ,
  `num_trucks` TINYINT NULL ,
  `is_edge_complete` BIT NULL ,
  `is_connected_component_complete` VARCHAR(45) NULL ,
  `num_topo_classes` VARCHAR(45) NULL ,
  `num_states` VARCHAR(45) NULL ,
PRIMARY KEY (`comb_class_id`))
ENGINE = InnoDB;


#drop table rush_hour.topo_classes;
;CREATE  TABLE IF NOT EXISTS `rush_hour`.`topo_classes` (
  `comb_class_id` TINYINT NULL ,
  `topo_hash` BIT(36) NULL ,
  `is_edge_complete` BIT NULL ,
  `is_connected_component_complete` BIT NULL ,
  `is_solved` BIT NULL ,
  `num_states` INT NULL ,
  `num_connected_components` TINYINT NULL ,
  INDEX `combinatorial_class` (`comb_class_id` ASC) ,
  INDEX `topo_hash` (`topo_hash` ASC) )
ENGINE = InnoDB;


#drop table rush_hour.state_transitions;
;create table if not exists `rush_hour`.`state_transitions` (
  `comb_class_id` TINYINT NOT NULL,
  `x_state_game_number`	INT not null ,
  `y_state_game_number`	INT not null ,
  INDEX `x_state_game_number` (`x_state_game_number` ASC) ,
  INDEX `y_state_game_number` (`y_state_game_number` ASC) ,
  INDEX `combinatorial_class` (`comb_class_id` ASC)) 
ENGINE = InnoDB;

#drop table rush_hour.connected_components;
;create table if not exists `rush_hour`.`connected_components`(
    `connected_component_id`  BIGINT NOT NULL AUTO_INCREMENT,
    `num_states`              BIGINT NOT NULL,
    `topo_class_hash`         BIT(48),
    PRIMARY KEY(connected_component_id),
    INDEX `topo_class_hash` (`topo_class_hash` ASC) )
ENGINE = INNODB;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;


topo_class_hash