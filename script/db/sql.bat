DROP DATABASE IF EXISTS `feed`;
create database feed default character set utf8 collate utf8_general_ci;
grant all on feed.* to 'feed'@'localhost' identified by 'feed!@#';


@echo off
set /p pwd=password:
rem mysql -uroot -p%pwd%  --default-character-set=utf8 < clear.sql
mysql -uroot -p%pwd%  -Dfeed --default-character-set=utf8 < ec2_wb_users.sql
PAUSE