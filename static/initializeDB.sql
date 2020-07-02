-- ----------------------------
-- Table structure for user
-- ----------------------------
CREATE TABLE `user` (
  `USERID` int(255) NOT NULL AUTO_INCREMENT,
  `USERNAME` varchar(255) NOT NULL,
  `ROLE` int(1) NOT NULL,
  PRIMARY KEY (`USERID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
INSERT INTO `consolemg`.`user` (`USERID`, `USERNAME`, `ROLE`) VALUES ('1', 'admin', '0');
INSERT INTO `consolemg`.`user` (`USERID`, `USERNAME`, `ROLE`) VALUES ('2', 'lisi', '1');

-- ----------------------------
-- Table structure for passwd
-- ----------------------------
CREATE TABLE `passwd` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `USERID` int(11) NOT NULL,
  `PASSWD` varchar(255) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
INSERT INTO `consolemg`.`passwd` (`ID`, `USERID`, `PASSWD`) VALUES ('1', '1', 'e10adc3949ba59abbe56e057f20f883e');
INSERT INTO `consolemg`.`passwd` (`ID`, `USERID`, `PASSWD`) VALUES ('2', '2', 'e10adc3949ba59abbe56e057f20f883e');

-- ----------------------------
-- Table structure for links
-- ----------------------------
CREATE TABLE `links` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `LINKNAME` varchar(255) NOT NULL,
  `LINKURL` varchar(255) NOT NULL,
  `EXPLAIN` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;