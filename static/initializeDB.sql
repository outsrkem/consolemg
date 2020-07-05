-- ----------------------------
-- Table structure for user
-- ----------------------------
CREATE TABLE `user` (
  `ID` int(255) NOT NULL AUTO_INCREMENT,
  `USERID` varchar(255) NOT NULL,
  `USERNAME` varchar(255) NOT NULL,
  `ROLE` int(1) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8;
INSERT INTO `consolemg`.`user` (`USERID`, `USERNAME`, `ROLE`) VALUES ('1593846915297111', 'admin', '0');
INSERT INTO `consolemg`.`user` (`USERID`, `USERNAME`, `ROLE`) VALUES ('1593846915497322', 'lisi', '1');


-- ----------------------------
-- Table structure for passwd
-- ----------------------------
CREATE TABLE `passwd` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `USERID` varchar(255) NOT NULL COMMENT '用户id',
  `PASSWD` varchar(255) NOT NULL COMMENT '密码',
  `CHANGE` datetime DEFAULT NULL COMMENT '最近一次密码修改时间',
  `EXPIRES` varchar(255) DEFAULT NULL COMMENT '密码过期时间',
  `INACTIVE` int(11) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;
INSERT INTO `consolemg`.`passwd` (`USERID`, `PASSWD`, `CHANGE`, `EXPIRES`, `INACTIVE`) VALUES ('1593846915297111', 'pbkdf2:sha256:150000$sNZdzStJ$d852c2cbba9c20a0c70c2c89497a0396c7ac3b10067dec036d88447069b8d802', '2020-06-04 15:42:39', NULL, '99999');
INSERT INTO `consolemg`.`passwd` (`USERID`, `PASSWD`, `CHANGE`, `EXPIRES`, `INACTIVE`) VALUES ('1593846915497322', 'pbkdf2:sha256:150000$neAMqQB1$2d483312a03c21e0ade6345dcdb9c638d1f5470a285ce1fe5dd406ef0b962939', '2020-06-07 15:42:39', NULL, '0');


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