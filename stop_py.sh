ps aux | grep bigdata_assis_main_test1.py |grep -v grep|cut -c 9-15|xargs kill -9
