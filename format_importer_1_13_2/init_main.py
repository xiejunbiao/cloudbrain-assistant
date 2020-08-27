import traceback
import os
import time


def data_init_start():

    try:
        path = os.path.abspath(os.path.dirname(__file__))
        exception_result = ''
        lsdir = os.listdir(path)
        try:
            # 初始化订单表
            os.system('python %s/format_importer.py mysql_event @%s/conf/mysql_event_init_sale_order.conf' % (path, path))

        except:

            exception_result = exception_result + '\n' + traceback.print_exc(), traceback.print_exc()

        try:
            # 初始化退单表
            os.system('python %s/format_importer.py mysql_event @%s/conf/mysql_event_init_return_sku.conf' % (path, path))

        except:
            exception_result = exception_result + '\n' + traceback.print_exc(), traceback.print_exc()

        if exception_result:
            # return 'at %s traceback.print_exc():' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + str(
            #     traceback.print_exc())
            return exception_result
        else:
            # print('at %s Data import completed' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + str(path))
            return 'at %s Data import completed' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    except Exception as e:
        # print('traceback.print_exc():', traceback.print_exc())
        return 'traceback.print_exc():%s' % str(traceback.print_exc())


if __name__ == '__main__':
    data_init_start()
