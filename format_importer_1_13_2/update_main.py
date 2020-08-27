import traceback
import os
import time


def data_update_start():
    try:
        path = os.path.abspath(os.path.dirname(__file__))
        os.system(
            'python %s/format_importer.py mysql_event @%s/conf/mysql_event_update_sale_order.conf' % (path, path))
        os.system(
            'python %s/format_importer.py mysql_event @%s/conf/mysql_event_update_sale_return_sku.conf' % (path, path))
        os.system(
            'python %s/format_importer.py mysql_event @%s/conf/mysql_event_update_area_data_set.conf' % (path, path))
        os.system(
            'python %s/format_importer.py mysql_event @%s/conf/mysql_event_update_goods_area_count.conf' % (path, path))
        os.system(
            'python %s/format_importer.py mysql_event @%s/conf/mysql_event_update_owner_binding_area_count.conf' % (path, path))
        return 'at %s Data import completed' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    except Exception as e:
        # print('traceback.print_exc():', traceback.print_exc())
        return 'at %s traceback.print_exc():' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + str(traceback.print_exc())


if __name__ == '__main__':
    data_update_start()
