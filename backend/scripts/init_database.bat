@echo off
echo 正在创建数据库...
mysql -uroot -p12345678 < init_db.sql
echo 数据库创建完成！

