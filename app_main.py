import threading

import logger.logger as logger
from flask import Flask, abort, request, jsonify
import application.app_context as application_context
from application.demand import poco_demand_ver, poco_demand_parser
from crontab.crontab_cal import start_crontab
from database.db_conn import get_data_conn_orm

app = Flask(__name__)

_MODULE_NAME = u'application.app_main'

@app.route('/srv6_pathapp_webrtc/vpath_calc', methods=['POST'])
def optimal_vpath_cal_restful():
    request_json = request.get_json(force=True)
    if not request_json:
        abort(400)
    poco_demand = request_json
    if not poco_demand_ver.is_poco_demand_vaild(poco_demand):
        logger.log_warn(_MODULE_NAME, u'Unvaild virtual path calculation demand\n\n')
        abort(500)
    result = application_context.optimal_virtual_path_cal(poco_demand)
    status_code = result[0]
    result_str = result[1]
    resp = {
        'status': status_code,
        'links': result_str,
    }
    logger.log_info(_MODULE_NAME, u'Resending result : ' + str(request_json) + '\n\n')
    return jsonify(result), 200


@app.route('/srv6_pathapp_webrtc/topo_calc', methods=['POST'])
def optimal_topology_cal_restful():
    request_json = request.get_json(force=True)
    print(request_json)
    if not request_json:
        abort(400)
    poco_demand = request_json
    if not poco_demand_ver.is_poco_demand_vaild(poco_demand):
        logger.log_warn(_MODULE_NAME, u'Unvaild virtual path calculation demand\n\n')
        abort(500)
    logger.log_info(_MODULE_NAME, u'Resending result : ' + str(request_json) + '\n\n')
    return jsonify(request_json), 200


@app.route('/srv6_pathapp_webrtc/topo_mainten', methods=['POST'])
def optimal_topology_mainten_restful():
    request_json = request.get_json(force=True)
    print (request_json)
    if not request_json:
        abort(400)
    poco_demand = request_json
    if not poco_demand_ver.is_poco_demand_vaild(poco_demand):
        logger.log_warn(_MODULE_NAME, u'Unvaild virtual path calculation demand\n\n')
        abort(500)
    logger.log_info(_MODULE_NAME, u'Resending result : ' + str(request_json) + '\n\n')
    return jsonify(request_json), 200


# def update_data_job():
#     global format_data_set
#     format_data_set = application_context.update_memory_data()

@app.route('/srv6_pathapp_webrtc/test', methods=['POST'])
def get_test_db():
    request_json = request.get_json(force=True)
    if not request_json:
        abort(400)
    poco_demand = request_json
    if not poco_demand_ver.is_poco_demand_vaild(poco_demand):
        logger.log_warn(_MODULE_NAME, u'Unvaild virtual path calculation demand\n\n')
        abort(500)
    conn=get_data_conn_orm('')
    cursor = conn.cursor()

    # 执行SQL查询
    cursor.execute("SELECT * FROM node")
    records = cursor.fetchall()
    print(records)
    cursor.close()
    conn.close()

    result = application_context.optimal_virtual_path_cal(poco_demand)
    status_code = result[0]
    result_str = result[1]
    resp = {
        'status': status_code,
        'links': result_str,
    }
    logger.log_info(_MODULE_NAME, u'Resending result : ' + str(request_json) + '\n\n')
    return jsonify(result), 200


if __name__ == '__main__':
    # logger.log_info(_MODULE_NAME, u'Starting application...')
    # if not format_data_set:
    #     update_data_job()

    thread = threading.Thread(target=start_crontab)
    # 启动线程
    thread.start()
    app.run(host="0.0.0.0", port=8888, debug=False)
    # 每天将缓存中的全量qos数据读到内存中，为拓扑计算提供服务
    # 如果每次计算时读取的话时间较长
    # schedule.every().day.at("00:00").do(update_data_job)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
