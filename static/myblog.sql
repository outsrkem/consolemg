-- MySQL dump 10.14  Distrib 5.5.65-MariaDB, for Linux (x86_64)
--
-- Host: 10.10.10.24    Database: blognote
-- ------------------------------------------------------
-- Server version 5.6.44
--
-- 建议使用 source 命令导入，若手动执行，需注意外键关联。
--
-- Current Database: `blognote`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `myblog` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;

USE `myblog`;

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for article
-- ----------------------------
DROP TABLE IF EXISTS `article`;
CREATE TABLE `article` (
  `articleid` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `userid` int(11) NOT NULL COMMENT '关联发布者信息',
  `type` tinyint(255) NOT NULL COMMENT '关联文章类型',
  `headline` varchar(100) NOT NULL COMMENT '文章标题',
  `content` mediumtext COMMENT '文章内容',
  `thumbnail` varchar(30) DEFAULT NULL COMMENT '缩略图文件名',
  `credit` int(11) DEFAULT '0' COMMENT '文章消耗的积分数',
  `readcount` int(11) DEFAULT '0' COMMENT '文章阅读次数',
  `replycount` int(11) DEFAULT '0' COMMENT '评论回复次数',
  `recmmended` tinyint(255) DEFAULT '0' COMMENT '是否设为推荐文章',
  `hidden` tinyint(255) DEFAULT '0' COMMENT '文章是否被隐藏',
  `drafted` tinyint(255) DEFAULT '0' COMMENT '文章是否是草稿',
  `checked` tinyint(255) DEFAULT '1' COMMENT '文章是否已被审核',
  `createtime` datetime DEFAULT NULL COMMENT '新增时间',
  `updatetime` datetime DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`articleid`),
  KEY `userid` (`userid`),
  CONSTRAINT `article_ibfk_1` FOREIGN KEY (`userid`) REFERENCES `users` (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='文章表';

-- ----------------------------
-- Records of article
-- ----------------------------

-- ----------------------------
-- Table structure for comment
-- ----------------------------
DROP TABLE IF EXISTS `comment`;
CREATE TABLE `comment` (
  `commentid` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `userid` int(11) NOT NULL COMMENT '关联评论者信息',
  `articleid` int(11) NOT NULL COMMENT '关联文章表信息',
  `content` text COMMENT '评论的内容',
  `ipaddr` varchar(30) DEFAULT NULL COMMENT '评论用户的IP地址',
  `replyid` int(11) DEFAULT '0' COMMENT '是否为原始评论及被回复评论的ID号，0 为原始评论',
  `agreecount` int(11) DEFAULT '0' COMMENT '赞同该评论的数量',
  `opposecount` int(11) DEFAULT '0' COMMENT '反对该评论的数量',
  `hidden` tinyint(255) DEFAULT '0' COMMENT '评论是否被隐藏',
  `createtime` datetime DEFAULT NULL COMMENT '新增时间',
  `updatetime` datetime DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`commentid`),
  KEY `userid` (`userid`),
  KEY `articleid` (`articleid`),
  CONSTRAINT `comment_ibfk_1` FOREIGN KEY (`userid`) REFERENCES `users` (`userid`),
  CONSTRAINT `comment_ibfk_2` FOREIGN KEY (`articleid`) REFERENCES `article` (`articleid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='评论表';

-- ----------------------------
-- Records of comment
-- ----------------------------

-- ----------------------------
-- Table structure for credit
-- ----------------------------
DROP TABLE IF EXISTS `credit`;
CREATE TABLE `credit` (
  `creditid` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `userid` int(11) NOT NULL COMMENT '关联用户表信息',
  `category` varchar(10) DEFAULT NULL COMMENT '积分变化的原因说明，便于用户和管理员查询明细',
  `target` int(11) DEFAULT NULL COMMENT '积分新增或消耗对应的目标对象。如果是阅读和评论文章，则对应为文章ID，如果在正常登录或注册，则显示0。',
  `credit` int(11) DEFAULT NULL COMMENT '积分的具体数量,整数，可正可负',
  `createtime` datetime DEFAULT NULL COMMENT '新增时间',
  `updatetime` datetime DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`creditid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='积分表';

-- ----------------------------
-- Records of credit
-- ----------------------------

-- ----------------------------
-- Table structure for favorite
-- ----------------------------
DROP TABLE IF EXISTS `favorite`;
CREATE TABLE `favorite` (
  `favorite` int(11) NOT NULL AUTO_INCREMENT COMMENT '收藏表',
  `articleid` int(11) NOT NULL COMMENT '关联文章表信息',
  `userid` int(11) NOT NULL COMMENT '关联用户表信息',
  `canceled` tinyint(255) DEFAULT '0' COMMENT '文章是否被取消收藏',
  `createtime` datetime DEFAULT NULL COMMENT '新增时间',
  `updatetime` datetime DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`favorite`),
  KEY `articleid` (`articleid`),
  KEY `userid` (`userid`),
  CONSTRAINT `favorite_ibfk_1` FOREIGN KEY (`articleid`) REFERENCES `article` (`articleid`),
  CONSTRAINT `favorite_ibfk_2` FOREIGN KEY (`userid`) REFERENCES `users` (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='收藏表';

-- ----------------------------
-- Records of favorite
-- ----------------------------

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `userid` int(11) NOT NULL AUTO_INCREMENT COMMENT '用户表id',
  `username` varchar(50) NOT NULL COMMENT '用户登录名',
  `password` varchar(32) NOT NULL COMMENT '登录密码',
  `nickname` varchar(30) DEFAULT NULL COMMENT '昵称',
  `avatar` varchar(255) DEFAULT NULL COMMENT '用户头像的图片文件名',
  `qq` varchar(15) DEFAULT NULL COMMENT 'QQ',
  `role` varchar(10) DEFAULT NULL COMMENT '角色',
  `credit` int(11) DEFAULT '50' COMMENT '用户的剩余积分',
  `createtime` datetime DEFAULT NULL COMMENT '创建时间',
  `updatetime` datetime DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表信息表';

-- ----------------------------
-- Records of users
-- ----------------------------

-- ----------------------------
-- Table structure for loginrecord
-- ----------------------------
DROP TABLE IF EXISTS `loginrecord`;
CREATE TABLE `loginrecord` (
  `tid` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `userid` int(11) DEFAULT NULL COMMENT '用户ID，关联users表userid',
  `logipaddr` varchar(30) DEFAULT NULL COMMENT '用户登录的源IP',
  `createtime` datetime DEFAULT NULL COMMENT '登录时间',
  PRIMARY KEY (`tid`),
  KEY `userid` (`userid`),
  CONSTRAINT `loginrecord_ibfk_1` FOREIGN KEY (`userid`) REFERENCES `users` (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='登录日志表';

-- ----------------------------
-- Records of users
-- ----------------------------

INSERT INTO `users` (`username`, `password`, `nickname`, `avatar`, `qq`, `role`, `credit`) VALUES ('admin@admin.com', 'e10adc3949ba59abbe56e057f20f883e', 'admin', '1.jpg', '00000000', 'admin', '200');
INSERT INTO `users` (`username`, `password`, `nickname`, `avatar`, `qq`, `role`, `credit`) VALUES ('yong@126.com', 'e10adc3949ba59abbe56e057f20f883e', 'yong', '2.jpg', '123456', 'user', '50');
INSERT INTO `users` (`username`, `password`, `nickname`, `avatar`, `qq`, `role`, `credit`) VALUES ('www@baidu.com', 'e10adc3949ba59abbe56e057f20f883e', 'www', '3.jpg', '93847748', 'user', '50');
INSERT INTO `users` (`username`, `password`, `nickname`, `avatar`, `qq`, `role`, `credit`) VALUES ('yong4@126.com', 'e10adc3949ba59abbe56e057f20f883e', 'yong4', '2.jpg', '76813276', 'user', '50');
INSERT INTO `users` (`username`, `password`, `nickname`, `avatar`, `qq`, `role`, `credit`) VALUES ('yong5@126.com', 'e10adc3949ba59abbe56e057f20f883e', 'yong5', '5.jpg', '237467', 'user', '50');
INSERT INTO `users` (`username`, `password`, `nickname`, `avatar`, `qq`, `role`, `credit`) VALUES ('yong6@126.com', 'e10adc3949ba59abbe56e057f20f883e', 'yong6', '6.jpg', '988769823', 'user', '50');


















